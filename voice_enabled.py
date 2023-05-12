import pandas as pd
import re
import pyttsx3
import speech_recognition as sr
import tkinter as tk

window = tk.Tk()
window.title("Chatbot")


def speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # getting details of current voice
    # changing index, changes voices. 1 for female
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
        ans = f"The symptoms of {disease_name} are: {data}"
        print(ans)
        speech(ans)
        response_label.config(text=ans)
    else:
        match = re.search(r'\btreatment of (\w+)\b', question)
        if match:
            disease_name = match.group(1).lower()
            data = treatments_df.loc[treatments_df["Disease"]
                                     == disease_name, "Treatment"].iloc[0]
            ans = f"The treatment for {disease_name} is: {data}"
            print(ans)
            speech(ans)
            response_label.config(text=ans)
        else:
            ans = "I'm sorry, I didn't understand your question."
            print(ans)
            speech(ans)
            response_label.config(text=ans)


def get_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
        try:
            input_query = r.recognize_google(audio).lower()
            input_label.config(text=f"You said: {input_query}")
            this_is_where_the_magic_happens(input_query)
        except sr.UnknownValueError:
            response_label.config(text="Sorry, I did not understand that.")
        except sr.RequestError as e:
            response_label.config(
                text="Could not request results from Google Speech Recognition service; {0}".format(e))


input_label = tk.Label(
    window, text="Click the Speak button to ask a question", font=("Helvetica", 16))
input_label.pack(pady=20)

speak_button = tk.Button(window, text="Speak", font=(
    "Helvetica", 14), command=get_input)
speak_button.pack(pady=10)

response_label = tk.Label(window, text="", font=("Helvetica", 16))
response_label.pack(pady=20)

window.mainloop()
