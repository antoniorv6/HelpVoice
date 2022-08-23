from glob import glob
import uvicorn
from fastapi import FastAPI
from Wav2Vec import AudioTranscription
from distance import Hosp_Dist_Calc
from db_connection import DBModule
import os
import base64

app = FastAPI()

audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
distance_module = Hosp_Dist_Calc("data/datos_hospitales.csv")
db_handler = None

@app.post("/transcribe_audio")
def get_transcription(client_id: str = "0", lat: float = 0.0, lon: float = 0.0 ,audio: str = ""):
    hospitals_dict = distance_module(lat, lon, 5)
    os.makedirs("audio_files", exist_ok=True)
    audiostring = base64.b64decode(audio)
    with open(f"audio_files/{client_id}.wav", "wb") as wavfile:
        wavfile.write(audiostring)
    transcription = audio_model(f"audio_files/{client_id}.wav")
    response_dict = {
        "hospitals": hospitals_dict,
        "transcription": transcription.text
    }
    return response_dict
    

    # Devuelve un diccionario con los datos de los 5 hospitales más cercanos
    # NOMBRE: nombre del hospital o centro de salud
    # LATITUD
    # LONGITUD
    # TELÉFONO
    # TIPO: centro de salud u hospital
    # DISTANCIA: distancia en km al hospital/centro de salud
    ## AQUÍ ACABA LO DE SANDRA



    return {"transcription":"ok"}

def launch():
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    launch()