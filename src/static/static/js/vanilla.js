window.map = null;

main();
async function main() {
  await ymaps3.ready;
  const {YMap, YMapDefaultSchemeLayer, YMapMarker, YMapControls, YMapDefaultFeaturesLayer} = ymaps3;

  const {YMapZoomControl} = await ymaps3.import('@yandex/ymaps3-controls@0.0.1');
  const {YMapDefaultMarker} = await ymaps3.import('@yandex/ymaps3-markers@0.0.1');

  map = new YMap(document.getElementById('yandex-map'), {location: LOCATION});

  map.addChild((scheme = new YMapDefaultSchemeLayer()));
  map.addChild(new YMapControls({position: 'right'}).addChild(new YMapZoomControl({})));
  map.addChild(new YMapDefaultFeaturesLayer({id: 'features'}));

  POINTS.forEach((point) => {
    if (point.element) {
      map.addChild(new YMapMarker(point, point.element(point)));
    } else {
      map.addChild(new YMapDefaultMarker(point));
    }
  });

  const marker = new YMapDefaultMarker(INC_POINT);
  map.addChild(marker);

  const marker2 = new YMapDefaultMarker(INC2_POINT);
  map.addChild(marker2);

  let inc = 0;
  const updateTitle = () => {
    inc++;
    marker.update({
      title: 'Marker inc #' + inc
    });
  };

  updateTitle();
  setInterval(updateTitle, 1000);

  setTimeout(() => {
    marker2.update({
      title: 'Marker 2',
      subtitle: 'Marker 2'
    });
  }, 1000);
}