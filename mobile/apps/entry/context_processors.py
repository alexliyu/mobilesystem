#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django.conf import settings


def media(request):
    """Adds media-related context variables to the context"""
    return {'BLOG_MEDIA_URL': settings.MEDIA_URL}


def version(request):
    """Adds version of blog to the context"""
    return {'LINCDM_VERSION': settings.VERSION}

def sitename(request):
    return {'LINCDM_NAME':settings.LINCDM_NAME}

def sitetitle(request):
    return {'LINCDM_TITLE':settings.LINCDM_TITLE}



    
