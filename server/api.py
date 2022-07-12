import uvicorn
from fastapi import FastAPI
from Wav2Vec import AudioTranscription

app = FastAPI()
audio_model = None

@app.post("/transcribe_audio")
def get_transcription():
    return {"transcription":"ok"}


def launch():
    audio_model = AudioTranscription("facebook/wav2vec2-large-xlsr-53-spanish") 
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    launch()