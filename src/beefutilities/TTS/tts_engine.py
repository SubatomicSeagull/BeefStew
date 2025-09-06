from io import BytesIO
import os
import pyttsx3
import discord
import datetime
from beefutilities.IO import file_io
from beefcommands.events.tasks.cleanup_tts import cleanup_tts_folder


import wave
from piper import PiperVoice

async def generate_speech(text):
    filename = file_io.construct_data_path("temp_tts_data", f"output-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav")
    voice = PiperVoice.load("C:\\Users\\jamie\\Downloads\\en_GB-alan-low.onnx")
    audio_binary = BytesIO()

    wav = wave.open(filename, "wb")
    
    wav = voice.synthesize_wav(text, wav_file)
    
    
    
    with wave.open(filename, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    

    return audio_binary
    
    return filepath

async def init_tts_engine():
    # initialise TTS engine
    engine = pyttsx3.init()
    # retrieve installed voices
    voices = engine.getProperty('voices')
    
    
    # set the default voice
    engine.setProperty("voice", voices[0].id)

    
    # checks of the ivy voice is installed    
    for voice in voices:
        print(voice.name.lower())
        if "ivona 2 ivy" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    # set the default rate and volume
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    return engine


async def Xgenerate_speech(text):
    tts = await init_tts_engine()
    
    await cleanup_tts_folder()
    
    filename = os.path.join(file_io.construct_data_path(), "temp_tts_data", f"output-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.wav")
    
    tts.save_to_file(text, filename)
    tts.runAndWait()
    
    filepath = file_io.construct_root_path(filename)
    
    return filepath



# list all installed voices
#for i, v in enumerate(voices):
#    print(f"{i}: {v.id} - {v.name} ({v.languages})")
    



