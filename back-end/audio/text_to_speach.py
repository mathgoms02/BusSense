from gtts import gTTS
import os
from config import constants

class TextTSpeech():
    def __init__(self, text):
        self.text = text

    def convert_to_speech(self):
        tts = gTTS(text=self.text, lang='pt-br')
        tts.save(constants.DEFAULT_AUDIO_OUTPUT)

        os.system("mpg123 " + constants.DEFAULT_AUDIO_OUTPUT)
