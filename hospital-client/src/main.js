import { createApp } from "vue";

import "./css/bootstrap.min.css"
import './../node_modules/maplibre-gl/dist/maplibre-gl.css'
import App from "./App.vue"
import { initializeApp } from 'firebase/app';

fetch('./src/firebase-key.json').then( async (response) =>{ 
    initializeApp(await response.json());
    console.log('ok entre')
})

const app = createApp(App);

app.mount("#app");
