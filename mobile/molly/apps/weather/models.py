#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from datetime import datetime, time
from django.db import models
from mobile.molly.gmapsfield.fields import GoogleMapsField


PRESSURE_STATE_CHOICES = (
    ('+', u'上升'),
    ('-', u'下降'),
    ('~', u'持续'),
    ('c', u'无变化'),
)

VISIBILITY_CHOICES = (
    ('vp', u'能见度很差'),
    ('p', u'能见度差'),
    ('vg', u'能见度很好'),
    ('g', u'能见度好'),
    ('df', u'浓雾'),
    ('f', u'雾'),
    ('e', u'能见度最好'),
    ('m', u'能见度中等'),
)

OUTLOOK_CHOICES = (
    ('si', u'晴有时多云'),
    ('gc', u'多云'),
    ('hr', u'大雨'),
    ('s', u'晴'),
    ('lr', u'小雨'),
    ('pc', u'局部多云'),
    ('f', u'雾'),
    ('wc', u'白云'),
    ('tst', u'暴风雨'),
    ('m', u'薄雾'),
    ('tsh', u'雷阵雨'),
    ('lrs', u'小阵雨'),
    ('cs', u'晴天'),
    ('d', u'毛毛雨'),
    ('h', u'冰雹'),
    ('lsn', u'小雪'),
    ('sn', u'雪'),
    ('hsn', u'大雪'),
    ('unk', u'n/a'),
)

OUTLOOK_TO_ICON = {
    'si':  'cloudy2',
    'gc':  'overcast',
    'hr':  'shower3',
    's':   'sunny',
    'lr':  'light_rain',
    'pc':  'cloudy3%(night)s',
    'f':   'fog%(night)s',
    'wc':  'cloudy5',
    'tst': 'tstorm1',
    'm':   'mist%(night)s',
    'tsh': 'tstorm3',
    'lrs': 'shower2%(night)s',
    'cs':  'sunny%(night)s',
    'd':   'shower1%(night)s',
    'h':   'hail',
    'lsn': 'snow1%(night)s',
    'sn':  'snow3%(night)s',
    'hsn': 'snow5',
    'unk': 'dunno',
}

SCALE_CHOICES = (
    ('l', u'低'),
    ('m', u'中'),
    ('h', u'高'),
)

class Weather(models.Model):
    location_id = models.CharField(max_length=16)

    name = models.TextField(null=True)

    outlook = models.CharField(null=True, max_length=3, choices=OUTLOOK_CHOICES)

    published_date = models.DateTimeField(null=True)
    observed_date = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(auto_now=True)

    temperature = models.IntegerField(null=True)
    wind_direction = models.CharField(null=True, max_length=3)
    wind_speed = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    pressure = models.PositiveIntegerField(null=True)
    pressure_state = models.CharField(null=True, max_length=1, choices=PRESSURE_STATE_CHOICES)
    visibility = models.CharField(null=True, max_length=2, choices=VISIBILITY_CHOICES)

    location = GoogleMapsField()

    min_temperature = models.IntegerField(null=True)
    max_temperature = models.IntegerField(null=True)
    uv_risk = models.CharField(max_length=1, choices=SCALE_CHOICES, null=True)
    pollution = models.CharField(max_length=1, choices=SCALE_CHOICES, null=True)
    sunset = models.TimeField(null=True)
    sunrise = models.TimeField(null=True)

    def icon(self):
        now = datetime.now().time()
        if now > time(7) or now > time(21):
            night = '_night'
        else:
            night = ''
        return OUTLOOK_TO_ICON.get(self.outlook, 'dunno') % {'night':night}

