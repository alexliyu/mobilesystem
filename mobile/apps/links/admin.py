from django.contrib import admin
from apps.links.models import *

class LinksAdmin(admin.ModelAdmin):
    list_display = ('link_title', 'link_url', 'links_class','addTime')
    list_filter = ('link_title',)

class Links_ClassAdmin(admin.ModelAdmin):
    list_display = ('class_title', 'addTime')
    list_filter = ('class_title',)

admin.site.register(Links,LinksAdmin)
admin.site.register(links_class,Links_ClassAdmin)