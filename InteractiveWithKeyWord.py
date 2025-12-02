import speech_recognition as sr
import pyttsx3
from voicebot_core import VoiceIO

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
        
        return "Bot: Merci d'avoir fourni les informations. Votre demande est en cours de traitement."

    else:
        return "Bot: Désolé, je n'ai pas compris. Pourriez-vous répéter?"

def text_to_speech(text):
    engine = pyttsx3.init()

    # Set the language to French
    engine.setProperty("rate", 150)  # Adjust the speed if needed
    engine.setProperty("voice", "french")
    
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

def find_keyword(text: str):
    kws = {
        "aide": "Je peux vous aider avec les informations de compte, facturation ou assistance technique.",
        "urgence": "Si c'est une urgence, veuillez contacter les services d'urgence locaux.",
        "facture": "Je peux vous donner le statut de votre facture si vous fournissez votre identifiant client.",
        "email": "D'accord, je vais vous demander votre adresse e-mail."
    }
    txt = (text or "").lower()
    for k, resp in kws.items():
        if k in txt:
            return resp
    return None

# Initialize state
current_state = "purpose"

# Main loop
while current_state != "finished":
    user_input = get_user_response()
    if user_input:
        response = process_input(user_input)
        if response:
            text_to_speech(response)

def main():
    io = VoiceIO(config_path=None)
    io.speak("Bonjour, dites un mot-clé pour commencer (par ex. aide, facture, urgence).")
    while True:
        heard = io.listen(prompt=None)
        if not heard:
            io.speak("Je n'ai pas entendu. Voulez-vous réessayer ?")
            continue
        if heard.lower().strip() in ("quit", "exit", "stop", "au revoir"):
            io.speak("Au revoir.")
            break
        resp = find_keyword(heard)
        if resp:
            io.speak(resp)
        else:
            io.speak("Mot-clé non reconnu. Dites aide, facture ou urgence.")

if __name__ == "__main__":
    main()
