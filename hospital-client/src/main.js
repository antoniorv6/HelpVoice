import { createApp } from "vue";
import 'vue3-openlayers/dist/vue3-openlayers.css'
import "./css/bootstrap.min.css"

import App from "./App.vue"
import OpenLayersMap from 'vue3-openlayers'

const app = createApp(App);
app.use(OpenLayersMap)
app.mount("#app");
