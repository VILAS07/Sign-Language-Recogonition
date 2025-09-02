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
import random
import subprocess
import pyjokes

# Initialize virtual assistant
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty('rate', 170)

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

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    
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
        if labels[index] == "HELLO":
            speak("Hello there how can i assist you today")

        elif labels[index] == "THANK YOU":
            speak("OPENING YOUTUBE")
            webbrowser.open("https://www.youtube.com/")
        elif labels[index] == "YES":
            os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk")
            
        
        # Display recognized sign gesture
        cv2.rectangle(imgOutput,(x-offset,y-offset-70),(x -offset+400, y - offset+60-50),(0,255,0),cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 2)
        cv2.rectangle(imgOutput, (x-offset,y-offset), (x + w + offset, y+h + offset), (0,255,0), 4)
        cv2.imshow('ImageCrop', imgCrop)
        cv2.imshow('ImageWhite', imgWhite)

    cv2.imshow('Image', imgOutput)
    cv2.waitKey(1)
