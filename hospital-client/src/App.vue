<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Greet from "./components/Greet.vue";
import { emit, listen } from '@tauri-apps/api/event'
import { sendNotification } from '@tauri-apps/api/notification';
import { BaseDirectory, createDir, writeFile, readTextFile, exists} from "@tauri-apps/api/fs";
</script>

<script>
  import {ref} from 'vue'
  export default {
    setup() {
      const center = ref([-98.8449,19.6869])
      const projection = ref('EPSG:4326')
      const zoom = ref(15)
      const rotation = ref(0)
      const radius = ref(40)
      const strokeWidth = ref(10)
      const strokeColor = ref('red')

      return {
          center,
          projection,
          zoom,
          rotation,
          radius,
          strokeWidth,
          strokeColor,
      }
    },
    data(){ return {
      numNotifications : 0,
      unattendedNotifications: [],
      attendedNotifications: [],
      notifications_listener: null,
      appState: 0,
      visualized_alert: 0
    }},
    mounted() {
      this.notifications_listener = listen('new_alert', (event) => {
        this.store_notification(event.payload)
        sendNotification({title: 'Nueva alerta', body:event.payload})

      }
        )
      this.init()
      },
    methods: {
      store_notification: async function(notificationContent){
        const notification_object = await JSON.parse(notificationContent)
        this.numNotifications += 1;
        this.unattendedNotifications.push(notification_object)
        console.log("Notification correctly propagated")
        await this.saveStateSnapshot()
      },
      init: async function(){
        try
        {
          await createDir("data" ,{dir: BaseDirectory.Desktop})
        }
        catch (e)
        {
          console.error(e)
        }
        const content = await readTextFile("./data/state.json", {dir: BaseDirectory.Desktop})
        const jsonContent = await JSON.parse(content)
        this.numNotifications = jsonContent.numNotifications
        this.unattendedNotifications = jsonContent.unattendedNotifications
        this.attendedNotifications = jsonContent.attendedNotifications
      },
      saveStateSnapshot: async function(){
        try{
          let jsonData = {
            numNotifications: this.numNotifications,
            unattendedNotifications: this.unattendedNotifications,
            attendedNotifications: this.attendedNotifications
          }
          writeFile("./data/state.json",
            `${JSON.stringify(jsonData)}`,
            {dir: BaseDirectory.Desktop}).then(()=>{
            console.log("ok")
          })
        }
        catch(e)
        {
          console.error(e)
        }
      },
      visualize_alert: function (alert_number, visualized) {
        console.log(`You are visualizing alert ${alert_number}`)
        if(!visualized)
          this.visualized_alert = this.unattendedNotifications[alert_number]
        else
          this.visualized_alert = this.attendedNotifications[alert_number]

        this.appState = 1
      },
      send_message: function(body){
        console.log("Sending alert")
        emit("send_rbmq", {theMessage: 'Tauri is awesome!'})
      }
    }
  }
</script>

<template>
  <div class="container m-0 p-0">
  <div class="row">
    <div class="col-3 p-3 text-bg-dark" style="width: 280px; min-height: 720px;">
    <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none">
      <svg class="bi pe-none me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
      <span class="fs-4">Help Voice!</span>
    </a>
    <hr>
    <ul class="nav nav-pills flex-column mb-auto">
      <li class="nav-item">
        <a href="#" class="nav-link active" aria-current="page" id="Home">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
          Inicio <span class="badge bg-danger">{{this.numNotifications}}</span>
        </a>
      </li>
      <li>
        <a href="#" class="nav-link text-white" id="Alerts">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
          Alertas
        </a>
      </li>
      <li>
        <a href="#" class="nav-link text-white " id="History">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#table"></use></svg>
          Historiales
        </a>
      </li>
    </ul>
    <hr>
    </div>
    <div v-if="this.appState == 0" class="col-9">
      <div class="row">
        <div class="col-12 p-3 ">
          <h1>Alertas pendientes</h1>
          <br>
          <div v-if="this.numNotifications == 0" class="alert alert-success" role="alert">
            <b>No hay nuevas notificaciones</b>
          </div>
          <div v-else class="alert alert-danger" role="alert">
            <b>Tienes {{this.numNotifications}} alertas sin atender.</b>
          </div>
        </div>
      </div>
      <div class="row">
        <div v-for="(alert, index) in this.unattendedNotifications" class="col-4">
          <div class="card" style="min-height: 250px;">
            <div class="card-body">
              <h5 class="card-title">{{alert.level}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{alert.user}}</h6>
              <p class="card-text">{{alert.transcription}}</p>
            </div>
            <div class="card-footer">
              <button type="button" class="btn btn-primary btn-lg" v-on:click="this.visualize_alert(index)">Detalles</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="this.appState == 1" class="col-9">
      <div class="row">
        <div class="jumbotron p-3">
          <button type="button" class="btn btn-outline-secondary" v-on:click="this.appState=0">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
          </svg>
          Atrás
          </button>
          <br>
          <br>
          <div v-if="this.visualized_alert.level_int==0" class="alert alert-danger" role="alert">
            <b>Nivel de emergencia alto</b>
          </div>
          <div v-if="this.visualized_alert.level_int==1" class="alert alert-warning" role="alert">
            <b>Nivel de emergencia medio</b>
          </div>
          <div v-if="this.visualized_alert.level_int==2" class="alert alert-primary" role="alert">
            <b>Nivel de emergencia bajo</b>
          </div>
          <h2 class="display-4">{{this.visualized_alert.user}}</h2>
          <h5>Enfermedad diagnosticada:</h5>
          <p class="lead">{{this.visualized_alert.diagnostico}}</p>
          <h5>Mensaje recibido:</h5>
          <p class="lead">{{this.visualized_alert.transcription}}</p>
          <h5>Ubicación del paciente:</h5>
            <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height:400px">

            <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />
                    
            <ol-tile-layer>
                <ol-source-osm />
            </ol-tile-layer>
          
            <ol-vector-layer>
                <ol-source-vector>
                    <ol-feature>
                        <ol-geom-polygon :coordinates="[[[-98.844959,19.691586],[-98.842749,19.690980],[-98.842170,19.693122],[-98.844358,19.693667],[-98.844959,19.691586]]]"></ol-geom-polygon>
                        <ol-style>
                            <ol-style-stroke :color="strokeColor" :width="strokeWidth"></ol-style-stroke>
                        </ol-style>
                    </ol-feature>
                
                </ol-source-vector>
            
            </ol-vector-layer>
          
          </ol-map>
          <hr class="my-4">
          <p class="lead">
          <button class="btn btn-success btn-lg" href="#" role="button" style="margin-right: 1em;" v-on:click="this.send_message('Hello brother')">Atender alerta</button>
          <button class="btn btn-danger btn-lg" href="#" role="button">Rechazar alerta</button>
          </p>
        </div>
      </div>
    </div>
    

  </div>
</div>
  
</template>

<style scoped>
  html{
    height: 100%;
  }
  .overlay-content {
    background: #efefef;
    box-shadow: 0 5px 10px rgb(2 2 2 / 20%);
    padding: 10px 20px;
    font-size: 16px;
}
</style>
