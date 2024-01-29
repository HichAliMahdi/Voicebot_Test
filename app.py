import speech_recognition as sr
import pyttsx3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Bot: {get_question()}")
        text_to_speech(get_question())
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        print("Vous avez dit:", text)
        return text
    except sr.UnknownValueError:
        print("La reconnaissance vocale n'a pas compris l'audio")
        return None
    except sr.RequestError as e:
        print(f"Impossible de récupérer des résultats depuis l'API Google Web Speech : {e}")
        return None

def process_input(text):
    global current_state

    if current_state == "purpose":
        print("Bot: Génial! Quelle est votre adresse e-mail?")
        text_to_speech("Génial! Quelle est votre adresse e-mail?")
        current_state = "email"
        return None

    elif current_state == "email":
        print("Vous avez fourni votre adresse e-mail :", text)
        email = text
        current_state = "phone"
        return None

    elif current_state == "phone":
        print("Vous avez fourni votre numéro de téléphone :", text)
        phone_number = text
        current_state = "finished"
        
        # Send email
        send_email(email, phone_number)
        
        return "Bot: Merci d'avoir fourni les informations. Votre demande est en cours de traitement."

    else:
        return "Bot: Désolé, je n'ai pas compris. Pourriez-vous répéter?"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_user_response():
    while True:
        user_input = recognize_speech()
        if user_input:
            return user_input

def get_question():
    global current_state
    questions = {
        "purpose": "Quel est le but de votre appel?",
        "email": "Quelle est votre adresse e-mail?",
        "phone": "Quel est votre numéro de téléphone?",
        "finished": "Merci d'avoir fourni les informations. Votre demande est en cours de traitement."
    }
    return questions.get(current_state, "Désolé, une erreur s'est produite.")

def send_email(email, phone_number):
    # Update the following information with your email server details
    smtp_server = "oxxodata.net"
    smtp_port = 465
    smtp_username = "h.ali@oxxodata.net"
    smtp_password = "9R65?jzd"
    sender_email = "h.ali@oxxodata.net"
    receiver_email = "h.ali@oxxodata.com"

    subject = "User Information"
    body = f"Email: {email}\nPhone Number: {phone_number}"

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

# Initialize state
current_state = "purpose"

# Main loop
while current_state != "finished":
    user_input = get_user_response()
    if user_input:
        response = process_input(user_input)
        if response:
            text_to_speech(response)
