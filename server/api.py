import uvicorn
from fastapi import FastAPI
from Wav2Vec import AudioTranscription
from Distancia_hospitales import Distancia_hospitales

app = FastAPI()
audio_model = None

@app.post("/transcribe_audio")
def get_transcription():

    ## AQUÍ VA LO DE SANDRA
    # data: dataframe con los datos 'datos_hospitales.csv', está en esta carpeta
    # lat_p: latitud de la ubicación del paciente
    # long_p: longitud de la ubicación del paciente

    # data = pd.read_csv('datos_hospitales.csv')
    distancia_hospitales = Distancia_hospitales(data, lat_p, long_p)
    # Devuelve un diccionario con los datos de los 5 hospitales más cercanos
    # NOMBRE: nombre del hospital o centro de salud
    # LATITUD
    # LONGITUD
    # TELÉFONO
    # TIPO: centro de salud u hospital
    # DISTANCIA: distancia en km al hospital/centro de salud
    hosp_centosSalud_cecanos = distancia_hospitales.dict_cercanos(5)
    ## AQUÍ ACABA LO DE SANDRA

    return {"transcription":"ok"}

def launch():
    audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    launch()