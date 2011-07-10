{% extends "gis/admin/openlayers.js" %}
 
{% block base_layer %}new OpenLayers.Layer.Google("Google Base Layer", {
    'type': google.maps.MapTypeId.ROADMAP, 
    'sphericalMercator': true
});
 
{% endblock %}
 

{% block controls %}
 
{{ block.super }}
// 2011-07-09 作者：李昱 功能实现：使用openlayers的GOOGLE MAP API V3显示地图，并且默认进行当前位置定位


if (!wkt) {
    var zoomLevel = 14;
    var infowindow = new google.maps.InfoWindow();
    // 尝试使用 W3C 定位，最好的方法
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
               // 进行定位
               initialLocation = new OpenLayers.LonLat(
                position.coords.longitude, position.coords.latitude
                ).transform(
                    new OpenLayers.Projection("EPSG:4326"),
                    new OpenLayers.Projection("EPSG:3857")
                );
                
               {{ module }}.map.setCenter(initialLocation, zoomLevel);
                // 显示信息框
                contentString = "当前位置已经使用W3C进行定位";
                popup = new OpenLayers.Popup("mylocation",initialLocation,new OpenLayers.Size(200,20),contentString,true);
                {{ module }}.map.addPopup(popup);
        }, function() {
            // Location could not be found (probably denied by user)
        });
    } else if (google.gears) {
        // 尝试使用 Google Gears 定位，基本上webkit浏览器都支持
        var geo = google.gears.factory.create('beta.geolocation');
 
        geo.getCurrentPosition(function(position) {
            
            initialLocation = new OpenLayers.LonLat(position.longitude, position.latitude);
            {{ module }}.map.setCenter(initialLocation, zoomLevel);
            // 显示信息框
            contentString = "当前位置已经使用Gears进行定位";
            popup = new OpenLayers.Popup("mylocation",initialLocation,new OpenLayers.Size(200,20),contentString,true);
            {{ module }}.map.addPopup(popup);
            
        }, function() {
            // Location could not be found (probably denied by user)
        });
    } else {
        // 不支持浏览器定位，进行不支持情况下的处理。。。。默认定位到厦门娱讯公司位置
    	
    }
}
 
{% endblock %}