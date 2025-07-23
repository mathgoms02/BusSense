from gtts import gTTS
import os

class TextTSpeech():
    def __init__(self, text):
        self.text = text

    def convert_to_speech(self):
        tts = gTTS(text=self.text, lang='pt-br')
        tts.save("audio/model_output.mp3")

        os.system("mpg123 audio/model_output.mp3")
