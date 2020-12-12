import pyttsx3

def text_to_speech(txt):
    #intialize the engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    engine.say(txt)
    engine.runAndWait()
    del engine
