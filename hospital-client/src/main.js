import { createApp } from "vue";

import "./css/bootstrap.min.css"
import './../node_modules/maplibre-gl/dist/maplibre-gl.css'
import App from "./App.vue"

const app = createApp(App);

app.mount("#app");
