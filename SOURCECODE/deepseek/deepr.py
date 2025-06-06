import requests
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# DeepSeek API Configuration
API_KEY = "sk-ca460cb204004c93aeec30e048a4f4d2"
BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def search_deepseek(query):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": query},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error fetching search results: {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust speech rate
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)  # Change voice if needed
    engine.say(text)
    engine.runAndWait()

def main():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Say something...")
            audio = recognizer.listen(source, timeout=60)

        query = recognizer.recognize_google(audio, language="en-IN")
        print("Recognized:", query)

        deepseek_result = search_deepseek(query)

        print(f"DeepSeek Result: {deepseek_result}")
        text_to_speech(deepseek_result)

    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Speech Recognition error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
