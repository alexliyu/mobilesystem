#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
本文件创建于 2011-7-16

@author 李昱  Email:alexliyu2012@gmail.com QQ:939567050

————————————————————————————
创建于 2011-1-30.

用来从APPS目录下自动加载模块，并安装

'''
import os, re


from conf.settings import Application, extract_installed_apps, Authentication, ExtraBase, Provider

REMOVELIST = ['places', 'desktop', 'feeds', 'library', 'contact']
APPLICATIONS = [
    
    Application('apps.feeds', 'feeds', 'Feeds',
        providers=[
            Provider('apps.feeds.providers.RSSFeedsProvider'),
            Provider('apps.feeds.providers.MeituanFeedsProvider'),
        ],
        display_to_user=False,
    ),
    
    Application('apps.feeds.tuan', 'tuan', '团购'),
    
    
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

    Application('external_media', 'external_media', 'External Media',
        display_to_user=False,
    ),
    
    Application('wurfl', 'device_detection', '终端信息',
        display_to_user=False,
        expose_view=True,
    ),

    Application('url_shortener', 'url_shortener', 'URL Shortener',
        display_to_user=False,
    ),

#     
    Application('baseutils', 'baseutils', 'E2-Mobile utility services',
        display_to_user=True,
    ),
#    Application('auth', 'auth', '授权',
#        display_to_user=False,
#        secure=True,
#        unify_identifiers=('weblearn:id',),
#    ),
#    
    Application('apps.places', 'places', '消费导航',
        providers=[
            Provider('apps.places.providers.OSMMapsProvider',
                     lat_north=24.671363, lat_south=24.271363,
                     lon_west=117.915749, lon_east=118.315749
            ),
        ],

    ),
    
   
]
def load_apps():
    """
    自动加载模块，并完成配置
    @return 返回配置好的APPLICATIONS列表
    """
    all_apps = [f for f in os.listdir(os.path.join(os.path.dirname(__file__).rstrip('baseutils'), 'apps')) if not f.endswith(".py") or f.endswith(".pyc")]
    try:
        all_apps.remove('__init__.pyc')
        all_apps.remove('.svn')
    except:
        pass
    for f in REMOVELIST:
        all_apps.remove(f)

    for app in all_apps:
        try:
            config = __import__('apps.' + app + '.__init__', fromlist='Mete').Mete
            appconfig = Application('apps.%s' % app, app, config.title, **config.config)
            APPLICATIONS.append(appconfig)
        except Exception, e:     
            print app + str(e)
    return APPLICATIONS
    
def get_config(config):
    if config.has_key('providers'):
        if len(config['providers']) > 0:
            providers = []
            for provider in config['providers']:
                providers.append(Provider(provider))
                
            config['providers'] = providers
            
    return config
    
    
