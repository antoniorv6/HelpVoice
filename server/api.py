from glob import glob
import uvicorn
from rbmq import RabbitMQManager
from db_connection import DBModule
import os
import base64
import sys


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
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    launch()