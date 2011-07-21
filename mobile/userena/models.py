#-*- coding:utf-8 -*-
'''
项目的用户模型文件

Created on 2011-1-30

@author: 李昱
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured

from userena.utils import get_gravatar, generate_sha1, get_protocol
from userena.managers import UserenaManager, UserenaBaseProfileManager
from userena import settings as userena_settings

from guardian.shortcuts import get_perms
from guardian.shortcuts import assign

from easy_thumbnails.fields import ThumbnailerImageField
from django.utils import timesince, html
from mobile.utils import formatter, function
import PIL
import datetime, random

PROFILE_PERMISSIONS = (
            ('view_profile', 'Can view profile'),
)

def upload_to_mugshot(instance, filename):
    """
    Uploads a mugshot for a user to the ``USERENA_MUGSHOT_PATH`` and saving it
    under unique hash for the image. This is for privacy reasons so others
    can't just browse through the mugshot directory.

    """
    extension = filename.split('.')[-1].lower()
    salt, hash = generate_sha1(instance.id)
    return '%(path)s%(hash)s.%(extension)s' % {'path': userena_settings.USERENA_MUGSHOT_PATH,
                                               'hash': hash[:10],
                                               'extension': extension}

class UserenaSignup(models.Model):
    """
    Userena model which stores all the necessary information to have a full
    functional user implementation on your Django website.

    """
    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                related_name='userena_signup')


    last_active = models.DateTimeField(_('last active'),
                                       blank=True,
                                       null=True,
                                       help_text=_('The last date that the user was active.'))

    activation_key = models.CharField(_('activation key'),
                                      max_length=40,
                                      blank=True)

    activation_notification_send = models.BooleanField(_('notification send'),
                                                       default=False,
                                                       help_text=_('Designates whether this user has already got a notification about activating their account.'))

    email_unconfirmed = models.EmailField(_('unconfirmed email address'),
                                          blank=True,
                                          help_text=_('Temporary email address when the user requests an email change.'))

    email_confirmation_key = models.CharField(_('unconfirmed email verification key'),
                                              max_length=40,
                                              blank=True)

    email_confirmation_key_created = models.DateTimeField(_('creation date of email confirmation key'),
                                                          blank=True,
                                                          null=True)


    objects = UserenaManager()

    class Meta:
        verbose_name = _('userena registration')
        verbose_name_plural = _('userena registrations')

    def __unicode__(self):
        return '%s' % self.user.username

    def change_email(self, email):
        """
        Changes the email address for a user.

        A user needs to verify this new email address before it becomes
        active. By storing the new email address in a temporary field --
        ``temporary_email`` -- we are able to set this email address after the
        user has verified it by clicking on the verification URI in the email.
        This email gets send out by ``send_verification_email``.

        :param email:
            The new email address that the user wants to use.

        """
        self.email_unconfirmed = email

        salt, hash = generate_sha1(self.user.username)
        self.email_confirmation_key = hash
        self.email_confirmation_key_created = datetime.datetime.now()
        self.save()

        # Send email for activation
        self.send_confirmation_email()

    def send_confirmation_email(self):
        """
        Sends an email to confirm the new email address.

        This method sends out two emails. One to the new email address that
        contains the ``email_confirmation_key`` which is used to verify this
        this email address with :func:`UserenaUser.objects.confirm_email`.

        The other email is to the old email address to let the user know that
        a request is made to change this email address.

        """
        context = {'user': self.user,
                  'new_email': self.email_unconfirmed,
                  'protocol': get_protocol(),
                  'confirmation_key': self.email_confirmation_key,
                  'site': Site.objects.get_current()}


        # Email to the old address
        subject_old = render_to_string('userena/emails/confirmation_email_subject_old.txt',
                                       context)
        subject_old = ''.join(subject_old.splitlines())

        message_old = render_to_string('userena/emails/confirmation_email_message_old.txt',
                                       context)

        send_mail(subject_old,
                  message_old,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email])

        # Email to the new address
        subject_new = render_to_string('userena/emails/confirmation_email_subject_new.txt',
                                       context)
        subject_new = ''.join(subject_new.splitlines())

        message_new = render_to_string('userena/emails/confirmation_email_message_new.txt',
                                       context)

        send_mail(subject_new,
                  message_new,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.email_unconfirmed, ])

    def activation_key_expired(self):
        """
        Checks if activation key is expired.

        Returns ``True`` when the ``activation_key`` of the user is expired and
        ``False`` if the key is still valid.

        The key is expired when it's set to the value defined in
        ``USERENA_ACTIVATED`` or ``activation_key_created`` is beyond the
        amount of days defined in ``USERENA_ACTIVATION_DAYS``.

        """
        expiration_days = datetime.timedelta(days=userena_settings.USERENA_ACTIVATION_DAYS)
        expiration_date = self.user.date_joined + expiration_days
        if self.activation_key == userena_settings.USERENA_ACTIVATED:
            return True
        if datetime.datetime.now() >= expiration_date:
            return True
        return False

    def send_activation_email(self):
        """
        Sends a activation email to the user.

        This email is send when the user wants to activate their newly created
        user.

        """
        context = {'user': self.user,
                  'protocol': get_protocol(),
                  'activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
                  'activation_key': self.activation_key,
                  'site': Site.objects.get_current()}

        subject = render_to_string('userena/emails/activation_email_subject.txt',
                                   context)
        subject = ''.join(subject.splitlines())

        message = render_to_string('userena/emails/activation_email_message.txt',
                                   context)
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email, ])

class UserenaBaseProfile(models.Model):
    """ Base model needed for extra profile functionality """
    PRIVACY_CHOICES = (
        ('open', _('Open')),
        ('registered', _('Registered')),
        ('closed', _('Closed')),
    )

    MUGSHOT_SETTINGS = {'size': (userena_settings.USERENA_MUGSHOT_SIZE,
                                 userena_settings.USERENA_MUGSHOT_SIZE),
                        'crop': 'smart'}

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

    mugshot = ThumbnailerImageField(_('mugshot'),
                                    blank=True,
                                    upload_to=upload_to_mugshot,
                                    resize_source=MUGSHOT_SETTINGS,
                                    help_text=_('A personal image displayed in your profile.'))

    privacy = models.CharField(_('privacy'),
                               max_length=15,
                               choices=PRIVACY_CHOICES,
                               default=userena_settings.USERENA_DEFAULT_PRIVACY,
                               help_text=_('Designates who can view your profile.'))

    objects = UserenaBaseProfileManager()


    class Meta:
        """
        Meta options making the model abstract and defining permissions.

        The model is ``abstract`` because it only supplies basic functionality
        to a more custom defined model that extends it. This way there is not
        another join needed.

        We also define custom permissions because we don't know how the model
        that extends this one is going to be called. So we don't know what
        permissions to check. For ex. if the user defines a profile model that
        is called ``MyProfile``, than the permissions would be
        ``add_myprofile`` etc. We want to be able to always check
        ``add_profile``, ``change_profile`` etc.

        """
        abstract = True
        permissions = PROFILE_PERMISSIONS

    def __unicode__(self):
        return 'Profile of %(username)s' % {'username': self.user.username}

    def get_mugshot_url(self):
        """
        Returns the image containing the mugshot for the user.

        The mugshot can be a uploaded image or a Gravatar.

        Gravatar functionality will only be used when
        ``USERENA_MUGSHOT_GRAVATAR`` is set to ``True``.

        :return:
            ``None`` when Gravatar is not used and no default image is supplied
            by ``USERENA_MUGSHOT_DEFAULT``.

        """
        # First check for a mugshot and if any return that.
        if self.mugshot:
            return self.mugshot.url

        # Use Gravatar if the user wants to.
        if userena_settings.USERENA_MUGSHOT_GRAVATAR:
            return get_gravatar(self.user.email,
                                userena_settings.USERENA_MUGSHOT_SIZE,
                                userena_settings.USERENA_MUGSHOT_DEFAULT)

        # Gravatar not used, check for a default image.
        else:
            if userena_settings.USERENA_MUGSHOT_DEFAULT not in ['404', 'mm',
                                                                'identicon',
                                                                'monsterid',
                                                                'wavatar']:
                return userena_settings.USERENA_MUGSHOT_DEFAULT
            else: return None

    def get_full_name_or_username(self):
        """
        Returns the full name of the user, or if none is supplied will return
        the username.

        Also looks at ``USERENA_WITHOUT_USERNAMES`` settings to define if it
        should return the username or email address when the full name is not
        supplied.

        :return:
            ``String`` containing the full name of the user. If no name is
            supplied it will return the username or email address depending on
            the ``USERENA_WITHOUT_USERNAMES`` setting.

        """
        user = self.user
        if user.first_name or user.last_name:
            # We will return this as translated string. Maybe there are some
            # countries that first display the last name.
            name = _("%(first_name)s %(last_name)s") % \
                {'first_name': user.first_name,
                 'last_name': user.last_name}
        else:
            # Fallback to the username if usernames are used
            if not userena_settings.USERENA_WITHOUT_USERNAMES:
                name = "%(username)s" % {'username': user.username}
            else:
                name = "%(email)s" % {'email': user.email}
        return name.strip()

    def can_view_profile(self, user):
        """
        Can the :class:`User` view this profile?

        Returns a boolean if a user has the rights to view the profile of this
        user.

        Users are divided into four groups:

            ``Open``
                Everyone can view your profile

            ``Closed``
                Nobody can view your profile.

            ``Registered``
                Users that are registered on the website and signed
                in only.

            ``Admin``
                Special cases like superadmin and the owner of the profile.

        Through the ``privacy`` field a owner of an profile can define what
        they want to show to whom.

        :param user:
            A Django :class:`User` instance.

        """
        # Simple cases first, we don't want to waste CPU and DB hits.
        # Everyone.
        if self.privacy == 'open': return True
        # Registered users.
        elif self.privacy == 'registered' and isinstance(user, User):
            return True

        # Checks done by guardian for owner and admins.
        elif 'view_profile' in get_perms(user, self):
            return True

        # Fallback to closed profile.
        return False

class UserenaLanguageBaseProfile(UserenaBaseProfile):
    """
    Extends the :class:`UserenaBaseProfile` with a language choice.

    Use this model in combination with ``UserenaLocaleMiddleware`` automatically
    set the language of users when they are signed in.

    """
    language = models.CharField(_('language'),
                                max_length=4,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE[:2])

    class Meta:
        abstract = True
        permissions = PROFILE_PERMISSIONS

# Area Model
class Area(models.Model):
    TYPE_CHOISES = (
        (0, '国家'),
        (1, '省'),
        (2, '市'),
        (3, '区县'),
    )
    name = models.CharField('地名', max_length=100)
    code = models.CharField('代码', max_length=255)
    type = models.IntegerField('类型', choices=TYPE_CHOISES)
    parent = models.IntegerField('父级编号(关联自已)')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = u'所在地'
        verbose_name_plural = u'所在地'
        
class UserProfile(UserenaBaseProfile):
    GENDER_CHOICES = (
                                    ('M', '男'),
                                    ('F', '女'),
                                    )
    #user = models.ForeignKey(User, unique=True, verbose_name=u'用户')
    birthday = models.DateField(u'用户生日')
    mac = models.CharField(u'用户mac地址', max_length=30, blank=True)
    mobile = models.CharField(u'移动电话', max_length=20, blank=True, null=True)
    address = models.CharField(u'家庭地址', max_length=100, blank=True, null=True)
    website = models.URLField(u'个人主页', blank=True, null=True)
    birthday = models.DateField(u'出生日期', blank=True, null=True)
    gender = models.CharField(u'性别', max_length=1, choices=GENDER_CHOICES, default='M')
    blog = models.URLField(u'个人主页', blank=True, null=True)
    QQ = models.CharField('QQ', max_length=50, blank=True, null=True)
    MSN = models.CharField(max_length=50, blank=True, null=True)
    IM = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(u'目前所在地', max_length=200, blank=True, null=True)
    area = models.ForeignKey(Area, verbose_name='地区')
    about = models.TextField('关于我', max_length=1000, default='', blank=True)
    friend = models.ManyToManyField("self", verbose_name='朋友')
    
    
    class Meta:
        verbose_name = u"用户信息列表"
        verbose_name_plural = u"用户信息列表"
    
    def __unicode__(self):
        return self.mobile
    def replacestr(self):
        return "%s****%s" % (self.__str__()[0:3], self.__str__()[7:11])

# category model
class Category(models.Model):
    name = models.CharField('名称', max_length=20)
    
    def __unicode__(self):
        return self.name
    
    def save(self, **kwags):
        self.name = self.name[0:20]
        return super(Category, self).save()        
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        

# Note model
class Note(models.Model):
    
    id = models.AutoField(
        primary_key=True
    )
    message = models.TextField('消息')
    addtime = models.DateTimeField('发布时间', auto_now=True)
    category = models.ForeignKey(Category, verbose_name='来源')
    user = models.ForeignKey(User, verbose_name='发布者')
    
    def __unicode__(self):
        return self.message
    
    def message_short(self):
        return formatter.substr(self.message, 30)

    def addtime_format_admin(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')
        
    def category_name(self):
        return self.category.name
    
    def user_name(self):
        return self.user.realname

    def save(self, force_insert=True):
        self.message = formatter.content_tiny_url(self.message)
        self.message = html.escape(self.message)
        self.message = formatter.substr(self.message, 140)
        super(Note, self).save()
    
    class Meta:
        verbose_name = u'消息'
        verbose_name_plural = u'消息'
    
    def get_absolute_url(self):
        return  '/message/%s/' % self.id
