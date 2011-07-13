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
from conf.settings import Application, extract_installed_apps, Authentication, ExtraBase, Provider
from utils.media import get_compress_groups
project_root = os.path.normpath(os.path.dirname(__file__))
molly_root = project_root
gettext = lambda s: s

ADMINS = (
    ('alex', 'alexliyu2012@gmail.com'),
)

MANAGERS = ADMINS

# DEBUG mode is not recommended in production

DEBUG = True 

DEBUG_SECURE = DEBUG
TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = 'users.UserProfile' 

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
SITE_NAME = u'娱讯手机门户'

# Molly can automatically generate the urlpatterns, so it's recommended by
# default to use Molly's urls.py. This doesn't work if you have non-Molly apps
# and may require a custom urls.py to be written
ROOT_URLCONF = 'urls'

# 
# 在公司的数据库配置
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        'HOST': '192.168.1.34',
#        'NAME': 'mobile',
#        'USER': 'mobile',
#        'PASSWORD': 'md5c720ea1e0f756a4a2191557aa2c038ba',
#    }
#}


# 在家里的数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '127.0.0.1',
        'NAME': 'molly',
        'USER': 'molly',
        #'PASSWORD': 'mobile',
        'PASSWORD':'6b6RyKNvOnEvbrynYK',
    }
}


# API keys are used to access particular services
API_KEYS = {
    'cloudmade': 'None',
    'google_analytics': 'None',
}

TIME_ZONE = 'Asia/Shanghai'
# The meat of Molly - application configuration
APPLICATIONS = [

    Application('apps.home', 'home', '主页',
        display_to_user=False,
    ),
    
#    Application('apps.desktop', 'desktop', '桌面',
#        display_to_user=True,
#        twitter_username='alexliyu',
#        blog_rss_url='http://feeds.feedburner.com/mobileoxford',
#    ),
    
    Application('apps.podcasts', 'podcasts', '视频点播',
        providers=[        ]
        ),
    
#   Application('apps.webcams', 'webcams', 'Webcams'),
    
    Application('apps.weather', 'weather', '天气',
        location_id='1832',
         display_to_user=False,
    ),
    Application('apps.lottery', 'lottery', '中奖查询',
        providers=[        ],
         display_to_user=True,
        ),
    Application('apps.service_status', 'service_status', '服务状态',
        providers=[        ],
         display_to_user=False,
        ),
    
    Application('apps.search', 'search', '搜索',
        providers=[
            Provider('apps.search.providers.ApplicationSearchProvider'),
        ],
        # Uncomment if you're using a query expansion file
        #query_expansion_file = os.path.join(project_root, 'data', 'query_expansion.txt'),
        display_to_user=False,
    ),
    
    Application('apps.feeds', 'feeds', 'Feeds',
        providers=[
            Provider('apps.feeds.providers.RSSFeedsProvider'),
        ],
        display_to_user=False,
    ),
    
    Application('apps.feeds.news', 'news', '团购'),
    
    Application('apps.feeds.events', 'events', '公告'),
    
    Application('maps', 'maps', '地图',
        display_to_user=False,
    ),
    
    Application('geolocation', 'geolocation', 'Geolocation',
    
        prefer_results_near=(118.115749, 24.471363, 10000),
        providers=[
            Provider('geolocation.providers.PlacesGeolocationProvider'),
            Provider('geolocation.providers.CloudmadeGeolocationProvider',),
        ],
        display_to_user=False,
    ),
    
    Application('apps.feedback', 'feedback', '建议',
        display_to_user=False,
    ),
#    
#    Application('apps.feature_vote', 'feature_vote', '活动建议',
#        display_to_user=True,
#    ),
    
    Application('external_media', 'external_media', 'External Media',
        display_to_user=False,
    ),
    
    Application('wurfl', 'device_detection', '终端信息',
        display_to_user=False,
        expose_view=True,
    ),
#    
#    Application('apps.stats', 'stats', 'Statistics',
#         display_to_user=True,
#     ),
#    
    Application('url_shortener', 'url_shortener', 'URL Shortener',
        display_to_user=False,
    ),
    
    Application('apps.links', 'links', '网址导航',
        display_to_user=True,
    ),
     
    Application('utils', 'utils', 'Molly utility services',
        display_to_user=True,
    ),
    Application('auth', 'auth', '授权',
        display_to_user=False,
        secure=True,
        unify_identifiers=('weblearn:id',),
    ),
    
    Application('apps.places', 'places', '消费导航',
        providers=[
            Provider('apps.places.providers.OSMMapsProvider',
                     lat_north=24.671363, lat_south=24.271363,
                     lon_west=117.915749, lon_east=118.315749
            ),
        ],

    ),
    
    Application('favourites', 'favourites', 'Favourite pages',
        display_to_user=False,
    ),
                
    Application('apps.business', 'business', '联盟商家',
        display_to_user=True,
    ),
                
    Application('apps.users', 'users', '用户中心',
        display_to_user=False,
    ),
    
    
]


# Middleware classes alter requests and responses before/after they get
# handled by the view. They're useful in providing high-level global
# functionality
MIDDLEWARE_CLASSES = (
    'wurfl.middleware.WurflMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'utils.middleware.ErrorHandlingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'auth.middleware.SecureSessionMiddleware',
    'apps.stats.middleware.StatisticsMiddleware',
    'url_shortener.middleware.URLShortenerMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Each entity has a primary identifier which is used to generate the absolute
# URL of the entity page. We can define a list of identifier preferences, so
# that when an entity is imported, these identifier namespaces are looked at in
# order until a value in that namespace is chosen. This is then used as the
# primary identifer.
#IDENTIFIER_SCHEME_PREFERENCE = ('atco', 'osm', 'naptan', 'postcode', 'bbc-tpeg')

# This setting defines which context processors are used - this can affect what
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
    'batch_processing',
    'django.contrib.gis',
#    'debug_toolbar',
    'tinymce',
    'compress',
    'easy_thumbnails',
    'guardian',
    'south',
    'userena',
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

# The CACHE_DIR is used by default to store cached map tiles, generated static
# maps, markers, external images, etc
CACHE_DIR = os.path.join(project_root, 'cache')
# Defines where markers get generated
MARKER_DIR = os.path.join(CACHE_DIR, 'markers')

# This shouldn't need changing
SRID = 3857

GMAP_JQUERY = 'http://code.jquery.com/jquery-1.4.2.min.js'
GMAP_API = 'http: // maps.google.com / maps / api / js?sensor = false'
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


MEDIA_ROOT = os.path.join(project_root, 'media') # the location on disk where media is stored
UPLOADS_ROOT = os.path.join(os.path.abspath(MEDIA_ROOT), 'uploads/images') #上传文件路径
MEDIA_URL = '/media/' # The URL used to refer to media
ADMIN_MEDIA_PREFIX = MEDIA_URL + "grappelli/"
GRAPPELLI_ADMIN_TITLE = u"娱讯手机门户管理平台"

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
