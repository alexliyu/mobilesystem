from django import template

from apps.weather.models import Weather
from conf.applications import app_by_application_name

register = template.Library()

@register.tag
def weather(parser, token):
    return WeatherNode(*token.split_contents()[1:])
    
class WeatherNode(template.Node):
    """
    Adds a WeatherNode instance to the context.
    """
    
    def __init__(self, name="weather"):
        self.name = name
        
    def render(self, context):
        
        try:
            context[self.name] = Weather.objects.latest('published_date')
        except Weather.DoesNotExist:
            context[self.name] = None
        return ''
