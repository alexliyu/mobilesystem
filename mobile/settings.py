#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from oauth.oauth import OAuthSignatureMethod_PLAINTEXT
import os.path
from molly.conf.settings import Application, extract_installed_apps, Authentication, ExtraBase, Provider
from molly.utils.media import get_compress_groups
project_root = os.path.normpath(os.path.dirname(__file__))
molly_root = os.path.join(project_root, 'molly')
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
SITE_NAME = 'eiimedia'

# Molly can automatically generate the urlpatterns, so it's recommended by
# default to use Molly's urls.py. This doesn't work if you have non-Molly apps
# and may require a custom urls.py to be written
ROOT_URLCONF = 'mobile.urls'

# The connection to your database is configured below. We assume you're using
# PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '192.168.1.119',
        'NAME': 'molly',
        'USER': 'molly',
#        'PASSWORD': 'FSNICgM3wDvNU29XmR',
    	'PASSWORD':'6b6RyKNvOnEvbrynYK',
    }
}



# API keys are used to access particular services
API_KEYS = {
    'cloudmade': 'None',
    'google_analytics': 'None',
}


# The meat of Molly - application configuration
APPLICATIONS = [

    Application('mobile.molly.apps.home', 'home', '主页',
        display_to_user=False,
    ),
    
#    Application('mobile.molly.apps.desktop', 'desktop', '桌面',
#        display_to_user=True,
#        twitter_username='alexliyu',
#        blog_rss_url='http://feeds.feedburner.com/mobileoxford',
#    ),
    
    Application('mobile.molly.apps.podcasts', 'podcasts', '视频点播',
        providers=[        ]
        ),
    
#   Application('mobile.molly.apps.webcams', 'webcams', 'Webcams'),
    
    Application('molly.apps.weather', 'weather', '天气',
        location_id='1832',
        provider=Provider('molly.apps.weather.providers.BBCWeatherProvider',
            location_id=1832,
        ),
         display_to_user=False,
    ),
    Application('mobile.molly.apps.Lottery', 'Lottery', '中奖查询',
        providers=[        ],
         display_to_user=True,
        ),
    Application('mobile.molly.apps.service_status', 'service_status', '服务状态',
        providers=[        ],
         display_to_user=False,
        ),
    
    Application('mobile.molly.apps.search', 'search', '搜索',
        providers=[
            Provider('mobile.molly.apps.search.providers.ApplicationSearchProvider'),
        ],
        # Uncomment if you're using a query expansion file
        #query_expansion_file = os.path.join(project_root, 'data', 'query_expansion.txt'),
        display_to_user=False,
    ),
    
#    Application('mobile.molly.apps.feeds', 'feeds', 'Feeds',
#        providers=[
#            Provider('mobile.molly.apps.feeds.providers.RSSFeedsProvider'),
#        ],
#        display_to_user=True,
#    ),
    
    Application('mobile.molly.apps.feeds.news', 'news', '新闻'),
    
    Application('mobile.molly.apps.feeds.events', 'events', '公告'),
    
    Application('molly.maps', 'maps', '地图',
        display_to_user=False,
    ),
    
    Application('molly.geolocation', 'geolocation', 'Geolocation',
    
        prefer_results_near=(118.115749, 24.471363, 10000),
        providers=[
            Provider('molly.geolocation.providers.PlacesGeolocationProvider'),
        ],
        display_to_user=False,
    ),
    
    Application('mobile.molly.apps.feedback', 'feedback', '建议',
        display_to_user=False,
    ),
#    
#    Application('mobile.molly.apps.feature_vote', 'feature_vote', '活动建议',
#        display_to_user=True,
#    ),
    
#    Application('molly.external_media', 'external_media', 'External Media',
#        display_to_user=True,
#    ),
#    
    Application('molly.wurfl', 'device_detection', '终端信息',
        display_to_user=True,
        expose_view=True,
    ),
#    
#    Application('mobile.molly.apps.stats', 'stats', 'Statistics',
#         display_to_user=True,
#     ),
#    
    Application('molly.url_shortener', 'url_shortener', 'URL Shortener',
        display_to_user=False,
    ),
    
    Application('mobile.molly.apps.links', 'links', '网址导航',
        display_to_user=True,
    ),
     
    Application('molly.utils', 'utils', 'Molly utility services',
        display_to_user=True,
    ),
#    
    Application('molly.auth', 'auth', '授权',
        display_to_user=False,
        secure=True,
        unify_identifiers=('weblearn:id',),
    ),
    
    Application('mobile.molly.apps.places', 'places', '消费导航',
        providers=[
            'mobile.molly.apps.places.providers.ACISLiveMapsProvider',
            Provider('mobile.molly.apps.places.providers.OSMMapsProvider',
                     lat_north=24.671363, lat_south=24.271363,
                     lon_west=117.915749, lon_east=118.315749
            ),
        ],

    ),
    
#    Application('mobile.molly.apps.transport', 'transport', '交通',
#            train_station='crs:AYW',
#        nearby={
#            'bus_stops': ('bus-stop', 5),
#        },
#        #transit_status_provider = 'mobile.molly.apps.transport.providers.TubeStatusProvider',
#    
#        ),
    
    Application('molly.favourites', 'favourites', 'Favourite pages',
        display_to_user=False,
    ),
                
    Application('mobile.molly.apps.business', 'business', '联盟商家',
        display_to_user=True,
    ),
                
    Application('mobile.molly.apps.users', 'users', '用户中心',
        display_to_user=False,
    ),
    
    
]


# Middleware classes alter requests and responses before/after they get
# handled by the view. They're useful in providing high-level global
# functionality
MIDDLEWARE_CLASSES = (
    'mobile.molly.wurfl.middleware.WurflMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'mobile.molly.utils.middleware.ErrorHandlingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mobile.molly.auth.middleware.SecureSessionMiddleware',
    'mobile.molly.apps.stats.middleware.StatisticsMiddleware',
    'mobile.molly.url_shortener.middleware.URLShortenerMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
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
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'mobile.molly.utils.context_processors.ssl_media',
    'django.contrib.messages.context_processors.messages',
    'mobile.molly.wurfl.context_processors.wurfl_device',
    'mobile.molly.wurfl.context_processors.device_specific_media',
    'mobile.molly.geolocation.context_processors.geolocation',
    'mobile.molly.utils.context_processors.full_path',
    'mobile.molly.utils.context_processors.site_name',
    #'molly.utils.context_processors.google_analytics',
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
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
    'mobile.molly.utils.template_loaders.MollyDefaultLoader'
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
    'mobile.userena.backends.UserenaAuthenticationBackend',
    'mobile.guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    
)

# Non-Molly apps get added here (plus, tell Django about Molly apps)
INSTALLED_APPS = extract_installed_apps(APPLICATIONS) + (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'molly.batch_processing',
#    'debug_toolbar',
    'compress',
    'easy_thumbnails',
    'guardian',
    'south',
    'userena',
    'userena.contrib.umessages',
)

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
SRID = 27700

# Settings relating to staticfiles
STATIC_ROOT = os.path.join(project_root, 'static') # the location on disk where media is stored
STATIC_URL = '/static/' # The URL used to refer to media


STATICFILES_DIRS = (
    os.path.join(project_root, 'site_media'), # Custom overriding
    os.path.join(molly_root, 'media'), # Molly default media
    ('markers', MARKER_DIR), # Markers
)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
MEDIA_ROOT = os.path.join(project_root, 'media') # the location on disk where media is stored
MEDIA_URL = '/media/' # The URL used to refer to media
# Settings relating to django-compress
COMPRESS_SOURCE = MEDIA_URL
COMPRESS_ROOT = MEDIA_URL
COMPRESS_URL = MEDIA_URL
COMPRESS_MEDIA_ROOT = MEDIA_ROOT
COMPRESS_CSS, COMPRESS_JS = get_compress_groups(MEDIA_ROOT)
COMPRESS_CSS_FILTERS = ('mobile.molly.utils.compress.MollyCSSFilter',) # CSS filter is custom-written since the provided one mangles it too much
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
