import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pywhatkit
import time
from googletrans import Translator
import sys
import tkinter as tk
from tkinter import font
import pytesseract
from PIL import Image

# Initialize virtual assistant
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty('rate', 170)

def save_image(img, filename):
    cv2.imwrite(filename, img)
    speak(f"Screenshot saved as {filename}")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query

# Initialize sign language recognition
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model//keras_model.h5" , "Model//labels.txt")
offset = 20
imgSize = 300
labels = ["A","B","C","D","F","G","H","HELLO","L","O","THANK YOU","THUMBS","V","W","Y","YES"]

# Dictionary mapping sign gestures to messages or actions
gesture_messages = {
    "L": "hello .",
    "W": "I'm working right now, I'll message you later."
}

# Timer for controlling recognition rate
recognize_timer = time.time()

# Function to start the program
def start_program(recognize_timer):
    root.destroy()  # Close the GUI window
    while True:
        success, img = cap.read()
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        
        # Check if enough time has passed for recognition
        if time.time() - recognize_timer >= 1:  # Adjust recognition rate as needed
            recognize_timer = time.time()  # Reset the timer

            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]
                imgCropShape = imgCrop.shape
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize-wCal)/2)
                    imgWhite[:, wGap: wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap: hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                
                # Execute commands based on recognized sign gestures
                if labels[index] in gesture_messages:
                    speak("Sending WhatsApp message")
                    message = gesture_messages[labels[index]]
                    # Replace "+1234567890" with the recipient's phone number
                    pywhatkit.sendwhatmsg_instantly("+919746906494", message)

                elif labels[index] == "G":
                    speak("Sending WhatsApp message")
                    # Replace "+1234567890" with the recipient's phone number
                    pywhatkit.sendwhatmsg_instantly("+919746906494", "Thank you!")
                elif labels[index] == "Y":
                    speak("OPENING YOUTUBE")
                    webbrowser.open("https://www.youtube.com/")
                    print("Y")
                elif labels[index] == "HELLO":
                    speak("Hello there, how can I assist you today")
                    print("HELLO")
                elif labels[index] == "THUMBS":
                    speak("OK")
                    print("THUMBS")
                elif labels[index] == "D":
                     now = datetime.datetime.now()
                     current_time = now.strftime("%H:%M:%S")
                     current_date = now.strftime("%Y-%m-%d")
                     speak(f"The current time is {current_time} and the date is {current_date}")
                     print("D") 
                elif labels[index] == "A":
                     webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                     print("V")
                elif labels[index] == "O":
                     speak("Closing the program")
                     sys.exit()
                     print("O")
                elif labels[index] == "H":
                    os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk")
                elif labels[index] == "YES":  # Replace "YOUR_GESTURE" with the desired gesture
                     print("YES")
                     speak("Taking screenshot after 5 seconds...")
                     time.sleep(5)
                     save_image(imgOutput, "screenshot4.jpg")
                    

                # Display recognized sign gesture
                cv2.rectangle(imgOutput,(x-offset,y-offset-70),(x -offset+400, y - offset+60-50),(0,255,0),cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 2)
                cv2.rectangle(imgOutput, (x-offset,y-offset), (x + w + offset, y+h + offset), (0,255,0), 4)
                cv2.imshow('ImageCrop', imgCrop)
                cv2.imshow('ImageWhite', imgWhite)

        cv2.imshow('Image', imgOutput)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()                 
# Create the main window
root = tk.Tk()
root.title("Sign Language Virtual Assistant")
root.geometry("600x400")
root.configure(bg="#333333")

# Set custom font
custom_font = font.Font(family="Helvetica", size=16, weight="bold")

# Create the title label
title_label = tk.Label(root, text="Sign Language Virtual Assistant", font=custom_font, fg="white", bg="#333333")
title_label.pack(pady=20)

# Create the start button with a custom style
start_button = tk.Button(root, text="Start", font=custom_font, bg="#4CAF50", fg="white", command=lambda: start_program(recognize_timer))
start_button.pack(pady=20)

# Create the group members and guide name label
member_label = tk.Label(root, text="Group Members: Abhay das, Afin k sunny, Fathima ebrahim, Vilas pk\nGuide: Aswathy TS", font=custom_font, fg="white", bg="#333333")
member_label.pack(side=tk.BOTTOM, pady=20)

# Run the main event loop
root.mainloop()