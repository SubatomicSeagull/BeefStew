from io import BytesIO
from beefutilities.IO import file_io
import wave
from piper import PiperVoice

global _voice
_voice = None

async def generate_speech(text):
    audio_binary = BytesIO()
    
    with wave.open(audio_binary, "wb") as wav_file:
        _voice.synthesize_wav(text, wav_file)
    
    audio_binary.seek(0)
    return audio_binary

def set_voice(voice_id):
    pass

def get_voice():
    return _voice

# on init load the default voice
def load_voice():
    global _voice
    _voice = PiperVoice.load(file_io.construct_data_path("tts_voices", "rocket.onnx"))

