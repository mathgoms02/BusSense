import os
import pandas as pd
import google.generativeai as genai
from audio_capture.audio_capture import AudioCapture
from audio_output.text_to_speach import TextTSpeech

class GeminiThinking:
    def __init__(self, api_key: str, routes_data: pd.DataFrame):
        if not api_key:
            raise ValueError("API key is mandatory! Check your .env file.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

        self.recorder = AudioCapture()
        self.routes_data = routes_data
        self.tts = None
    
    def generate_prompt(self, user_input):
        json_data = self.routes_data.to_json(orient='records')

        prompt = f"""
        You are an expert public transport assistant, you need to know all Bus Routes, who is good at say the bests routes depending where the user need to go.
        If the user need to go to someplace so far to RouteStart, put two or more routes, to get the RouteEnd
        In your output, only return the best route - which is provided between three backticks.
        Your task is to tell the best route to user, telling the RouteCode as 'Linha' (this code is the Bus Code too), the RouteStart as 'Ponto Inicial' and the RouteEnd as 'Ponto Final'.
        Your output must be without backticks.
        You need to awnser the 'user requisition'.
        ```
        {json_data}
        ```

        User requisition: {user_input}
        """

        return prompt
    
    def run(self):
        user_audio = self.recorder.listen()

        if not user_audio:
            print("Audio not detected!")
            raise Exception
        
        prompt = self.generate_prompt(user_audio)

        response = self.model.generate_content(prompt)
        response_text = response.text.strip()

        self.tts = TextTSpeech(response_text)
        self.tts.convert_to_speech()
