from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition as sr
import pyttsx3
import spacy

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("You: ")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None

# Function to convert text to speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Create a new chat bot
bot = ChatBot('MyBot')

# Create a new trainer for the chat bot
trainer = ChatterBotCorpusTrainer(bot)

# Train the chat bot on English language data
trainer.train('chatterbot.corpus.english')

# Main loop for interaction
while True:
    # Get user input
    user_input = recognize_speech()

    # Exit the loop if the user says 'exit'
    if user_input and user_input.lower() == 'exit':
        print("Bot: Goodbye!")
        break

    # Get the bot's response
    bot_response = bot.get_response(user_input)
    
    # Print and speak the bot's response
    print(f"Bot: {bot_response}")
    text_to_speech(bot_response)
