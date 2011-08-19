#-*- coding:utf-8 -*-
"""
这是项目的基本配置文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050

@param DEBUG 是否开启调试模式

@param TEMPLATE_DEBUG 是否开启模板调试模式

@event event 无事件

@exception exception 无返回

@keyparam  param 无参数

@return 无返回
       
"""
from oauth.oauth import OAuthSignatureMethod_PLAINTEXT
import os.path
from conf.settings import  extract_installed_apps
from utils.media import get_compress_groups

from utils import loading
project_root = os.path.normpath(os.path.dirname(__file__))
molly_root = project_root

APPLICATIONS = loading.load_apps()

COPYRIGHT = 'e2 mobile'

"""
短信接口帐号及密码
"""
#SMS_SN = 'SDK-XJG-010-00137'
#SMS_PWD = '438483'

SMS_SN = 'SDK-XJG-010-00137'
SMS_PWD = '438483'
SMS_PROVINCE = u'福建'
SMS_CITY = u'厦门'
SMS_TRADE = u'新媒体'
SMS_ENTNAME = u'娱讯（厦门）文化传播有限公司'
SMS_LINKMAN = u'李昱'
SMS_PHONE = '05925166918'
SMS_MOBILE = '13959260801'
SMS_EMAIL = 'liy@eiimedia.cn'
SMS_FAX = '05925166755'
SMS_ADDRESS = u'厦门禾祥东路138号4楼'
SMS_POSTCODE = 361000
SMS_SIGN = u'娱讯互动平台'

gettext = lambda s: s

ADMINS = (
    ('alex', 'alexliyu2012@gmail.com'),
)

MANAGERS = ADMINS

# DEBUG mode is not recommended in production

DEBUG = True 

DEBUG_SECURE = DEBUG
TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = 'userena.UserProfile' 

LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

LANGUAGES = [
    ('zh-cn', gettext('Chinese')),
]
DEFAULT_LANGUAGE = 0
# Site name is used extensively in templates to name the site
SITE_NAME = u'娱讯互动平台'

# Molly can automatically generate the urlpatterns, so it's recommended by
# default to use Molly's urls.py. This doesn't work if you have non-Molly apps
# and may require a custom urls.py to be written
ROOT_URLCONF = 'urls'

# 
# 在公司的数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '192.168.1.34',
        'NAME': 'mobile',
        'USER': 'mobile',
        'PASSWORD': 'md5c720ea1e0f756a4a2191557aa2c038ba',
    }
}


# 在家里的数据库配置
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        'HOST': '127.0.0.1',
#        'NAME': 'molly',
#        'USER': 'molly',
#        'PASSWORD': 'mobile',
#        'PASSWORD':'6b6RyKNvOnEvbrynYK',
#    }
#}


# API keys are used to access particular services
API_KEYS = {
    'cloudmade': 'None',
    'google_analytics': 'None',
}

TIME_ZONE = 'Asia/Shanghai'
# The meat of Molly - application configuration

GEOIP_PATH = os.path.join(project_root, 'geodata')
GEOIP_CITY = os.path.join(GEOIP_PATH, 'GeoLiteCity.dat')

# Middleware classes alter requests and responses before/after they get
# handled by the view. They're useful in providing high-level global
# functionality
MIDDLEWARE_CLASSES = (
    'wurfl.middleware.WurflMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'utils.middleware.ErrorHandlingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'auth.middleware.SecureSessionMiddleware',
    'apps.stats.middleware.StatisticsMiddleware',
    'url_shortener.middleware.URLShortenerMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'onlineuser.middleware.OnlineUserMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# is available in the context of a view
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'utils.context_processors.ssl_media',
    'django.contrib.messages.context_processors.messages',
    'wurfl.context_processors.wurfl_device',
    'wurfl.context_processors.device_specific_media',
    'geolocation.context_processors.geolocation', # This adds the current known location of the user to the context
    'utils.context_processors.full_path',
    'utils.context_processors.site_name',
    #'utils.context_processors.google_analytics',
    'django.core.context_processors.csrf',
    'djangohelper.context_processors.ctx_config',
)

# This setting defines where Django looks for templates when searching - it
# assumes your overriding templates are defined in '/your/project/templates'
# and you want to have the Molly defaults as a fallback
TEMPLATE_DIRS = (
    os.path.join(project_root, 'templates'),
    os.path.join(molly_root, 'templates'),
)

# This setting changes how Django searches for templates when rendering. The
# default is fine
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.load_template_source',
    'utils.template_loaders.MollyDefaultLoader'
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    #'compressor.finders.CompressorFinder',
)
INTERNAL_IPS = ('127.0.0.1',)


DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    
)

# Non-Molly apps get added here (plus, tell Django about Molly apps)
INSTALLED_APPS = extract_installed_apps(APPLICATIONS) + (
    'grappelli.dashboard',
    'grappelli',
    'filebrowser',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'mobile',
    'batch_processing',
    'django.contrib.gis',
    'actstream',
    'simpleavatar',
    'djangohelper',
    'onlineuser',
    'attachments',
    
#    'debug_toolbar',
    'tinymce',
    'compress',
    'pagination',
    'guardian',
    'south',
    'userena',
    'tagging',
    'userena.contrib.umessages',
     'sentry',
    'sentry.client',
    'sorl.thumbnail',
    'tracking',
)

GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

import logging
from sentry.client.handlers import SentryHandler

logger = logging.getLogger()
# ensure we havent already registered the handler
if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
    logger.addHandler(SentryHandler())

    # Add StreamHandler to sentry's default so you can catch missed exceptions
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
#            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}    
# Userena settings
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'


USERENA_DISABLE_PROFILE_LIST = False
USERENA_MUGSHOT_SIZE = 140
USERENA_WITH_MOBILE = True
# Guardian
ANONYMOUS_USER_ID = -1

MEDIA_ROOT = os.path.join(project_root, 'media') # the location on disk where media is stored
UPLOADS_ROOT = os.path.join(os.path.abspath(MEDIA_ROOT), 'uploads/images') #上传文件路径
MEDIA_URL = '/media/' # The URL used to refer to media

# The CACHE_DIR is used by default to store cached map tiles, generated static
# maps, markers, external images, etc
CACHE_DIR = os.path.join(MEDIA_ROOT, 'cache')
# Defines where markers get generated
MARKER_DIR = os.path.join(CACHE_DIR, 'markers')

# This shouldn't need changing
SRID = 3857

GMAP_JQUERY = 'http://code.jquery.com/jquery-1.4.2.min.js'
GMAP_API = 'http://maps.google.com/maps/api/js?sensor=false'
GMAP_DEFAULT = [-34.397, 150.644]
# Settings relating to staticfiles
STATIC_ROOT = os.path.join(project_root, 'static') # the location on disk where media is stored
STATIC_URL = '/static/' # The URL used to refer to media


STATICFILES_DIRS = (
    os.path.join(project_root, 'site_media'), # Custom overriding
    os.path.join(molly_root, 'media'), # Molly default media
    ('markers', MARKER_DIR), # Markers
)


TINYMCE_JS_URL = 'http://debug.example.org/tiny_mce/tiny_mce_src.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False



ADMIN_MEDIA_PREFIX = MEDIA_URL + "grappelli/"
GRAPPELLI_ADMIN_TITLE = u"娱讯互动平台管理系统"

TRACKING_USE_GEOIP = False

# Settings relating to django-compress
COMPRESS_SOURCE = MEDIA_URL
COMPRESS_ROOT = MEDIA_URL
COMPRESS_URL = MEDIA_URL
COMPRESS_MEDIA_ROOT = MEDIA_ROOT
COMPRESS_CSS, COMPRESS_JS = get_compress_groups(MEDIA_ROOT)
COMPRESS_CSS_FILTERS = ('utils.compress.MollyCSSFilter',) # CSS filter is custom-written since the provided one mangles it too much
COMPRESS_CSSTIDY_SETTINGS = {
    'remove_bslash': True, # default True
    'compress_colors': True, # default True
    'compress_font-weight': True, # default True
    'lowercase_s': False, # default False
    'optimise_shorthands': 0, # default 2, tries to merge bg rules together and makes a hash of things
    'remove_last_': False, # default False
    'case_properties': 1, # default 1
    'sort_properties': False, # default False
    'sort_selectors': False, # default False
    'merge_selectors': 0, # default 2, messes things up
    'discard_invalid_properties': False, # default False
    'css_level': 'CSS2.1', # default 'CSS2.1'
    'preserve_css': False, # default False
    'timestamp': False, # default False
    'template': 'high_compression', # default 'highest_compression'
}
COMPRESS_JS_FILTERS = ('compress.filters.jsmin.JSMinFilter',)
#COMPRESS = DEBUG     # Only enable on production (to help debugging)
COMPRESS = False
COMPRESS_VERSION = True  # Add a version number to compressed files.


MARKUP_LANGUAGE = 'html'

ENTRY_TEMPLATES = []
ENTRY_BASE_MODEL = ''
MARKDOWN_EXTENSIONS = ''

AUTO_CLOSE_COMMENTS_AFTER = None

URL_SHORTENER_BACKEND = 'entry.url_shortener.backends.default'

PROTOCOL = 'http'

MAIL_COMMENT_REPLY = False
MAIL_COMMENT_AUTHORS = True
AUTO_MODERATE_COMMENTS = False
SPAM_CHECKER_BACKENDS = ()
WYSIWYG = 'wymeditor'

PING_DIRECTORIES = ('http://www.33445120.tk/xmlrpc/',)
SAVE_PING_DIRECTORIES = bool(PING_DIRECTORIES)
SAVE_PING_EXTERNAL_URLS = True
MAIL_COMMENT_NOTIFICATION_RECIPIENTS = ''
PAGINATION = 10
ALLOW_EMPTY = True
ALLOW_FUTURE = True

ENTRY_TEMPLATES = []

MARKUP_LANGUAGE = 'html'

PROTOCOL = 'http'


FEEDS_FORMAT = 'rss'
FEEDS_MAX_ITEMS = 15

PINGBACK_CONTENT_LENGTH = 300

F_MIN = 0.1
F_MAX = 1.0
STOP_WORDS = ('able', 'about', 'across', 'after', 'all', 'almost',
                      'also', 'among', 'and', 'any', 'are', 'because', 'been',
                      'but', 'can', 'cannot', 'could', 'dear', 'did', 'does',
                      'either', 'else', 'ever', 'every', 'for', 'from', 'get',
                      'got', 'had', 'has', 'have', 'her', 'hers', 'him', 'his',
                      'how', 'however', 'into', 'its', 'just', 'least', 'let',
                      'like', 'likely', 'may', 'might', 'most', 'must',
                      'neither', 'nor', 'not', 'off', 'often', 'only', 'other',
                      'our', 'own', 'rather', 'said', 'say', 'says', 'she',
                      'should', 'since', 'some', 'than', 'that', 'the',
                      'their', 'them', 'then', 'there', 'these', 'they',
                      'this', 'tis', 'too', 'twas', 'wants', 'was', 'were',
                      'what', 'when', 'where', 'which', 'while', 'who', 'whom',
                      'why', 'will', 'with', 'would', 'yet', 'you', 'your')

# URL prefix for forum media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".    
FORUM_MEDIA_PREFIX = '%sforum/' % MEDIA_URL
    
#The URL where requests are redirected after login
LOGIN_REDIRECT_URL = '/'
#The URL where requests are redirected for login
LOGIN_URL = "/accounts/signin/"
#LOGIN_URL counterpart
LOGOUT_URL = "/accounts/signout/"
#register url 
REGISTER_URL = '/accounts/signup/'

CTX_CONFIG = {
            'FORUM_TITLE': u'娱讯互动社区',
            'FORUM_SUB_TITLE': u'厦门同城社区、本地交友、团购、娱乐',
            'FORUM_PAGE_SIZE': 50,
            'TOPIC_PAGE_SIZE': 20,
    
            'FORUM_MEDIA_PREFIX': FORUM_MEDIA_PREFIX,
            'LOGIN_URL': LOGIN_URL,
            'LOGOUT_URL': LOGOUT_URL,
            'REGISTER_URL': REGISTER_URL,
            }
BBCODE_AUTO_URLS = True
#add allow tags
HTML_SAFE_TAGS = ['embed']
HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
#add forbid tags
HTML_UNSAFE_TAGS = []
HTML_UNSAFE_ATTRS = []
    
