import pyttsx3
import speech_recognition as sr
import wikipedia


def speech(text):
    engine = engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def this_is_where_the_magic_happens(question):
    # speak("Searching...")
    result = wikipedia.summary(question, sentences=2)
    speech("According to Wikipedia")
    print(result)
    speech(result)


r = sr.Recognizer()
while (1):
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print("Did you say ", MyText)
            break
    except:
        print("Sorry! Didn't catch that, kindly speak again.")
this_is_where_the_magic_happens(MyText)
