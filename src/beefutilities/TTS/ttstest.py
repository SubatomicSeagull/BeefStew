
import pyttsx3
engine = pyttsx3.init()




voices = engine.getProperty('voices')

for i, v in enumerate(voices):
    print(f"{i}: {v.id} - {v.name} ({v.languages})")
    
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


engine.save_to_file('Hello, this is a test.', 'test.mp3')
engine.runAndWait()