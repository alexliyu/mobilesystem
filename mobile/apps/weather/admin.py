from django.contrib import admin

from models import Weather

class WeatherAdmin(admin.ModelAdmin):
    list_display = ('observed_date', 'temperature', 'min_temperature', 'max_temperature', 'sunset', 'sunrise', 'wind_speed', 'wind_direction', 'humidity', 'pressure')
    list_filter = ('temperature',)
    
admin.site.register(Weather, WeatherAdmin)
