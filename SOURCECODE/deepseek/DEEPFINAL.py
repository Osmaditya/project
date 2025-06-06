# DEEPSEEK WORKING WITH OBJECT DETECTION

import requests
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# OpenRouter Client Setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Replace with your actual OpenRouter API Key
)

def search_deepseek(query):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://yourwebsite.com",  # Optional
                "X-Title": "VoiceSearchBot"  # Optional
            },
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": query}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error fetching search results: {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice (change if needed)
    engine.setProperty('rate', 150)  # Adjust speed
    engine.say(text)
    engine.runAndWait()

def main():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Say something...")
            audio = recognizer.listen(source, timeout=60)

        query = recognizer.recognize_google(audio, language='en-IN')
        print("Recognized:", query)

        first_result = search_deepseek(query)
        print(f"DeepSeek Result: {first_result}")

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
