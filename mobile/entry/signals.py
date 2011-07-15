#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
import inspect
from functools import wraps

from django.db.models.signals import post_save

import settings
from settings import SAVE_PING_DIRECTORIES, PING_DIRECTORIES, SAVE_PING_EXTERNAL_URLS

def disable_for_loaddata(signal_handler):
    """Decorator for disabling signals sent
    by 'post_save' on loaddata command.
    http://code.djangoproject.com/ticket/8399"""

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == 'loaddata':
                return
        signal_handler(*args, **kwargs)

    return wrapper


@disable_for_loaddata
def ping_directories_handler(sender, **kwargs):
    """Ping Directories when an entry is saved"""
    entry = kwargs['instance']

    if entry.is_visible and SAVE_PING_DIRECTORIES:
        from entry.ping import DirectoryPinger

        for directory in PING_DIRECTORIES:
            DirectoryPinger(directory, [entry])


@disable_for_loaddata
def ping_external_urls_handler(sender, **kwargs):
    """Ping Externals URLS when an entry is saved"""
    entry = kwargs['instance']

    if entry.is_visible and SAVE_PING_EXTERNAL_URLS:
        from entry.ping import ExternalUrlsPinger

        ExternalUrlsPinger(entry)

def disconnect_entry_signals():
    """Disconnect all the signals provided by lincdm"""
    from entry.models import Entry

    post_save.disconnect(
        sender=Entry, dispatch_uid='entry.entry.post_save.ping_directories')
    post_save.disconnect(
        sender=Entry, dispatch_uid='entry.entry.post_save.ping_external_urls')
