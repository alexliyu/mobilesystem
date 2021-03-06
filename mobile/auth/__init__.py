#-*- coding:utf-8 -*-
"""
这是用于系统用户帐号的应用，主要用于与外部其他网站进行账户关联

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from django.utils.translation import ugettext_lazy as _

class Mete:
    """
    定义此应用程序的附加信息，诸如应用程序名
    """
    title = _('Auth')

from django.contrib.auth.models import User

from conf import app_by_application_name
from auth.models import UserIdentifier, UserSession, ExternalServiceToken
from favourites.models import Favourite

def unify_users(request):
    user = request.user
    conf = app_by_application_name('auth')

    users = set()
    for identifier in user.useridentifier_set.all():
        if not identifier.namespace in conf.unify_identifiers:
            continue

        identifiers = UserIdentifier.objects.filter(namespace=identifier.namespace, value=identifier.value)

        users |= set(i.user for i in identifiers)

    token_namespaces = set(t.namespace for t in user.externalservicetoken_set.all())
    identifier_namespaces = set(i.namespace for i in user.useridentifier_set.all())

    root_user = min(users, key=lambda u:u.date_joined)
    
    # Also need to update favourites
    Favourite.objects.filter(user__in=users).update(user=root_user)
    
    # Need to do the root_user first, otherwise if it's after the current user,
    # tokens get assigned from the current user to the root user, and then
    # removed from the root user, because it's not the current user.
    # We accomplish this by sorting the set into a list, with a custom
    # comparison function which gives the root_user the lowest value (and so is
    # first)
    for u in sorted(users, cmp=lambda x, y:-1 if x == root_user else 1 if y == root_user else 0):

        u.usersession_set.all().update(user=root_user)

        for token in u.externalservicetoken_set.all():
            if u != user and token.namespace in token_namespaces:
                token.delete()
            else:
                token.user = root_user
                token.save()

        for identifier in u.useridentifier_set.all():
            if u != user and identifier.namespace in identifier_namespaces:
                identifier.delete()
            else:
                identifier.user = root_user
                identifier.save()

        if u != root_user:
            u.delete()
