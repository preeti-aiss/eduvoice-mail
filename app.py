

import streamlit as st
from huggingface_hub import InferenceApi
import speech_recognition as sr
import smtplib
from email.message import EmailMessage

# Hugging Face API setup
HF_API_KEY = "your_huggingface_api_key"


try:
    inference = InferenceApi(repo_id="google/flan-t5-small", token=HF_API_KEY)
    response = inference(inputs="Your input text here.")
except Exception as e:
    st.error(f"An error occurred: {e}")


def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except:
        st.error("Sorry, could not understand.")
        return ""

def polish_text(text):
    response = inference(inputs=f"Improve this email professionally: {text}")
    return response[0]['generated_text']

def send_email(to, subject, body):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

st.title("📚 EduVoice Mail")
if st.button("🎙️ Speak"):
    raw = capture_voice()
    st.session_state['raw'] = raw

if 'raw' in st.session_state:
    polished = polish_text(st.session_state['raw'])
    st.text_area("✅ Polished Email", value=polished, height=150)

to = st.text_input("Recipient Email")
subject = st.text_input("Subject")
body = st.session_state.get('raw', "")

if st.button("📤 Send"):
    if to and subject and body:
        send_email(to, subject, body)
        st.success("Email sent successfully!")
    else:
        st.error("All fields are required.")
