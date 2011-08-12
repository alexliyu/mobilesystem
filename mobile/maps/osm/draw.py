#-*- coding:utf-8 -*-
"""
这是地图绘制程序，用于生成带标注的静态地图文件，主要用于在非webkit浏览器浏览时显示的静态地图

@author 李昱 Email:alexliyu2012@gmail.com QQ:939567050
       
"""
from __future__ import division
import math
import random
import PIL.Image
import urllib
import os.path
import sys
import time
from StringIO import StringIO
from maps.osm.models import OSMTile, get_marker_dir

def log2(x):
    """
    @return: log(x)/log(2)
    """
    return math.log(x) / math.log(2)

def get_tile_ref(lon_deg, lat_deg, zoom):
    """
    Gets OSM tile co-ordinates for the specified longitude, latitude and zoom
    level.
    
    @param lon_deg: The longitude, in degrees
    @type lon_deg: float
    
    @param lat_deg: The latitude, in degrees
    @type lat_deg: float
    
    @param zoom: The zoom level to get the tile references for
    @type zoom: int
    
    @return: A tuple of (x, y) co-ordinates for the OSM tile
    """
    lat_rad = lat_deg * math.pi / 180.0
    n = 2.0 ** zoom
    xtile = (lon_deg + 180.0) / 360.0 * n
    ytile = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
    return (xtile, ytile)

def get_tile_geo(xtile, ytile, zoom):
    """
    Gets the latitude and longitude corresponding to a particular set of OSM
    tile co-ordinates.
    
    @param lon_deg: The longitude, in degrees
    @type lon_deg: int
    
    @param lat_deg: The latitude, in degrees
    @type lat_deg: int
    
    @param zoom: The zoom level this tile exists at
    @type zoom: int
    
    @return: A tuple of (long, lat) co-ordinates for the OSM tile
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = lat_rad * 180.0 / math.pi
    return (lon_deg, lat_deg)

def minmax(i):
    """
    Gets the minimum and maximum values in some list
    
    @param i: The list for the maximum and minimum values to be obtained from
    @type i: list
    
    @return: A tuple (min, max)
    """
    min_, max_ = float('inf'), float('-inf')
    for e in i:
        min_ = min(min_, e)
        max_ = max(max_, e)
    return min_, max_

def get_map_url(points, zoom, lon_center, lat_center):
    """
    根据GOOGLE API生成用于获取标注好的静态地图文件的URL
    """
    g_points = ['&markers=color:%s|label:%s|%s,%s' % (p[2], p[3], p[1], p[0]) for p in points]
    g_api = "http://maps.google.com/maps/api/staticmap?center=%s,%s&zoom=%s&size=400x400&maptype=roadmap&mobile=true&sensor=true&language=zh_CN" % (lat_center, lon_center, zoom)
    g_map = g_api + ''.join(g_points)
    return g_map
def get_map(points, width, height, filename, zoom=None, lon_center=None, lat_center=None, retry=True):
    """
    根据参数生成带标注的静态地图文件
    
    @param points: The points where markers on the map should be added. This
                   should be a list of tuples corresponding to the points where
                   markers should be added. These tuples should be in the form
                   (latitude, longitude, colour, index), where acceptable values
                   of colour are specified in @C{utils.MARKER_COLOURS}, and
                   index is the number to appear on the marker, or None if
                   you want a star to appear
    @type points: list
    @param width: The width of the generated map image, in pixels
    @type width: int
    @param height: The height of the generated map image, in pixels
    @type height: int
    @param filename: The name of the file to write the generated map to
    @type filename: str
    @param zoom: The maximum zoom level which to generate this map at
    @type zoom: int
    @param lon_center: The actual center of the generated map
    @type lon_center: float
    @param lat_center: The actual center of the generated map
    @type lat_center: float
    """
    
    lon_min, lon_max = minmax(p[0] for p in points)
    lat_min, lat_max = minmax(p[1] for p in points)
    if width <= 30:width = 200
    if height <= 30:height = 200
    if not zoom:
        size = min(width, height)
        if lat_min != lat_max:
            zoom = int(log2(360 / abs(lat_min - lat_max)) + log2(size / 256) - 1.0)
        else:
            zoom = 16
    """
    2011-8-12 修改原有的通过本地静态地图文件进行标注为直接从GOOGLE服务器获取标注好的静态地图图片文件
    """
    #points = [(get_tile_ref(p[0], p[1], zoom), p[2], p[3]) for p in points]
    lon_range, lat_range = lon_max - lon_min, lat_min - lat_max
    if not lat_center:
        lon_center, lat_center = (lon_min + lon_max) / 2, (lat_min + lat_max) / 2
    try:
        response = urllib.urlopen(get_map_url(points, zoom, lon_center, lat_center))
    except IOError:
            # If it fails... try again, but only once
            if retry:
                return get_map(points, width, height, filename, zoom, lon_center, lat_center, retry=False)
            else:
                raise
    s = StringIO()
    s.write(response.read())
    f = open(filename, 'w')
    f.write(s.getvalue())
    f.close()

    return lon_center, lat_center

class PointSet(set):
    
    def __init__(self, initial=None):
        """
        @param initial: An initial point set to use
        @type initial: ( (float, float) )
        """
        super(PointSet, self).__init__(initial)
        self._min = (float('inf'), float('inf'))
        self._max = (float('-inf'), float('-inf'))
        self.ordered = []
        for p in initial:
            self.update(p)
        
    def add(self, point):
        """
        Add a point to the set
        
        @param point: The point to be added
        @type point: (float, float)
        """
        super(PointSet, self).add(point)
        self.update(point)
    
    def remove(self, point):
        """
        Remove a point from the set
        
        @param point: The point to be removed
        @type point: (float, float)
        """
        self.ordered.remove(point)
        super(PointSet, self).remove(point)
        if any((point[i] in (self._min[i], self._max[i])) for i in range(2)):
            self._min = (float('inf'), float('inf'))
            self._max = (float('-inf'), float('-inf'))
            for point in self:
                self._min = (min(self._min[0], point[0]),
                             min(self._min[1], point[1]))
                self._max = (max(self._max[0], point[0]),
                             max(self._max[1], point[1]))
    
    def update(self, point):
        """
        Update the set
        
        @param point: The point to be added
        @type point: (float, float)
        """
        self.ordered.append(point)
        self._min = min(self._min[0], point[0]), min(self._min[1], point[1])
        self._max = max(self._max[0], point[0]), max(self._max[1], point[1])
        
    def extent(self, zoom):
        """
        Get the bounding box of this set of points
        
        @param zoom: The zoom level to use
        """
        top_left = get_tile_ref(self._min[0], self._min[1], zoom)
        bottom_right = get_tile_ref(self._max[0], self._max[1], zoom)
        
        a = (bottom_right[0] - top_left[0]) * 256, (top_left[1] - bottom_right[1]) * 256
        return a
        
    def contained_within(self, box, zoom):
        """
        Check if @C{box} is inside this pointset at the specified zoom level
        """
        extent = self.extent(zoom)
        return extent[0] <= box[0] and extent[1] <= box[1]
        

def get_fitted_map(centre_point, points, min_points, zoom, width, height, filename):
    """
    Given a list of points and some minimum number of points, then a "fitted
    map" is generated, which is one which contains at least @C{min_points}, and
    is at least at the zoom level @C{zoom}, but also contains any other points
    in the list which is inside the bounding area of this minimal map.
    
    Valid colours in point definitions below are defined in @C{MARKER_COLOURS}
    
    @param centre_point: A tuple of longitude, latitude and colour corresponding
                         to the "centre" of the map. This is NOT the central
                         latitude/longitude of the generated image, which is
                         simply the middle of the set of points passed in, but
                         simply a special marker which is indicated with a star.
    @type centre_point: (float, float, str) or None
    @param points: An (ordered) list of points to be plotted on the map. These
                   are indicated on the map with numbered markers. This list
                   consists of tuples of longitude, latitude and a string
                   indicating the colours of the markers to be rendered.
    @type points: [(float, float, str)]
    @param min_points: The minimum number of points to be displayed on the
                       resulting map
    @type min_points: int
    @param zoom: A bound on the maximum zoom level to be rendered. If this zoom
                 level is too small to fit @C{min_points} points on it, then the
                 map will be zoomed out further to fit in. If this is None, then
                 this is equivalent to the smallest zoom level.
    @type zoom: int
    @param width: The width of the generated map image, in pixels
    @type width: int
    @param height: The height of the generated map image, in pixels
    @type height: int
    
    @raise MapGenerationError: If a map can not be generated (normally if the
                               OSM tile server is down)
    """

    # If we haven't been given a zoom, start as close as we can
    if not zoom:
        zoom = 18

    box = max(64, width - 20), max(64, height - 35)
    
    new_points = []
    for i, point in enumerate(points):
        if i > 1 and point == new_points[-1][0]:
            new_points[-1][1].append(i)
        else:
            new_points.append((point, [i]))
    
    points = [p[0] for p in new_points]
    
    # Include the central point in the points to be considered
    if centre_point:
        points = [centre_point] + list(points)
    
    # Get a set of the minimum points
    point_set, points = PointSet(points[:min_points + 1]), points[min_points + 1:]
    
    # Zoom out until the entire point set fits inside the generated map
    while not point_set.contained_within(box, zoom):
        zoom -= 1

    # If there are points outside the minimum points, see if they fit inside
    # the bounding box of the minimum points (or the specified zoom level)
    while point_set.contained_within(box, zoom):
        if not points:
            break
        new_point, points = points[0], points[1:]
        point_set.add(new_point)
    else:
        point_set.remove(new_point)
    
    if centre_point:
        used_points = point_set.ordered[1:]
        points = [(centre_point[0], centre_point[1], centre_point[2], None)]
    else:
        used_points = point_set.ordered[:]
        points = []
    
    for i, point in enumerate(used_points):
        points.append(
            (point[0], point[1], point[2], i + 1)
        )
    
    if centre_point:
        new_points = new_points[:len(point_set) - 1]
    else:
        new_points = new_points[:len(point_set)]
    
    try:
        lon_center, lat_center = get_map(points, width, height, filename, zoom)
    except MapGenerationError as e:
        e.metadata = (new_points, zoom, e.metadata[0], e.metadata[1])
        raise
    
    return new_points, zoom, lon_center, lat_center

class MapGenerationError(Exception):
    """
    Indicates that a map was unable to be successfully generated, but one was
    still attempted to be, in which case the metadata of the generated map can
    be attached to this.
    """
    
    def __init__(self, metadata=None):
        self.metadata = metadata

if __name__ == '__main__':
    RED, GREEN, BLUE = (1, 0, 0), (0, 0.5, 0), (0.25, 0.25, 1)
    get_map(
        [
            (51.760283, -1.259941, 'blue', None),
            (51.760565, -1.259021, 'red', 1),
            (51.760009, -1.260275, 'green', 2),
            (51.760294, -1.258813, 'red', 3),
            (51.759805, -1.261170, 'green', 4),
            (51.759810, -1.261359, 'red', 5),
            (51.759662, -1.261110, 'green', 6),
            (51.759520, -1.260638, 'red', 7),
            (51.759247, -1.259904, 'green', 8),
            (51.759173, -1.259880, 'red', 9),
        ], 300, 200, 'foo.png')
