from warnings import warn
warn('geopy.geocoders.virtual_earth: geocoders.virtual_earth is now geocoders.bing',DeprecationWarning)

from baseutils.geopy.geocoders.bing import Bing as VirtualEarth
