import speech_recognition as sr

class AudioCapture:
    def __init__(self):
        self.r = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Speak Something...")
            audio = self.r.listen(source, 5, 10)

            try:
                text = self.r.recognize_google(audio, language="pt-BR")
                print("You said: " + text)
                return text
            except sr.UnknownValueError:
                print("I didn't understand what you said")
            except sr.RequestError as e:
                print(f"Error accessing service: {e}")
