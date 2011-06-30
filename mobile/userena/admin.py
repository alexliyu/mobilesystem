from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from mobile.userena.models import UserenaSignup
from mobile.userena.utils import get_profile_model

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1

class UserenaAdmin(UserAdmin):
    inlines = [UserenaSignupInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, UserenaAdmin)
admin.site.register(get_profile_model())