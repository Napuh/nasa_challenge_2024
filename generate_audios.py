# from pages.increase_in_global_temperature import intro_messages
from pathlib import Path

from dotenv import load_dotenv

from prompts.intro_messages_main_page import intro_text
from prompts.intro_messages_rising_temperatures import intro_messages
from prompts.video import transcript
from utils.tts import TextToSpeech

load_dotenv()


def generate_intro_audios():
    tts = TextToSpeech(model="tts-1-hd")

    entire_intro = "\n\n".join(msg for msg in intro_messages)

    audio_file_path = Path("./static/audio_intro_rising_temperatures.mp3")
    audio_path = tts.generate_speech(entire_intro, file_path=audio_file_path)
    print(f"Generated audio for rising temperature intro page: {audio_path}")

    audio_file_path = Path("./static/audio_intro_main_page.mp3")
    audio_path = tts.generate_speech(intro_text, file_path=audio_file_path)
    print(f"Generated audio for main intro page: {audio_path}")

    audio_file_path = Path("./static/final_video_audio.mp3")
    audio_path = tts.generate_speech(transcript, file_path=audio_file_path)
    print(f"Generated audio final video: {audio_path}")


if __name__ == "__main__":
    generate_intro_audios()
