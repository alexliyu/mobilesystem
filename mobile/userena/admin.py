#-*- coding:utf-8 -*-
"""
这是用户后台管理模型定义文件.

创建于 2011-1-30.

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
import random
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from userena.models import UserenaSignup, Note, Category, Area
from userena.utils import get_profile_model
from baseutils.smsutils import sms




def roles(self):
    short_name = unicode # function to get group name
    #short_name = lambda x:unicode(x)[:1].upper() # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x)) for x in self.groups.all()])
    if self.user_permissions.count(): p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)
roles.allow_tags = True
roles.short_description = u'群组'

def last(self):
    fmt = "%b %d, %H:%M"
    #fmt = "%Y %b %d, %H:%M:%S"
    value = self.last_login.strftime(fmt)
    return mark_safe("<nobr>%s</nobr>" % value)
last.allow_tags = True
last.admin_order_field = 'last_login'
last.short_description = u'最后登录时间'

def adm(self):
    return self.is_superuser
adm.boolean = True
adm.admin_order_field = 'is_superuser'
adm.short_description = u'是否管理员'

def staff(self):
    return self.is_staff
staff.boolean = True
staff.admin_order_field = 'is_staff'
staff.short_description = u'是否工作人员'

from django.core.urlresolvers import reverse

def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])
persons.allow_tags = True
persons.short_description = u'所属用户'

def personscount(self):
    return self.user_set.count()
personscount.allow_tags = True
personscount.short_description = u'用户数'

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1
    


class UserprofileInline(admin.StackedInline):
    model = get_profile_model()
    max_num = 1
    
    
class GroupAdmin(GroupAdmin):
    list_display = ['name', personscount, persons]
    list_display_links = ['name']
    
class UserenaAdmin(UserAdmin):
    inlines = [UserenaSignupInline, UserprofileInline ]
    list_display = ['username', 'email', 'last_name', 'first_name', 'is_active', staff, adm, roles, last]
    list_filter = ['groups', 'is_staff', 'is_superuser', 'is_active']
    actions = ['send_sms']
    actions_on_top = True
    actions_on_bottom = True
    
    def send_sms(self, request, queryset, *arg1, **arg2):
        sms_object = sms()
        for user_object in queryset:
            send_users = ''
            try:
                password = int(random.random() * 100000)
            except:
                password = 123456
            send_users = user_object.get_profile().mobile
            user_object.set_password(password)
            user_object.save()
            send_result = sms_object.post_sms(u'管理员重设密码短信', send_users, u'您的新密码是%s' % password)
            self.message_user(request, send_result)
    send_sms.short_description = u'发送用户密码'
    
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'message_short', 'addtime_format_admin', 'category_name')
    list_display_links = ('id', 'message_short')
    search_fields = ['message']
    list_per_page = 10
    
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    list_display_links = ('id', 'name', 'code')
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_per_page = 10
    
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserenaAdmin)
admin.site.register(get_profile_model())
admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
