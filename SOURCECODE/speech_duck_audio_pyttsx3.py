import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import pyttsx3

def search_duckduckgo(query):
    search_url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results

def text_to_speech(text):
    text_speech = pyttsx3.init()
    voices = text_speech.getProperty('voices')
    text_speech.setProperty('voice', voices[1].id)
    text_speech.setProperty('rate', 150)
    text_speech.say(text)
    text_speech.runAndWait()

def main():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Say something...")
            audio = recognizer.listen(source, timeout=60)

        query = recognizer.recognize_google(audio, language='en-IN')
        print("Recognized:", query)

        search_results = search_duckduckgo(query)
        if 'AbstractText' in search_results and search_results['AbstractText']:
            first_result = search_results['AbstractText']
        elif 'RelatedTopics' in search_results and search_results['RelatedTopics']:
            first_result = search_results['RelatedTopics'][0]['Text']
        else:
            first_result = "Sorry, I couldn't find any relevant information."

        print(f"First search result: {first_result}")
        text_to_speech(first_result)

    except sr.WaitTimeoutError:
        print("Timeout: No speech detected within the timeout period.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except Exception as e:
        print("Error: {0}".format(e))

if __name__ == "__main__":
    main()
