from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor, QMouseEvent
from PyQt5.QtWidgets import QFrame, QLabel, QPushButton
from playsound import playsound


class MusicItem(QPushButton):
    click_signal = pyqtSignal(bool)
    def __init__(self, parent, name, theme, playlist):
        super(MusicItem, self).__init__(parent)

        self.musicName = QLabel(self)
        self.fileName = name
        self.isActive = False
        self.setObjectName("songFrame")
        self.theme = theme
        self.playlist = playlist
        self.name = name.split("/")[-1]
        self.name = self.name.split(".")[0]

        self.setupUI()


    def setupUI(self):
        self.musicName.setGeometry(29,10, 82, 30)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(55)
        self.musicName.setFont(font)
        self.musicName.setText(self.name)

        self.setCursor(QCursor(Qt.PointingHandCursor))

        if not self.playlist:
            self.setObjectName("songFrame")
        else:
            self.setObjectName("songFramePlaylist")

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self.isActive = (not self.isActive)

        if self.isActive:
            self.json2style(self, "pressed")
        else:
            self.json2style(self, "default")
        playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\ui_tap-variant-02.wav")

        self.click_signal.emit(self.isActive)

    def getName(self):
        return self.name

    def getPath(self):
        return self.fileName

    def setName(self, name):
        self.name = name
        print(self.name)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(55)
        self.musicName.setFont(font)
        self.musicName.setText(self.name)

    def json2style(self, element, action):
        styleValue = ""

        styleJson = self.theme[element.objectName()][action]

        for style in styleJson:
            styleValue += style["name"] + ":"+style["value"]+";"

        element.setStyleSheet(styleValue)

    def thread_function(self,name):
        print("Thread %s: starting", name)
        playsound('D:\\SEM_2\\IOC\\proiect\\buttonSound\\button-error.wav')
        print("Thread %s: finishing", name)

    def play(self):

        playsound(self.fileName)
