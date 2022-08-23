from transformers import pipeline

class AudioTranscription:
    def __init__(self, model_name) -> None:
        self.pipe = pipeline(model=model_name)
        
                
    def __call__(self, audio_path):
        output = self.pipe(audio_path, chunk_length_s=10, stride_length_s=(4, 2))
        return output