import json
import os
import re
import time
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import wave
import pyttsx3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def record_audio_to_file(duration=5, fs=16000):
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    byte_io = io.BytesIO()
    with wave.open(byte_io, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    byte_io.seek(0)
    return byte_io

class VoiceIO:
    def __init__(self, config_path=None):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        # load config for language/voice if provided
        self.config = {}
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        self.language = self.config.get("language", "fr-FR")
        # Optional TTS tuning
        rate = self.config.get("tts_rate", 150)
        try:
            self.engine.setProperty("rate", rate)
        except Exception:
            pass

    def speak(self, text: str):
        print(f"Bot: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            # fallback to printing only
            pass

    def listen(self, prompt: Optional[str] = None, timeout: int = 6, phrase_time_limit: int = 10) -> Optional[str]:
        if prompt:
            self.speak(prompt)
        audio_file = record_audio_to_file(duration=timeout)
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

# simple validators
def validate_phone(number: str) -> bool:
    if not number:
        return False
    digits = re.sub(r"\D", "", number)
    return 7 <= len(digits) <= 15

def send_email(config: dict, phone_number: str):
    smtp_server = config.get("smtp_server")
    smtp_port = config.get("smtp_port")
    smtp_username = config.get("smtp_username")
    smtp_password = config.get("smtp_password")
    sender_email = config.get("sender_email")
    receiver_email = config.get("receiver_email") or sender_email

    if not smtp_server or not smtp_port or not sender_email:
        print("Email not sent: SMTP not configured in config.json")
        return False

    subject = "User Information from VoiceBot"
    body = f"Phone Number: {phone_number}\nTimestamp: {time.ctime()}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port), timeout=10) as server:
            server.starttls()
            if smtp_username and smtp_password:
                server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

class VoiceBot:
    def __init__(self, config_path=None):
        self.io = VoiceIO(config_path=config_path)
        self.config = {}
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        self.state = "purpose"
        self._collected = {"purpose": None, "phone": None}
        self.questions = {
            "purpose": "Quel est le but de votre appel?",
            "phone": "Quel est votre numéro de téléphone?",
            "confirm": "Confirmez-vous que les informations sont correctes? Dites oui pour valider ou non pour recommencer.",
            "finished": "Merci d'avoir fourni les informations. Votre demande est en cours de traitement."
        }

    def _ask(self, key):
        return self.questions.get(key, "")

    def _handle_response(self, text: Optional[str]):
        if not text:
            return False, "Je n'ai pas bien entendu. Voulez-vous répéter?"
        if self.state == "purpose":
            self._collected["purpose"] = text
            self.state = "phone"
            return True, None
        if self.state == "phone":
            if validate_phone(text):
                self._collected["phone"] = text
                self.state = "confirm"
                return True, None
            else:
                return False, "Numéro invalide. Pouvez-vous répéter votre numéro de téléphone?"
        if self.state == "confirm":
            low = text.lower()
            if "oui" in low or "yes" in low:
                self.state = "finished"
                return True, None
            else:
                # restart collection
                self.state = "purpose"
                self._collected = {"purpose": None, "phone": None}
                return True, "D'accord, reprenons depuis le début."

        return False, "Etat inconnu."

    def run(self):
        # main loop
        retry_count = 0
        while self.state != "finished":
            prompt = self._ask(self.state)
            heard = self.io.listen(prompt=prompt)
            ok, message = self._handle_response(heard)
            if not ok:
                retry_count += 1
                if retry_count >= 3:
                    self.io.speak("Trop d'erreurs. Veuillez réessayer plus tard.")
                    return
                if message:
                    self.io.speak(message)
                continue
            retry_count = 0
            # if message present (e.g., restart notice), speak it
            if message:
                self.io.speak(message)
        # finished: send email if configured
        self.io.speak(self._ask("finished"))
        send_email(self.config, self._collected["phone"])
        return self._collected