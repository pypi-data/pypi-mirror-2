function update_panorama_widget(obj,map, panorama_url_pattern) {
    var option = obj[obj.selectedIndex];
    var panorama_pk = option.value;

    var panorama_url = panorama_url_pattern.replace('999999',panorama_pk);
    panorama_layer(map, panorama_url);
}

function panorama_layer(map, panorama_url) {
  $.get(url=panorama_url, callback = function(data, textStatus) {
      var layer = map.getLayersByName('panorama')[0];
      if (layer) layer.destroy();

      var panorama = JSON.parse(data);
      var imagen = panorama.imgurl
      var size = new OpenLayers.Size(panorama.width, panorama.height);
      var bounds = new OpenLayers.Bounds(0,0,panorama.width,panorama.height);
      var options = {numZoomLevels: 3};
      var newlayer = new OpenLayers.Layer.Image('panorama', imagen, bounds, size, options);
  
      map.addLayer(newlayer);
      map.setBaseLayer(newlayer);
      map.zoomTo(0);
  });
}
