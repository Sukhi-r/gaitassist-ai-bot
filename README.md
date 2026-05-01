# NeuroStep – GaitAssist AI Chatbot

## Overview

NeuroStep is a web-based chatbot designed to provide information related to gait analysis and its applications in healthcare. The system enables users to ask questions about gait patterns, sensors, machine learning techniques, and related medical conditions through an interactive interface.

The chatbot uses Natural Language Processing techniques to understand user queries and return the most relevant responses from a predefined knowledge base. It also includes voice output to enhance user interaction.

---

## Objectives

* To develop an interactive chatbot for gait-related information
* To demonstrate the application of NLP in healthcare systems
* To provide a simple and user-friendly interface
* To enable voice-based response for better accessibility

---

## Technologies Used

* Python (Flask) for backend development
* HTML, CSS, and JavaScript for frontend design
* TF-IDF Vectorization for text processing
* Cosine Similarity for response matching
* Web Speech API for voice output

---

## System Working

1. The user enters a query through the web interface
2. The input is processed and converted into a vector using TF-IDF
3. Cosine similarity is calculated between the user query and stored questions
4. The most relevant answer is selected from the dataset
5. The response is displayed and converted into speech

---

## Features

* Chat-based interaction
* NLP-based response generation
* Voice output support
* Lightweight and fast system
* Offline functionality without external APIs

---

## Project Structure

gaitassist-ai-bot/
│
├── app.py
├── chatbot.py
├── dataset.json
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css

---

## Installation and Setup

1. Install required dependencies:
   pip install flask scikit-learn

2. Run the application:
   python app.py

3. Open the browser and navigate to:
   http://127.0.0.1:5000/

---

## Limitations

* The chatbot relies on a predefined dataset and cannot handle unknown queries effectively
* It does not use advanced deep learning models
* Voice output depends on browser compatibility

---

## Future Scope

* Integration with real-time gait sensor data
* Use of advanced machine learning or deep learning models
* Development of a mobile application
* Integration with clinical and healthcare systems

---

## Conclusion

This project demonstrates the use of Natural Language Processing and web technologies to build an interactive chatbot for healthcare-related applications. It highlights how AI-based systems can be used to improve accessibility and awareness in the domain of gait analysis.
