import pika
from loguru import logger
import os
import base64
import json
import sys

from Wav2Vec import AudioTranscription
from distance import Hosp_Dist_Calc
from DiseasePredictor import DiseasePredictor


logger.info("Initializing server add-ons")
audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
distance_module = Hosp_Dist_Calc("data/datos_hospitales.csv")
disease_pred = DiseasePredictor()
logger.success("Server add-ons initialized correctly")

class RabbitMQManager:
    @logger.catch
    def __init__(self) -> None:
        logger.info("Initializing server connections")
        self.connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
        self.channel = self.connection.channel()
        
        #Exchanges para poder comunicarse con los hospitales y los pacientes
        self.channel.exchange_declare(exchange='patients', exchange_type='direct')
        self.channel.exchange_declare(exchange='hospitals', exchange_type='direct')
        
        #Colas para que los pacientes y los hospitales nos cuenten cosas
        self.channel.queue_declare(queue='patient_alerts')

        self.channel.basic_consume(queue='patient_alerts', on_message_callback=RabbitMQManager.consume_patient_message, auto_ack=True)

    @staticmethod
    @logger.catch
    def consume_patient_message(ch, method, properties, body):
        logger.info(f"{body}")
        request = json.loads(body)
        hospitals_dict = distance_module(request["lat"], request["lon"], 5)
        os.makedirs("audio_files", exist_ok=True)
        audiostring = base64.b64decode(request["audio"])
        with open(f"audio_files/{request['client_id']}.wav", "wb") as wavfile:        
            wavfile.write(audiostring)
        
        transcription = audio_model(f"audio_files/{request['client_id']}.wav")
        illness = disease_pred([{'diarrea'}])[0]

        alert_dict = {
            "user_id": request['client_id'],
            "alerted_hospitals": hospitals_dict,
            "audio_file": f"audio_files/{request['client_id']}.wav",
            "transcription": transcription["text"],
            "sickness_prediction": illness
        }

        logger.info(alert_dict)
    
    def start_listening(self):
        self.channel.start_consuming()
    
    def stop(self):
        self.channel.close()



#db_api = DBModule()

#async def get_transcription(client_id, lat, lon, audio):
#    hospitals_dict = distance_module(lat, lon, 5)
#    os.makedirs("audio_files", exist_ok=True)
#    audiostring = base64.b64decode(audio)
#    with open(f"audio_files/{client_id}.wav", "wb") as wavfile:
#        wavfile.write(audiostring)
#    
#    transcription = audio_model(f"audio_files/{client_id}.wav")
#    illness = disease_pred([{'diarrea'}])[0]
#
#    alert_dict = {
#        "user_id": client_id,
#        "alerted_hospitals": hospitals_dict,
#        "audio_file": f"audio_files/{client_id}.wav",
#        "transcription": transcription["text"],
#        "sickness_prediction": illness
#    }
#
#    ##Tenemos que mandar alertas a los hospitales
#    #db_api.post('/alerts', alert_dict)
#
#    return {"status":"correct"}

#async def rbmq_test():
#    rbmq_manager.send_message(message='El paciente esta malito')
#    return {"message": "ok"}

#def app():
    #audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
    #distance_module = Hosp_Dist_Calc("data/datos_hospitales.csv")
    #disease_pred = DiseasePredictor()
    
def launch():
    try:
        rbmq_manager = RabbitMQManager()
        rbmq_manager.start_listening()
    except KeyboardInterrupt:
        logger.warning('Interrupted')
        try:
            rbmq_manager.stop()
            sys.exit(0)
        except SystemExit:
            rbmq_manager.stop()
            os._exit(0)

if __name__ == "__main__":
    launch()