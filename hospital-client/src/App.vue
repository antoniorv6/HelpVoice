<script setup>
import MapeCom from './components/MapeCom.vue';

import { emit, listen } from '@tauri-apps/api/event'
import { sendNotification } from '@tauri-apps/api/notification';
import { BaseDirectory, createDir, writeFile, readTextFile, exists} from "@tauri-apps/api/fs";
import { getDatabase, ref, onValue } from 'firebase/database'

</script>

<script>
  //import {ref} from 'vue'
  //let modalEle= ref(null);
  export default {
    components:{
      MapeCom
    },
    data(){ return {
      numNotifications : 0,
      unots: [],
      anots: [],
      onots: [],
      notifications_listener: null,
      appState: 0,
      visualized_alert: 0,
      chosen_action: 0
    }},
    mounted() {
      this.save_notifications_listener = listen('save_alert', (event)=>{
        console.log("Yepa")
        const notification = JSON.parse(event.payload)
        this.store_notification(notification)
      })
      this.notifications_listener = listen('new_alert', (event) => {
        
       event.payload = JSON.parse(event.payload)
       
        const db = getDatabase()
        const settingsRef = ref(db, '/users/' +event.payload['user_id'])
        onValue(settingsRef, function(snapshot) {
          console.log("Hola")
          var childData = snapshot.val();
          event.payload.personal = childData
          emit('save_alert', event.payload)
        });

        sendNotification({title: 'Nueva alerta', body:JSON.stringify(event.payload)})

      }
        )
      this.init()
      },
    methods: {
      store_notification: async function(notificationContent){
        console.log("Reached")
        const notification_object = notificationContent
        console.log(notification_object)
        this.numNotifications += 1;
        this.unots.push(notification_object)
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
        console.log(jsonContent)
        this.numNotifications = jsonContent.numNotifications
        this.unots = jsonContent.unots
        this.onots = jsonContent.onots
        this.anots = jsonContent.anots
      },
      saveStateSnapshot: async function(){
        try{
          let jsonData = {
            numNotifications: this.numNotifications,
            unots: this.unots,
            anots: this.anots,
            onots: this.onots
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
        {
          this.visualized_alert = this.unots[alert_number]
          this.unots.splice(alert_number,1)
          this.onots.push(this.visualized_alert)
          this.numNotifications -= 1
          this.saveStateSnapshot()
        }
        else
          this.visualized_alert = this.onots[alert_number]
        
        console.log(this.visualized_alert)
        this.appState = 1
      },
      send_message: function(body){
        const response = JSON.stringify({"user_id": body.user_id, 
        "hospital":"Hospital la paz", 
        'coordinates': [98.24, 54.03], 
        "illness":this.visualize_alert.sickness_prediction, 
        "action":this.chosen_action})
        
        console.log(response)
        emit("send_rbmq", response)
      },
      alert_color(a) {
        if(a==0){
          return 'h_alert'
        }else if(a==1){
          return 'm_alert'
        }else{
          return 'l_alert'
        }

    }
    },

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
    <ul class="nav nav-pills flex-column mb-auto ">
      <li class="nav-item">
        <a href="#" class="nav-link active" aria-current="page" id="Home">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
          Inicio <span v-if="this.numNotifications > 0" class="badge bg-danger">{{this.numNotifications}}</span>
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link link-light" id="Alerts">
          <svg class="bi pe-none me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
          Alertas
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link link-light" id="History">
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
        <div v-for="(alert, index) in this.unots" class="col-4">
          <div class="card" style="min-height: 250px; max-height: 250px;">
            <div class="card-body">
              <h5 class="card-title" :class="alert_color(alert.level_int)">{{alert.level}} 
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-circle-fill" viewBox="0 0 16 16" style="margin-left: 3.5em;">
                <circle cx="8" cy="8" r="8"/>
              </svg>
              </h5>
              <h6 class="card-subtitle mb-2 text-muted">Fractura</h6>
              <p class="card-text">{{alert.transcription}}</p>
            </div>
            <div class="card-footer text-end">
              <button type="button" class="btn btn-primary btn-lg" v-on:click="this.visualize_alert(index, false)">Detalles</button>
            </div>
          </div>
        </div>
        <div v-for="(alert, index) in this.onots" class="col-4">
          <div class="card" style="min-height: 250px; max-height: 250px;">
            <div class="card-body" style="overflow: hidden;">
              <h5 class="card-title" :class="alert_color(alert.level_int)">{{alert.level}}</h5>
              <h6 class="card-subtitle mb-2 text-muted">Fractura</h6>
              <p class="card-text">
                {{alert.transcription}}
              </p>
            </div>
            <div class="card-footer text-end">
              <button type="button" class="btn btn-primary btn-lg" v-on:click="this.visualize_alert(index, true)">Detalles</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="this.appState == 1" class="col-9">
      <div class="row">
        <div class="jumbotron p-3">
          <button type="button" class="btn btn-outline-secondary" v-on:click="this.appState=0">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" class="bi bi-arrow-left" viewBox="0 0 16 16">
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
    
          <div class="container">
            <div class="row">
            <div class="col">
           
             <h5>Datos paciente</h5>
             <div class="row ms-1">
              <span class="text-muted">Nombre</span>
              <p>{{this.visualized_alert.personal.name}}</p>
            </div>
            <div class="row ms-1">
              <div class="col">
                <span class="text-muted">Edad</span>
                <p>{{this.visualized_alert.personal.Edad}}</p>
              </div>
              <div class="col">
                <span class="text-muted">Sexo</span>
                <p> {{this.visualized_alert.personal.Sexo}}</p>
              </div>
            </div>

            <div class="row ms-1">
              <div class="col">
                  <span class="text-muted">Dirección</span>
                  <p>C. de Orense, 4, 28020 Madrid</p>
              </div>
              <div class="col">
                <span class="text-muted">Contacto</span>
               <p>{{this.visualized_alert.personal.phone}}</p>
              </div>
            </div>

              <h5>Mensaje recibido</h5>
              <p class="ms-3">{{this.visualized_alert.transcription}}</p>
              <h5>Audio mensaje</h5>
              <audio controls>
                <source src="https://file-examples.com/storage/feb2e515cc6339d7ba1ffcd/2017/11/file_example_MP3_700KB.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
              </audio>
              <h5>Diagnostico</h5>
              <p class="ms-3">Fractura</p>
              
              <hr class="my-4">
              <p class="lead">
          <button class="btn btn-success btn-lg" href="#" role="button" style="margin-right: 1em;" v-on:click="this.appState = 2">Atender alerta</button>
          <button class="btn btn-danger btn-lg" href="#" role="button">Rechazar alerta</button>
          </p>
          </div>

            <div class="col">
              <MapeCom :coordinates="[visualized_alert.lon, visualized_alert.lat]" />
            </div>
          </div>
        </div>
        </div>
       
        </div>
          
    </div>
    <div v-if="this.appState == 2" class="col-9">
      <div class="row">
        <div class="jumbotron p-3">
          <button type="button" class="btn btn-outline-secondary" v-on:click="this.appState=0">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#ffffff" class="bi bi-arrow-left" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8z"/>
          </svg>
          Atrás
          </button>
          <br>
          <br>
          <h3>Vas a atender la alerta de {{this.visualized_alert.personal.name}}</h3>
          <br>
          <div class="container">
            <div class="row">
            <div class="col">

            <div class="row ms-1">
              <div class="col">
                  <span class="text-muted">Dirección</span>
                  <p>C. de Orense, 4, 28020 Madrid</p>
              </div>
              <div class="col">
                <span class="text-muted">Contacto</span>
               <p>{{this.visualized_alert.personal.phone}}</p>
              </div>
            </div>

            <h5>Diagnostico</h5>
            <div class="input-group">
              <input type="text" class="form-control" value="Fractura" aria-label="Recipient's username" aria-describedby="basic-addon2">
            </div>
            <h5>Acción</h5>
            <div class="input-group">
              <select v-model="this.chosen_action" class="custom-select" id="inputGroupSelect01">
                <option selected>Choose...</option>
                <option value="Llamada telefónica urgente">Llamada telefónica urgente</option>
                <option value="Enviar ambulancia">Enviar ambulancia</option>
              </select>
            </div>
            <hr class="my-4">
            <p class="lead">
          <button class="btn btn-lg btn-primary" href="#" role="button" style="margin-right: 1em;" v-on:click="this.send_message(this.visualized_alert)">Responder alerta</button>
          </p>
          </div>

            <div class="col">
              <MapeCom :coordinates="[visualized_alert.lon, visualized_alert.lat]" />
            </div>
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
  .overlay-content {
    background: #efefef;
    box-shadow: 0 5px 10px rgb(2 2 2 / 20%);
    padding: 10px 20px;
    font-size: 16px;
}

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
  
  h5{
    color: #252525 !important;
  }

  .h_alert{
    background-color: #ff0054 !important;
    color: white !important;
    padding: .5em;
  }

  .m_alert{
    background-color: #f4a261 !important;
    color: white !important;
    padding: .5em;
  }

  .l_alert{
    background-color: #8ecae6 !important;
    color: white !important;
    padding: .5em;
  }
</style>
