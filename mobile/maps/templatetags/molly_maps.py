#-*- coding:utf-8 -*-
'''
Created on 2011-1-30

@author: 李昱
'''
from django import template
from django.template.loader import get_template

from maps import map_from_point

register = template.Library()

class MapDisplayNode(template.Node):
    """
    Node to display a more complex map from a @C{maps.Map} object
    """
    
    def __init__(self, map):
        """
        @param map: The Map to be rendered
        @type map: maps.Map
        """
        self.map = map
    
    def render(self, context):
        """
        Returns HTML for the map to be rendered
        
        @type context: dict
        """
        context.update({
            'map': template.Variable(self.map).resolve(context)
            })
        return get_template('maps/embed.html').render(context)

@register.tag
def render_map(parser, token):
    """    
    @raise template.TemplateSyntaxError: If incorrect arguments are passed
    @return: Ready for the map to be rendered
    @rtype: MapDisplayNode
    """
    try:
        tag_name, map = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError, \
            "%r tag requires exactly 1 arguments: map" % tag_name
    return MapDisplayNode(map)

class LocationDisplayNode(template.Node):
    """
    Node to display a simple map with only one location
    """
    
    def __init__(self, place):
        """
        @param place: Point to render a map for
        """
        self.place = place
    
    def render(self, context):
        """
        返回用于渲染的地图HTML内容
        
        @type context: dict
        """
        html = ''
        try:
            if context['entity'].businessinfo_set.get().get_absolute_url():
                html = context['entity'].title + "<p><a href=%s>点击察看商家详细信息</a></p>" % context['entity'].businessinfo_set.get().get_absolute_url()
            else:
                html = context['entity'].title + "<p>暂无商家详细信息</p>"
        except:
                html = context['entity'].title + "<p>暂无商家详细信息</p>"
        context.update({
           'map': map_from_point(template.Variable(self.place).resolve(context),
                                 context['request'].map_width,
                                 context['request'].map_height,
                                 title=html,
                                 zoom=context.get('zoom', 14))
           })
        return get_template('maps/embed.html').render(context)

@register.tag
def render_location_map(parser, token):
    """    
    @raise template.TemplateSyntaxError: If incorrect arguments are passed
    @return: Ready for the map to be rendered
    @rtype: PlaceDisplayNode
    """
    try:
        tag_name, place = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError, \
            "%r tag requires exactly 1 arguments: location" % tag_name
    return LocationDisplayNode(place)
