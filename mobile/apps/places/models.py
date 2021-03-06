#-*- coding:utf-8 -*-
"""
这是地理信息系统的模型类，主要包含GIS以及GEO的模型类

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
from calendar import weekday, monthrange
from datetime import date, timedelta
from math import atan2, degrees

import simplejson
from dateutil.easter import easter

from django.conf import settings
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.gis.geos import Point
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

from baseutils.i18n import name_in_language


class Source(models.Model):
    """
    定义GIS数据源模型
    """

    module_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u"地理数据来源"
        verbose_name_plural = u"地理数据来源"




class EntityTypeCategory(models.Model):
    """
    定义GIS entity的分类模型，诸如：公交车站、娱乐场所、餐饮场所、火车站等等
    """

    name = models.TextField(blank=False)

    def __unicode__(self):
        return self.name


class EntityType(models.Model):
    """
    具体定义GIS entity的类别模型，诸如娱乐场所——夜总会之类，是子类.
    """

    slug = models.SlugField()
    
    @property
    def verbose_name(self):
        return name_in_language(self, 'verbose_name', self.slug)
    
    @property
    def verbose_name_singular(self):
        return name_in_language(self, 'verbose_name_singular', self.slug)
    
    @property
    def verbose_name_plural(self):
        return name_in_language(self, 'verbose_name_plural', self.slug)
    
    show_in_nearby_list = models.BooleanField(u'显示在附近列表')
    show_in_category_list = models.BooleanField(u'显示在分类列表')
    note = models.TextField(u'备注', null=True, blank=True)
    category = models.ForeignKey(EntityTypeCategory)

    subtype_of = models.ManyToManyField('self', blank=True, symmetrical=False,
                                        related_name="subtypes")
    subtype_of_completion = models.ManyToManyField('self',
            blank=True, symmetrical=False, related_name="subtypes_completion")

    def __unicode__(self):
        return self.verbose_name

    def save(self, *args, **kwargs):
        super(EntityType, self).save(*args, **kwargs)
        
        subtypes_of = set([self])
        for subtype_of in self.subtype_of.all():
            subtypes_of |= set(subtype_of.subtype_of_completion.all())
        
        if set(self.subtype_of_completion.all()) != subtypes_of:
            self.subtype_of_completion = subtypes_of
            for et in self.subtypes.all():
                et.save()
            for e in self.entities_completion.all():
                e.save()
        else:
            super(EntityType, self).save(*args, **kwargs)
            
    class Meta:
        verbose_name = u"地理位置分类"
        verbose_name_plural = u"地理位置分类"

class EntityTypeName(models.Model):
    """
    用来对GIS ENTITY模型进行多国语言化的模型类
    """
    entity_type = models.ForeignKey(EntityType, related_name='names')
    language_code = models.CharField('语言代码', max_length=10, choices=settings.LANGUAGES)
    verbose_name = models.TextField('别名')
    verbose_name_singular = models.TextField('单数别名')
    verbose_name_plural = models.TextField('复数别名')
    
    class Meta:
        unique_together = ('entity_type', 'language_code')




class EntityGroup(models.Model):
    """
    用来表示GIS entity实体之间的关系
    """
    
    @property
    def title(self):
        return name_in_language(self, 'title')

    source = models.ForeignKey(Source)
    ref_code = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = u"地理位置分组"
        verbose_name_plural = u"地理位置分组"    

class EntityGroupName(models.Model):
    entity_group = models.ForeignKey(EntityGroup, related_name='names')
    title = models.TextField(blank=False)
    language_code = models.CharField(max_length=10, choices=settings.LANGUAGES)
    
    class Meta:
        unique_together = ('entity_group', 'language_code')


class Entity(models.Model):
    """
    存储 geo-spatial point 以及 attached metadata的数据模型. 这里存储了整套系统中所有的地理信息数据.
    """
    
    @property
    def title(self):
        return name_in_language(self, 'title',
                    '%s:%s' % (self.primary_type.slug, self.slug))
    
    source = models.ForeignKey(Source)

    primary_type = models.ForeignKey(EntityType, null=True)
    all_types = models.ManyToManyField(EntityType, blank=True,
                                       related_name='entities')
    all_types_completion = models.ManyToManyField(EntityType, blank=True,
                                            related_name='entities_completion')
    slug = models.CharField(max_length=50)
    location = models.PointField(srid=4326, null=True)
    """
    修复：2011-07-09 本身是geometry=models.GeometryField(srid=4326, null=True),但是gdal里面会判断成UNKNOW类型的。结果就是openlayer中显示不出
    ，所以修复成为以下
    """
    
    geometry = models.PolygonField(srid=4326, null=True)
    
    _metadata = models.TextField(default='{}')
    
    absolute_url = models.TextField()
    
   
    is_sublocation = models.BooleanField(default=False)
    is_stack = models.BooleanField(default=False)



    groups = models.ManyToManyField(EntityGroup)

    
    
    def get_metadata(self):
        try:
            return self.__metadata
        except AttributeError:
            self.__metadata = simplejson.loads(self._metadata)
            return self.__metadata

    def set_metadata(self, metadata):
        self.__metadata = metadata
    metadata = property(get_metadata, set_metadata)
    
    # Translators: These are compass points
    COMPASS_POINTS = (_('N'), _('NE'), _('E'), _('SE'),
                      _('S'), _('SW'), _('W'), _('NW'))

    def get_bearing(self, p1):
        """
        Returns a compass point direction from current Entity to another Point
        """
        p2 = self.location
        lat_diff, lon_diff = p2[0] - p1[0], p2[1] - p1[1]
        compass_point = int(((90 - degrees(atan2(lon_diff, lat_diff)) + 22.5)
            % 360) // 45)
        return self.COMPASS_POINTS[compass_point]

    def get_distance_and_bearing_from(self, point):
        """
        Returns a distance and compass direction from current Entity to
        another point
        """
        if point is None or not self.location:
            return None, None
        if not isinstance(point, Point):
            point = Point(point, srid=4326)
        return (
            point.transform(3857, clone=True).distance(
                self.location.transform(3857, clone=True)),
            self.get_bearing(point),
        )
    
    def save(self, *args, **kwargs):
        try:
            self._metadata = simplejson.dumps(self.__metadata)
        except AttributeError:
            pass
        
        self.absolute_url = self._get_absolute_url()
        super(Entity, self).save(*args, **kwargs)
        self.update_all_types_completion()

    def update_all_types_completion(self):
        all_types = set()
        for t in self.all_types.all():
            all_types |= set(t.subtype_of_completion.all())
        if set(self.all_types_completion.all()) != all_types:
            self.all_types_completion = all_types
            self.metadata['types'] = [t.slug for t in all_types]

    @property
    def all_types_slugs(self):
        try:
            return self.metadata['types']
        except:
            self.metadata['types'] = [t.slug
                                      for t in self.all_types_completion.all()]
            self.save()
            return self.metadata['types']

    def delete(self, *args, **kwargs):
        super(Entity, self).delete()
    
    objects = models.GeoManager()

    def _get_absolute_url(self, identifiers=None):
        if identifiers:
            return reverse('places:entity', args=[identifiers['scheme'], identifiers['value']])
        else:
            identifiers = dict()
            identifiers['scheme'] = self.primary_type.slug
            identifiers['value'] = self.slug
            return reverse('places:entity', args=[identifiers['scheme'], identifiers['value']])

    def get_absolute_url(self):
        return self._get_absolute_url()
    
    def __unicode__(self):
        return self.title
    
    @property
    def display_id(self):
        for et in self.all_types.all():
            if et.slug == 'postcode':
                return getattr(self, et.id_field).strip()
            else:
                return getattr(self, et.id_field)

    def simplify_for_render(self, simplify_value, simplify_model):
        return simplify_value({
            '_type': '%s.%s' % (self.__module__[:-7], self._meta.object_name),
            '_pk': self.pk,
            '_url': self.get_absolute_url(),
            'location': self.location,
            'parent': simplify_model(self.parent, terse=True),
            'all_types': [simplify_model(t, terse=True)
                          for t in self.all_types_completion.all()],
            'primary_type': simplify_model(self.primary_type, terse=True),
            'metadata': self.metadata,
            'title': self.title,
            'identifier_scheme': self.primary_type,
            'identifier_value': self.title
        })
        
    class Meta:
        verbose_name = u"地理位置"
        verbose_name_plural = u"地理位置"

class EntityName(models.Model):
    entity = models.ForeignKey(Entity, related_name='names')
    title = models.TextField(blank=False)
    language_code = models.CharField(max_length=10, choices=settings.LANGUAGES)
    
    class Meta:
        unique_together = ('entity', 'language_code')

class Route(models.Model):
    """
    A class representing a route which a public transport service takes
    """
    
    # A publically displayed "ID" for this service, e.g., "4C"
    service_id = models.TextField()
    
    # The operator of this service, e.g., "Oxford Bus Company" or "First"
    operator = models.TextField(null=True, blank=True)
    
    # A longer name for this service, e.g., "4 to City & Abingdon"
    service_name = models.TextField(null=True, blank=False)
    
    # A primary key used in the external dataset
    external_ref = models.TextField()
    
    stops = models.ManyToManyField(Entity, through='StopOnRoute')
    
    def __unicode__(self):
        return u'%s: %s' % (self.service_id, self.service_name)
    
    class Meta:
        verbose_name = u"地理导航"
        verbose_name_plural = u"地理导航"

class StopOnRoute(models.Model):
    
    entity = models.ForeignKey(Entity)
    route = models.ForeignKey(Route)
    
    # The number stop which this is on this route
    order = models.IntegerField()
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
        return self.entity.title

class Journey(models.Model):
    """
    This is a scheduled public transport journey between entities
    """
    
    # The route this journey runs on (note that the stops RelatedManager should
    # contain where the bus actually stops - if it's different from the
    # indicated route)
    route = models.ForeignKey(Route)
    
    # A primary key used in the external dataset
    external_ref = models.TextField()
    
    # Any notes relating to this journey
    notes = models.TextField(null=True, blank=True)
    
    runs_on_monday = models.BooleanField()
    runs_on_tuesday = models.BooleanField()
    runs_on_wednesday = models.BooleanField()
    runs_on_thursday = models.BooleanField()
    runs_on_friday = models.BooleanField()
    runs_on_saturday = models.BooleanField()
    runs_on_sunday = models.BooleanField()
    runs_in_termtime = models.BooleanField()
    runs_in_school_holidays = models.BooleanField()
    runs_on_bank_holidays = models.BooleanField()
    runs_on_non_bank_holidays = models.BooleanField()
    runs_from = models.DateField()
    runs_until = models.DateField()
    
    def get_bank_holidays(self, year):
        
        def nth_dow_to_day((m, dow, n), y):
            """
            Figures out the day of the nth day-of-week in the month m and year y as an
            integer
            
            e.g., 2nd Wednesday in July 2010:
                  nth_dow_to_day((7, 3, 2), 2010)
            
            Conversion from GUTime
            https://github.com/cnorthwood/ternip/blob/master/ternip/rule_engine/normalisation_functions/date_functions.py
            """
            
            if dow == 7:
                dow = 0
            
            first_dow, num_days = monthrange(y, m) # the dow of the first of the month
            first_dow += 1
            if first_dow == 7:
                first_dow = 0
            
            shift = dow - first_dow
            if shift < 0:
                shift += 7
            
            if n == -1:
                while (shift + (7 * n) - 6) <= num_days:
                    n += 1
                n -= 1
            return date(y, m, shift + (7 * n) - 6)
        
        bank_holidays = [
            date(year, 1, 1), # New Year's Day
            easter(year) - timedelta(days=2), # Good Friday
            easter(year) + timedelta(days=1), # Easter Monday
            nth_dow_to_day((5, 1, 1), year), # May Day
            nth_dow_to_day((5, 1, -1), year) if year != 2012 else date(2012, 6, 4), # Spring Bank Holiday
            nth_dow_to_day((8, 1, -1), year), # Late Summer Bank Holiday
            date(year, 12, 25), # Christmas Day
            date(year, 12, 26), # Boxing Day
        ]
        if year == 2011:
            bank_holidays.append(date(2011, 4, 29)) # Royal Wedding
        if year == 2012:
            bank_holidays.append(date(2012, 6, 5)) # Diamond Jubilee
        
        # Now figure out if any of those are on a weekend and if so add the
        # Monday 'day in lieu' day
        for bank_holiday in bank_holidays[:]:
            if weekday(bank_holiday.year, bank_holiday.month, bank_holiday.day) == 5:
                new_date = bank_holiday + timedelta(days=2)
            elif weekday(bank_holiday.year, bank_holiday.month, bank_holiday.day) == 6:
                new_date = bank_holiday + timedelta(days=1)
            else:
                continue
            # Deal with the case of Christmas Day and Boxing Day both being on
            # a weekend
            while new_date in bank_holidays:
                new_date += timedelta(days=1)
            bank_holidays.append(new_date)
        return bank_holidays
    
    def runs_on(self, date):
        """
        Checks if the service runs on the given date
        """
        
        if date < self.runs_from:
            # Before this service starts
            return False
        
        if date > self.runs_until:
            # After this service finished
            return False
        
        if date in self.get_bank_holidays(date.year):
            # Bank holiday
            return self.runs_on_bank_holidays
        
        elif self.runs_on_non_bank_holidays:
            
            # TODO: Check for term time - fortunately this flag appears to be
            # unused in Greater Manchester. If more places release ATCO-CIF
            # dumps that do implement this, we should do this at a later date
            
            day = ['monday',
                   'tuesday',
                   'wednesday',
                   'thursday',
                   'friday',
                   'saturday',
                   'sunday'][weekday(date.year, date.month, date.day)]
            
            return getattr(self, 'runs_on_%s' % day)
        
        else:
            # Not a bank holiday, but this is a bank holiday only service
            return False
    
    vehicle = models.TextField()
    
    def __unicode__(self):
        return self.route.__unicode__()
    
    class Meta:
        verbose_name = u"路线导航"
        verbose_name_plural = u"路线导航"

class ScheduledStop(models.Model):
    """
    This is a scheduled route stop
    """
    
    entity = models.ForeignKey(Entity)
    journey = models.ForeignKey(Journey)
    
    order = models.IntegerField()
    
    sta = models.TimeField(verbose_name=_('Scheduled time of arrival'),
                           null=True, blank=True)
    
    std = models.TimeField(verbose_name=_('Scheduled time of departure'),
                           null=True, blank=True)
    
    times_estimated = models.BooleanField()
    fare_stage = models.BooleanField()
    activity = models.CharField(max_length=1, choices=(
            ('O', _('Service starts here')),
            ('B', _('Scheduled stop')),
            ('P', _('Service picks up here only')),
            ('D', _('Service does not pick up here')),
            ('N', _('Service does not stop here')),
            ('F', _('Service finishes here')),
        ), default='B')
    
    class Meta:
        ordering = ['order']
    
    def __unicode__(self):
        return self.entity.title

