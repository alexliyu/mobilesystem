from django.contrib import admin
from apps.interactive.models import Interactive_Info, Interactive_User, Interactive_Categries
from mobile.utils.sms import sms


class Interactive_User_Admin(admin.ModelAdmin):
    list_filter = ('interactive_user', 'interactive_info', 'stat')
    list_display = ('interactive_user', 'interactive_info', 'stat',
                    'create_time')

    actions_on_top = True
    actions_on_bottom = True



admin.site.register(Interactive_Info)
admin.site.register(Interactive_User, Interactive_User_Admin)
admin.site.register(Interactive_Categries)
