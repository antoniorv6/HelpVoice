from transformers import pipeline
from loguru import logger
class AudioTranscription:
    @logger.catch
    def __init__(self, model_name) -> None:
        self.pipe = pipeline(model=model_name)
        
    @logger.catch            
    def __call__(self, audio_path):
        output = self.pipe(audio_path, chunk_length_s=10, stride_length_s=(4, 2))
        return output