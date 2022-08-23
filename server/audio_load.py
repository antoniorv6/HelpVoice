import base64
from pyexpat import model
from Wav2Vec import AudioTranscription
from transformers import pipeline
import torchaudio

def main():
    audiob64 = ""
    with open("audo_test.txt") as audio_txt:
        audiob64 = audio_txt.read()
    
    audiostring = base64.b64decode(audiob64)
    with open("temp.wav", "wb") as wavfile:
        wavfile.write(audiostring)
    
    pipe = pipeline(model="facebook/wav2vec2-large-xlsr-53-spanish")
    output = pipe("test.wav", chunk_length_s=10, stride_length_s=(4, 2))
    print(output)


    pass

if __name__ == "__main__":
    main()