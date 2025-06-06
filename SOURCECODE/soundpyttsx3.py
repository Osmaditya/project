import pyttsx3
text_speech = pyttsx3.init()
voices = text_speech.getProperty('voices')
text_speech.setProperty('voice', voices[1].id)
text_speech.setProperty('rate', 150) 

answer="what do you want to search"
text_speech.say(answer)
text_speech.runAndWait()
'''
rate = text_speech.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
text_speech.setProperty('rate', 125) 
'''