from imp import reload
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.post("/transcribe_audio")
def get_transcription():
    return {"transcription":"ok"}


def launch():
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    launch()