# Drowsiness Detection System 🧠😴  
**Made by Raghunandan Sahani**

---

## 📌 Project Overview

This is a real-time **Drowsiness and Yawning Detection System** built using **Python**, **OpenCV**, and **MediaPipe**. It uses facial landmarks to monitor eye blinks and mouth movement. If your eyes remain closed for too long or you start yawning — the system immediately gives a **voice alert** to wake you up or ask you to take a break.

This project is designed to help prevent **accidents due to fatigue**, especially for drivers, security staff, and even students during long study hours.

---

## 🧠 Features

- **Drowsiness detection** using Eye Aspect Ratio (EAR)
- **Yawn detection** using lip distance
- **Voice alerts** using `pyttsx3` (offline text-to-speech)
- No external models required (no dlib!)
- Runs completely offline and in real time

---

## 🔧 Tech Stack

- **Python 3**
- **OpenCV** – for capturing and displaying webcam frames
- **MediaPipe** – for face landmark detection
- **Scipy & Numpy** – for geometric calculations
- **pyttsx3** – for speaking alerts (works on Windows too!)

---

## 🗂️ Project Files

Drowsiness-Detection-System/
├── drowsiness.py # Main Python script
├── requirements.txt # List of required packages 
└── README.md # Project documentation 



---

## 🖥️ How to Run the Project

### 1. Install Python libraries
Open your terminal or command prompt and run:

pip install -r requirements.txt

Run the application
Make sure your webcam is connected, then run:

Run the python file 

drowsiness.py


Press Q anytime to quit the program.
