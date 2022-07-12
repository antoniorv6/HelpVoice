import logging
import torchaudio
import torch
import transformers
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class AudioTranscription:
    def __init__(self, model_name) -> None:
        self.logger = logging.getLogger(__name__)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name).to(self.device)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.resampler = torchaudio.transforms.Resample(orig_freq=48_000, new_freq=16_000)
        self.logger.info("Wav2Vec correctly loaded!")
                
    def __call__(self, audioStream):
        
        audio_tensor = self.processor(audioStream, sampling_rate=16, padding=True, return_tensors="pt")
        x = audio_tensor.input_values.to(self.device)
        attention_mask = audio_tensor.attention_mask.to(self.device)
        with torch.no_grad():
            logits = self.model(x, attention_mask=attention_mask).logits
        
        pred_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(pred_ids)
        
        return transcription