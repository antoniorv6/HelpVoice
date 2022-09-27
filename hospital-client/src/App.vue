<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Greet from "./components/Greet.vue";
import { emit, listen } from '@tauri-apps/api/event'
import { sendNotification, isPermissionGranted } from '@tauri-apps/api/notification';
import { BaseDirectory, createDir, writeFile, readTextFile, exists} from "@tauri-apps/api/fs";
</script>

<script>
  export default {
    data(){ return {
      numNotifications : 0,
      unattendedNotifications: [],
      attendedNotifications: [],
      notifications_listener: null
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
        <a href="#" class="nav-link active" aria-current="page">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
          Inicio <span class="badge bg-danger">{{this.numNotifications}}</span>
        </a>
      </li>
      <li>
        <a href="#" class="nav-link text-white">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
          Alertas
        </a>
      </li>
      <li>
        <a href="#" class="nav-link text-white">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#table"></use></svg>
          Historiales
        </a>
      </li>
    </ul>
    <hr>
    </div>
    <div class="col-9">
      <div class="row">
        <div class="col-12 p-3 ">
          <div v-if="this.numNotifications == 0" class="alert alert-success" role="alert">
            <b>No hay nuevas notificaciones</b>
          </div>
          <div v-else class="alert alert-danger" role="alert">
            <b>Tienes {{this.numNotifications}} alertas sin atender.</b>
          </div>
        </div>
      </div>
      <div class="row">
        <div v-for="alert in this.unattendedNotifications" class="col-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{alert.level}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{alert.user}}</h6>
              <h6 class="card-subtitle mb-2 text-muted">{{alert.coordinates}}</h6>
              <p class="card-text">{{alert.transcription}}</p>
              <button type="button" class="btn btn-primary btn-lg">Detalles</button>
            </div>
          </div>
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
</style>
