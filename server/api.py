from glob import glob
from turtle import distance
from fastapi import Form
import uvicorn
from fastapi import FastAPI
from Wav2Vec import AudioTranscription
from distance import Hosp_Dist_Calc
from DiseasePredictor import DiseasePredictor
from db_connection import DBModule
import os
import base64

audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
distance_module = Hosp_Dist_Calc("data/datos_hospitales.csv")
disease_pred = DiseasePredictor()
app = FastAPI()

@app.post("/transcribe_audio")
async def get_transcription(client_id: int = Form(), lat: float = Form(), lon: float = Form() , audio: str=Form()):
    hospitals_dict = distance_module(lat, lon, 5)
    os.makedirs("audio_files", exist_ok=True)
    audiostring = base64.b64decode(audio)
    with open(f"audio_files/{client_id}.wav", "wb") as wavfile:
        wavfile.write(audiostring)
    
    transcription = audio_model(f"audio_files/{client_id}.wav")
    illness = disease_pred([{'diarrea'}])[0]

    response_dict = {
        "hospitals": hospitals_dict,
        "transcription": transcription["text"],
        "sick": illness
    }
    return response_dict

def launch():
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    launch()