
#python program to convert text to sppech
# speech to txt and txt to speech

import speech_recognition as sr
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

def speech_to_text():
    r = sr.Recognizer() # Initialize recognizer class (for recognizing the speech)
    m = sr.Microphone()
    # Reading Microphone as source
    try:
    
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))

            print("Say something!")

            # listening the speech and store in audio variable
        with m as source :
            audio = r.listen(source)
            text_to_speech("Got it! Recognizing voice....")

            # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            value = r.recognize_google(audio)
            text_to_speech("You said "+ value)
            print("You said {}".format(value))
            # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
          
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
        return str(r.recognize_google(audio))
    except  KeyboardInterrupt:
        pass 

