import cv2  # Import OpenCV library for computer vision
from cvzone.HandTrackingModule import HandDetector  # Import HandDetector from cvzone module for hand tracking
from cvzone.ClassificationModule import Classifier  # Import Classifier from cvzone module for hand gesture classification
import numpy as np  # Import numpy library for numerical operations
import math  # Import math library for mathematical operations
import pyttsx3  # Import pyttsx3 library for text-to-speech conversion
import speech_recognition as sr  # Import speech_recognition library for speech recognition
import datetime  # Import datetime library for handling date and time
import webbrowser  # Import webbrowser library for web browsing functionalities
import os  # Import os module for interacting with the operating system
import pywhatkit  # Import pywhatkit library for sending WhatsApp messages
import time  # Import time module for time-related functionalities
import sys  # Import sys module for system-specific parameters and functions
import tkinter as tk  # Import tkinter library for creating GUI applications
from tkinter import font  # Import font from tkinter for setting custom fonts
import pytesseract  # Import pytesseract library for OCR (Optical Character Recognition)
from PIL import Image  # Import Image module from PIL for working with images

# Initialize virtual assistant
engine = pyttsx3.init()  # Initialize text-to-speech engine
voices = engine.getProperty('voices')  # Get available voices
engine.setProperty('voice', voices[0].id)  # Set the voice
rate = engine.setProperty('rate', 170)  # Set the speaking rate

# Function to save image to file
def save_image(img, filename):
    cv2.imwrite(filename, img)  # Save image using OpenCV
    speak(f"Screenshot saved as {filename}")  # Speak confirmation message

# Function to speak text
def speak(audio):
    engine.say(audio)  # Speak the given text
    engine.runAndWait()  # Wait for speech to finish

# Function to recognize voice command
def takeCommand():
    r = sr.Recognizer()  # Initialize the recognizer
    with sr.Microphone() as source:
        print("Listening...")  # Print listening message
        r.pause_threshold = 1  # Set pause threshold
        r.energy_threshold = 300  # Set energy threshold
        audio = r.listen(source, 0, 4)  # Listen for audio input

    try:
        print("Recognizing...")  # Print recognizing message
        query = r.recognize_google(audio, language='en-in')  # Recognize speech using Google Speech Recognition
        print(f"You said: {query}\n")  # Print recognized speech
    except Exception as e:
        print("Say that again, please...")  # Print message if speech is not recognized
        return "None"  # Return "None" if speech is not recognized
    return query  # Return recognized speech

# Initialize sign language recognition
cap = cv2.VideoCapture(0)  # Initialize video capture
detector = HandDetector(maxHands=1)  # Initialize hand detector
classifier = Classifier("Model//keras_model.h5" , "Model//labels.txt")  #  hand gesture 
offset = 20  # Offset value for cropping hand region
imgSize = 300  # Size of resized image for classification
labels = ["A","B","C","D","F","G","H","HELLO","L","O","THANK YOU","THUMBS","V","W","Y","YES"]  

# Dictionary mapping sign gestures to messages or actions
gesture_messages = {
    "L": "hello .",  # Message for "L" gesture
    "W": "I'm working right now, I'll message you later."  # Message for "W" gesture
}

# Timer for controlling recognition rate
recognize_timer = time.time()  # Initialize recognition timer

# Function to start the program
def start_program(recognize_timer):
    root.destroy()  # Close the GUI window
    while True:
        success, img = cap.read()  # Read a frame from the video capture
        imgOutput = img.copy()  # Create a copy of the frame
        hands, img = detector.findHands(img)  # Detect hands in the frame
        
        # Check if enough time has passed for recognition
        if time.time() - recognize_timer >= 1:  # Adjust recognition rate as needed
            recognize_timer = time.time()  # Reset the timer

            if hands:  # If hands are detected
                hand = hands[0]  # Get the first detected hand
                x, y, w, h = hand['bbox']  # Get bounding box coordinates
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # Create a white image
                imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]  # Crop hand region from the frame
                imgCropShape = imgCrop.shape  # Get the shape of the cropped image
                aspectRatio = h / w  # Calculate aspect ratio of the hand

                if aspectRatio > 1:  # If aspect ratio is greater than 1
                    k = imgSize / h  # Calculate scaling factor
                    wCal = math.ceil(k * w)  # Calculate width after resizing
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))  # Resize the cropped image
                    imgResizeShape = imgResize.shape  # Get the shape of the resized image
                    wGap = math.ceil((imgSize-wCal)/2)  # Calculate gap for centering
                    imgWhite[:, wGap: wCal + wGap] = imgResize  # Place resized image in white image
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)  # Get prediction from classifier
                else:  # If aspect ratio is less than or equal to 1
                    k = imgSize / w  # Calculate scaling factor
                    hCal = math.ceil(k * h)  # Calculate height after resizing
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))  # Resize the cropped image
                    imgResizeShape = imgResize.shape  # Get the shape of the resized image
                    hGap = math.ceil((imgSize - hCal) / 2)  # Calculate gap for centering
                    imgWhite[hGap: hCal + hGap, :] = imgResize  # Place resized image in white image
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)  # Get prediction from classifier
                
                # Execute commands based on recognized sign gestures
                if labels[index] in gesture_messages:  # If the recognized gesture is in gesture_messages dictionary
                    speak("Sending WhatsApp message")  # Speak message
                    message = gesture_messages[labels[index]]  # Get message corresponding to the gesture
                    pywhatkit.sendwhatmsg_instantly("+919746906494", message)  # Send WhatsApp message

                elif labels[index] == "G":  # If the recognized gesture is "G"
                    speak("Sending WhatsApp message")  # Speak message
                    pywhatkit.sendwhatmsg_instantly("+919746906494", "Thank you!")  # Send WhatsApp message
                elif labels[index] == "Y":  # If the recognized gesture is "Y"
                    speak("OPENING YOUTUBE")  # Speak message
                    webbrowser.open("https://www.youtube.com/")  # Open YouTube in the default web browser
                    print("Y")  # Print message
                elif labels[index] == "HELLO":  # If the recognized gesture is "HELLO"
                    speak("Hello there, how can I assist you today")  # Speak message
                    print("HELLO")  # Print message
                elif labels[index] == "THUMBS":  # If the recognized gesture is "THUMBS"
                    speak("OK")  # Speak message
                    print("THUMBS")  # Print message
                elif labels[index] == "D":  # If the recognized gesture is "D"
                     now = datetime.datetime.now()  # Get current date and time
                     current_time = now.strftime("%H:%M:%S")  # Format current time
                     current_date = now.strftime("%Y-%m-%d")  # Format current date
                     speak(f"The current time is {current_time} and the date is {current_date}")  # Speak current time and date
                     print("D")  # Print message
                elif labels[index] == "A":  # If the recognized gesture is "A"
                     webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Open a YouTube video
                     print("A")  # Print message
                elif labels[index] == "O":  # If the recognized gesture is "O"
                     speak("Closing the program")  # Speak message
                     sys.exit()  # Exit the program
                     print("O")  # Print message
                elif labels[index] == "H":  # If the recognized gesture is "H"
                    os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk")  # Open Microsoft Edge
                elif labels[index] == "YES":  # If the recognized gesture is "YES"
                     print("YES")  # Print message
                     speak("Taking screenshot after 5 seconds...")  # Speak message
                     time.sleep(5)  # Wait for 5 seconds
                     save_image(imgOutput, "screenshot4.jpg")  # Save screenshot

                # Display recognized sign gesture
                cv2.rectangle(imgOutput,(x-offset,y-offset-70),(x -offset+400, y - offset+60-50),(0,255,0),cv2.FILLED)  # Draw rectangle for gesture label
                cv2.putText(imgOutput, labels[index], (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,0), 2)  # Put text for gesture label
                cv2.rectangle(imgOutput, (x-offset,y-offset), (x + w + offset, y+h + offset), (0,255,0), 4)  # Draw rectangle around hand region
                cv2.imshow('ImageCrop', imgCrop)  # Display cropped hand region
                cv2.imshow('ImageWhite', imgWhite)  # Display resized hand region

        cv2.imshow('Image', imgOutput)  # Display the output image
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Wait for 'q' key to exit
            break

    cap.release()  # Release the video capture
    cv2.destroyAllWindows()  # Close all OpenCV windows

# Create the main window
root = tk.Tk()  # Initialize tkinter
root.title("Sign Language Virtual Assistant")  # Set window title
root.geometry("600x400")  # Set window size
root.configure(bg="#333333")  # Set window background color

# Set custom font
custom_font = font.Font(family="Helvetica", size=16, weight="bold")

# Create the title label
title_label = tk.Label(root, text="Sign Language Virtual Assistant", font=custom_font, fg="white", bg="#333333")
title_label.pack(pady=20)  # Pack the title label

# Create the start button with a custom style
start_button = tk.Button(root, text="Start", font=custom_font, bg="#4CAF50", fg="white", command=lambda: start_program(recognize_timer))
start_button.pack(pady=20)  # Pack the start button

# Create the group members and guide name label
member_label = tk.Label(root, text="Group Members: Abhay das, Afin k sunny, Fathima ebrahim, Vilas pk\nGuide: Aswathy TS", font=custom_font, fg="white", bg="#333333")
member_label.pack(side=tk.BOTTOM, pady=20)  # Pack the member label

# Run the main event loop
root.mainloop()  # Start the tkinter event loop
