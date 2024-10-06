from pathlib import Path

from openai import OpenAI


class TextToSpeech:
    def __init__(self, model="tts-1", voice="alloy"):
        self.client = OpenAI()
        self.model = model
        self.voice = voice

    def generate_speech(self, text, file_path= None):
        if not file_path:
            file_path = Path(__file__).parent / "speech.mp3"

        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            speed=1.25,
        )
        response.write_to_file(file_path)
        return file_path

