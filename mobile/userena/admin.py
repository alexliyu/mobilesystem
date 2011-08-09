from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from userena.models import UserenaSignup, Note, Category, Area
from userena.utils import get_profile_model

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1
class UserprofileInline(admin.StackedInline):
    model = get_profile_model()
    max_num = 1
class UserenaAdmin(UserAdmin):
    inlines = [UserenaSignupInline, UserprofileInline ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'date_joined')

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
admin.site.register(User, UserenaAdmin)
admin.site.register(get_profile_model())
admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Area, AreaAdmin)
