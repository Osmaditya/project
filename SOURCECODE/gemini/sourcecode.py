# GEMINI WORKING WITH OBJECT DETECTION
from ultralytics import YOLO
import cv2
import cvzone
import math
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# -------------------- Gemini API Setup --------------------
genai.configure(api_key="AIzaSyDRHajxM61bp4h0G-WrmxcpEre-FSrZg14")  # Replace with your actual Gemini API key
model_gemini = genai.GenerativeModel('gemini-1.5-flash')  # Use 'gemini-1.5-pro' if needed

# -------------------- YOLO Model Setup --------------------
model = YOLO("yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "potted plant", "bed",
              "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cellphone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair dryer", "toothbrush"]

# -------------------- Gemini Search Function --------------------
def search_with_gemini(query):
    try:
        response = model_gemini.generate_content(query)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Sorry, I couldn't fetch results from Gemini."
    

# -------------------- Text to Speech --------------------
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# -------------------- Voice Input --------------------
def get_user_query():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        audio = recognizer.listen(source, timeout=10)
    try:
        query = recognizer.recognize_google(audio, language='en-IN')
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

# -------------------- Main Logic --------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    detected_objects = set()
    results = model(img, stream=True)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h), l=9)

            conf = round(float(box.conf[0]), 2)
            try:
                cls = int(box.cls[0])
                label = classNames[cls]
                detected_objects.add(label)
                cvzone.putTextRect(img, f'{label} {conf}', (max(0, x1), max(35, y1)))
            except Exception as e:
                print("Label Error:", e)

    cv2.imshow("Live Feed", img)

    if detected_objects:
        labels_text = ", ".join(detected_objects)
        text_to_speech(f"I detected: {labels_text}. Please name one to learn more.")
        selected_object = get_user_query()

        if selected_object:
            if selected_object.lower() in [obj.lower() for obj in detected_objects]:
                text_to_speech(f"You selected {selected_object}. Please ask a question.")
                user_question = get_user_query()
                if user_question:
                    full_query = f"{user_question} about {selected_object}"
                    print(f"Querying Gemini: {full_query}")
                    gemini_response = search_with_gemini(full_query)
                    print("Gemini Response:", gemini_response)
                    text_to_speech(gemini_response)
                else:
                    text_to_speech("Sorry, I couldn't understand your question.")
            else:
                text_to_speech("That object is not among the detected ones.")
    else:
        text_to_speech("No objects detected currently. Please wait.")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
