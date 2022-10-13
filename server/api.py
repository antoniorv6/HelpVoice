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
audio_model = AudioTranscription() 
distance_module = Hosp_Dist_Calc("data/datos_hospitales.csv")
disease_pred = DiseasePredictor()
#db_api = DBModule()
logger.success("Server add-ons initialized correctly")

class RabbitMQManager:
    @logger.catch
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(pika.URLParameters('amqps://tzpumyto:JSCw3UBKC1mnpUPgqZ_S8miEAKLXuiVQ@rat.rmq2.cloudamqp.com/tzpumyto'))
        self.channel = self.connection.channel()
        
        #Exchanges para poder comunicarse con los hospitales y los pacientes
        self.channel.exchange_declare(exchange='patients', exchange_type='direct')
        self.channel.exchange_declare(exchange='hospitals', exchange_type='direct')
        
        #Colas para que los pacientes y los hospitales nos cuenten cosas
        self.channel.queue_declare(queue='patient_alerts')
        self.channel.queue_declare(queue='hospital_response')


        self.channel.basic_consume(queue='patient_alerts', on_message_callback=RabbitMQManager.consume_patient_message, auto_ack=True)
        self.channel.basic_consume(queue='hospital_response', on_message_callback=RabbitMQManager.consume_hospital_response, auto_ack=True)


    @staticmethod
    @logger.catch
    def consume_patient_message(ch, method, properties, body):
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
            "audio_file": f"audio_files/{request['client_id']}.wav",
            "transcription": transcription["text"],
            "sickness_prediction": illness,
            "level_int": 0,
            "level": "Prioridad alta",
            "lat":request["lat"],
            "lon":request["lon"]
        }

        ch.basic_publish(exchange='hospitals', routing_key='hospital1', body=json.dumps(alert_dict))

        logger.success("Patient alert processed correctly, obtained the following info")
        logger.info(alert_dict)
    
    @staticmethod
    @logger.catch
    def consume_hospital_response(ch, method, properties, body):
        jsondata = json.loads(body)
        ch.basic_publish(exchange=jsondata['user_id'], routing_key='', body=body)
        logger.success("Hospital response correctly redirected to user")
    
    def start_listening(self):
        logger.success("Server connections correctly initialized")
        self.channel.start_consuming()
    
    @logger.catch
    def stop(self):
        logger.info("Closing server...")
        if self.channel.is_open:
            self.channel.close()
    
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
            os._exit(0)

if __name__ == "__main__":
    launch()
