#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''



XMLRPC_PINGBACK = [
    ('entry.xmlrpc.pingback.pingback_ping',
     'pingback.ping'),
    ('entry.xmlrpc.pingback.pingback_extensions_get_pingbacks',
     'pingback.extensions.getPingbacks')]

XMLRPC_METAWEBLOG = [
    ('entry.xmlrpc.metawelincdm.get_users_entrys',
     'entryger.getUsersBlogs'),
    ('entry.xmlrpc.metawelincdm.get_user_info',
     'entryger.getUserInfo'),
    ('entry.xmlrpc.metawelincdm.delete_post',
     'entryger.deletePost'),
    ('entry.xmlrpc.metawelincdm.get_authors',
     'wp.getAuthors'),
    ('entry.xmlrpc.metawelincdm.get_categories',
     'metaWelincdm.getCategories'),
    ('entry.xmlrpc.metawelincdm.new_category',
     'wp.newCategory'),
    ('entry.xmlrpc.metawelincdm.get_recent_posts',
     'metaWelincdm.getRecentPosts'),
    ('entry.xmlrpc.metawelincdm.get_post',
     'metaWelincdm.getPost'),
    ('entry.xmlrpc.metawelincdm.new_post',
     'metaWelincdm.newPost'),
    ('entry.xmlrpc.metawelincdm.edit_post',
     'metaWelincdm.editPost'),
    ('entry.xmlrpc.metawelincdm.new_media_object',
     'metaWelincdm.newMediaObject')]

XMLRPC_METHODS = XMLRPC_PINGBACK + XMLRPC_METAWEBLOG
