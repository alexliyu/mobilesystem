from django.contrib import admin

from models import Weather

class WeatherAdmin(admin.ModelAdmin):
    list_display = ('observed_date', 'published_date', 'temperature')
    list_filter = ('temperature',)
    
admin.site.register(Weather, WeatherAdmin)
