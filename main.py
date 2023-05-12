import pandas as pd
import re
import pyttsx3
import speech_recognition as sr

MyText = ''


def speech(text):
    engine = engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # getting details of current voice
    # engine.setProperty('voice', voices[0].id)  # changing index, changes voices. 0 for male
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def this_is_where_the_magic_happens(question):
    treatments_df = pd.read_csv("treatments_data.csv", encoding="latin1")
    treatments_df["Disease"] = treatments_df["Disease"].str.lower()
    symptoms_df = pd.read_csv("symptoms_data.csv", encoding="latin1")
    symptoms_df["Disease"] = symptoms_df["Disease"].str.lower()
    question = question.lower()
    match = re.search(r'\bsymptoms of (\w+)\b', question)
    if match:
        disease_name = match.group(1).lower()
        data = symptoms_df.loc[symptoms_df["Disease"]
                               == disease_name, "Symptoms"].iloc[0]
        ans = (f"The symptoms of {disease_name} are: {data}")
        print(ans)
        speech(ans)
    else:
        match = re.search(r'\btreatment of (\w+)\b', question)
        if match:
            disease_name = match.group(1).lower()
            data = treatments_df.loc[treatments_df["Disease"]
                                     == disease_name, "Treatment"].iloc[0]
            ans = (f"The treatment for {disease_name} is: {data}")
            print(ans)
            speech(ans)
        else:
            print("I'm sorry, I didn't understand your question.")
            speech("I'm sorry, I didn't understand your question.")


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
