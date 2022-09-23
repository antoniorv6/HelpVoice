import whisper
from loguru import logger
class AudioTranscription:
    @logger.catch
    def __init__(self, model_name) -> None:
        self.model = whisper.load_model("base")
        
    @logger.catch            
    def __call__(self, audio_path):
        output = self.model.transcribe(audio_path)
        return output