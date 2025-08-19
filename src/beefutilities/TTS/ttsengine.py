import pyttsx3

def init_tts_engine():
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

tts = init_tts_engine()

tts.save_to_file("I had a look and i cant find it im sorry :(", 'test.mp3')
tts.runAndWait()


# list all installed voices
#for i, v in enumerate(voices):
#    print(f"{i}: {v.id} - {v.name} ({v.languages})")
    



