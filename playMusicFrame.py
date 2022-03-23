from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QLabel

from buttons import Buttons


class PlayMusicFrame(QFrame):
    def __init__(self, parent):
        super(PlayMusicFrame, self).__init__(parent)
        self.musicName = QLabel(self)
        self.buttonPlayStop = Buttons(self, "play.svg", 38, 38, "pause.svg")
        self.buttonNext = Buttons(self, "next.svg", 38, 38)
        self.path = None

        self.name = ""
        self.setupUI()

    def setupUI(self):
        self.setName("")
        self.musicName.setGeometry(QRect(80, 70, 135, 28))

        self.buttonPlayStop.setGeometry(98, 144, 38, 38)
        self.buttonNext.setGeometry(188, 144, 38, 38)

        # if self.buttonPlayStop.

    def getPlayStopButton(self):
        return self.buttonPlayStop

    def getButtonNext(self):
        return self.buttonNext

    def setPath(self, path):
        self.path = path

    def setName(self, name):
        self.name = name
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(35)
        self.musicName.setFont(font)
        self.musicName.setText(self.name)

        if name == "":
            self.buttonPlayStop.setWarningSound("error-sound.wav")
        else:
            self.buttonPlayStop.setWarningSound(None)
            self.buttonPlayStop.setSong(self.path)


    def getName(self):
        return self.name
