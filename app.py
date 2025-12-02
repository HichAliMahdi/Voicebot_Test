import os
from voicebot_core import VoiceBot

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(project_dir, "config.json")
    bot = VoiceBot(config_path=config_path)
    try:
        bot.run()
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting.")
