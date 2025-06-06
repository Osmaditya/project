
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# Configure with your Gemini API key
genai.configure(api_key="AIzaSyDRHajxM61bp4h0G-WrmxcpEre-FSrZg14")

def search_gemini(query):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(query)
    return response.text.strip()

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty('rate', 150)
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

        result = search_gemini(query)
        print(f"Gemini Response: {result}")
        text_to_speech(result)

    except sr.WaitTimeoutError:
        print("Timeout: No speech detected within the timeout period.")
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
