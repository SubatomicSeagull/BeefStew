from io import BytesIO
from beefutilities.IO import file_io
import wave
import enum
from piper import PiperVoice
import os

global _voice
_voice = None

async def generate_speech(text):
    audio_binary = BytesIO()
    
    with wave.open(audio_binary, "wb") as wav_file:
        _voice.synthesize_wav(text, wav_file)
    
    audio_binary.seek(0)
    return audio_binary

def set_voice(voicefile):
    global _voice
    _voice = PiperVoice.load(file_io.construct_data_path("tts_voices", f"{voicefile}"))

def get_voice():
    return _voice

def generate_voice_enum():
    voices_dir = file_io.construct_data_path("tts_voices")
    enum_dict = {}
    for file in os.listdir(voices_dir):
        if file.endswith(".onnx"):
            human_name = _read_onnx_name_sync(file)
            enum_dict[human_name] = file
    return enum.Enum("VoiceList", enum_dict)

def _read_onnx_name_sync(file):
    name, _ = os.path.splitext(file)
    name = name.replace("_", " ").replace("-", " ")
    return " ".join(word.capitalize() for word in name.split())