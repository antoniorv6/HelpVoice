<template>
  <div class="map-wrap">
      <div class="map" ref="mapContainer"></div>
  </div>
</template>
  
  <script>
  import { Map, Marker } from 'maplibre-gl';

  import { shallowRef, onMounted, onUnmounted, markRaw } from 'vue';
import {ref} from 'vue';
  
  export default {
    name: "MapeCom",
    props: ["coordinates"],

    setup (props) {
      const coordinate = props.coordinates
      console.log(coordinate)
      const mapContainer = shallowRef(null);
      let map = shallowRef(null);
      console.log(coordinate)
      
  
       onMounted(async () => {
  
        const apiKey = 'BjYaCUZNh1TdYvsXoT86';
        
        map.value = markRaw(new Map({
          container: mapContainer.value,
          style: `https://api.maptiler.com/maps/streets/style.json?key=${apiKey}`,
          center: coordinate,
          zoom: 12
        }));
        const marker = new Marker({color: "#FF0000"}).setLngLat(coordinate);

        marker.addTo(map.value);
        

      }),
      onUnmounted(() => {
        map.value?.remove();
      })
  
      return {
        map, mapContainer
      };
    }
  };
  </script>
  
  
  <style scoped>
  
  .map-wrap {
  position: relative;
  width: 100%;
  height: calc(100vh - 77px); /* calculate height of the screen minus the heading */
}
  .map{
  position: absolute;
  width: 100%;
  height: 100%;
 }


  </style>