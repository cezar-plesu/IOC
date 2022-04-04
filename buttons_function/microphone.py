import speech_recognition as sr
import pyttsx3
from datetime import datetime

from playsound import playsound



class MicrophoneFunc():
    def __init__(self):
        self.comands = ["play", "stop", "next", "help","hey", "add"]
        self.engine = pyttsx3.init()
        self.responses = ["yes","no"]
        self.siri = False
        self.start = None
        self.finish = None

    def speechToText(self, recognizer, microphone):
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.energy_threshold = 1000
            audio = recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"

        return response

    def enableSiri(self):
        self.siri = True
        self.start = datetime.now()
        # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\siri.mp3")


    def getSiri(self):
        return self.siri

    def getCommands(self):
        return self.comands

    def checkSiri(self):
        self.finish = datetime.now()
        result = (self.finish - self.start).seconds
        if result > 55:
            self.siri = False
            self.start = None
            self.finish = None
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\closeS.mp3")
        return result

    def forceStop(self):
        self.siri = False
        self.start = None
        self.finish = None

    def isProblem(self, instructions, once):
        comm = instructions.split(" ")[0]

        if comm not in self.comands:
            if once:
                self.textToSpeech("Command "+comm+" not found. Do you want to see instructions?")
            else:
                self.textToSpeech("Command " + comm + " not found.")
            return True
        return False

    def waitResponse(self, response): # 0 - wait again , 1 - no, 2 - yes
        if response not in self.responses:
            self.textToSpeech("Please answer with yes or no")
            return 0
        if response == 'no':
            return 1
        if response == 'yes':
            return 2

    def textToSpeech(self, myText):
        self.engine.say(myText)
        self.engine.runAndWait()
