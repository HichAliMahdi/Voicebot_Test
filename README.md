# Voicebot Test

A modular voicebot system for interactive voice-based conversations, keyword detection, and information collection with email notification.

## Features

- Speech recognition (French/English)
- Text-to-speech responses
- Keyword-based interaction
- Guided information collection (purpose, email, phone)
- Email notification (configurable SMTP)
- Optional chatbot training (ChatterBot)

## Setup

1. **Clone or copy the repository files.**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Download spaCy language model:**
   ```bash
   python -m spacy download fr_core_news_sm
   ```

4. **Configure SMTP and language settings:**
   - Edit `config.json` and fill in your SMTP server details and preferred language.

## Files

- `app.py` — Main guided voicebot (purpose, email, phone, confirmation, email sending)
- `InteractiveWithKeyWord.py` — Keyword-based voice interaction
- `voicebot_core.py` — Core logic for speech I/O, validation, and bot state
- `interactiveTraining.py` — Optional ChatterBot training script
- `requirements.txt` — Python dependencies
- `config.json` — Configuration for SMTP and language
- `README.md` — This documentation

## Usage

### Guided Voicebot

```bash
python app.py
```

### Keyword Voicebot

```bash
python InteractiveWithKeyWord.py
```

### Chatbot Training (optional)

```bash
python interactiveTraining.py
```

## Configuration

Edit `config.json` to set:

- `language`: Speech recognition language code (e.g., "fr-FR")
- `tts_rate`: Speech speed (integer)
- `smtp_server`, `smtp_port`, `smtp_username`, `smtp_password`, `sender_email`, `receiver_email`: SMTP settings for email notification

## Notes

- Requires a working microphone.
- For email sending, valid SMTP credentials are needed.
- For ChatterBot, install and configure corpora as needed.

## Troubleshooting

- If `PyAudio` fails to install, use your OS package manager (e.g., `apt install portaudio19-dev` on Ubuntu) before running `pip install`.
- For speech recognition errors, check microphone permissions and internet connectivity.
