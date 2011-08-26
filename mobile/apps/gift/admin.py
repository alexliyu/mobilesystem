from django.contrib import admin
from apps.gift.models import Gift_Info, Gift_History


class Gift_Info_admin(admin.ModelAdmin):
    list_filter = ('business', 'gift_type', 'left_count')
    list_display = ('title', 'all_count', 'left_count', 'money', 'business',
                    'create_time')

    actions_on_top = True
    actions_on_bottom = True
    
    
    
class Gift_History_admin(admin.ModelAdmin):
    list_filter = ('gift', 'user', 'gift_active', 'stat')
    list_display = ('title', 'gift', 'user', 'gift_active', 'stat',
                    'create_time')

    actions_on_top = True
    actions_on_bottom = True


admin.site.register(Gift_Info, Gift_Info_admin)
admin.site.register(Gift_History, Gift_History_admin)
