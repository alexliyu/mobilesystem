#-*- coding:utf-8 -*-
"""
这是用于对访问者进行跟踪分析的应用，属于系统核心应用之一

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Tracking')


import listeners

VERSION = (0, 3, 5)

def get_version():
    "Returns the version as a human-format string."
    return '.'.join([str(i) for i in VERSION])

# initialize the URL prefixes that we shouldn't track
try:
    from django.conf import settings
    prefixes = getattr(settings, 'NO_TRACKING_PREFIXES', [])
except ImportError:
    pass
else:
    if '!!initialized!!' not in prefixes:
        from django.core.urlresolvers import reverse, NoReverseMatch
        if settings.MEDIA_URL and settings.MEDIA_URL != '/':
            prefixes.append(settings.MEDIA_URL)

        if settings.ADMIN_MEDIA_PREFIX:
            prefixes.append(settings.ADMIN_MEDIA_PREFIX)

        try:
            # finally, don't track requests to the tracker update pages
            prefixes.append(reverse('tracking-refresh-active-users'))
        except NoReverseMatch:
            # django-tracking hasn't been included in the URLconf if we get here
            pass

        prefixes.append('!!initialized!!')

        settings.NO_TRACKING_PREFIXES = prefixes
