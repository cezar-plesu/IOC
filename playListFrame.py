from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QWidget, QLabel

from buttons import Buttons
from musicItem import MusicItem
from playMusicFrame import PlayMusicFrame


class PlayListFrame(QFrame):
    def __init__(self, parent, theme):
        super(PlayListFrame, self).__init__(parent)
        self.playMusicFrame = PlayMusicFrame(self)
        self.theme = theme
        self.buttonAdd2Play = Buttons(self, "addInList.svg", 46, 46)

        self.buttonError = Buttons(self, "warning.svg", 45, 45)
        self.errorMessage = QLabel(self)

        self.yPos = 70
        self.xPos = 362

        #predefinesc frame pt muzica
        j =0
        self.musicList = []

        for i in range(9):

            # print(str(i)+":\t"+str(self.yPos)+" "+str(self.xPos))
            music = MusicItem(self, "", self.theme, True)
            self.json2style(music, "default")
            music.setGeometry(self.xPos, self.yPos, 133, 62)
            music.hide()
            self.musicList.append(music)
            if j == 2:
                self.xPos = 362
                self.yPos += 77
                j=0
            else:
                self.xPos += 173
                j+=1






        self.setupUI()


    def setupUI(self):
        # erori
        self.buttonError.setGeometry(59, 312, 45, 45)

        self.errorMessage.setObjectName("warning")
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(55)
        self.errorMessage.setFont(font)
        self.errorMessage.setText("Please select a song")
        self.json2style(self.errorMessage,"default")
        self.errorMessage.setGeometry(129, 312, 295, 35)

        self.buttonError.hide()
        self.errorMessage.hide()
        ###########################################

        self.playMusicFrame.setObjectName("playFrame")
        self.json2style(self.playMusicFrame, "default")
        self.playMusicFrame.setGeometry(QRect(58, 70, 240, 200))

        self.buttonAdd2Play.setObjectName("simpleIco")
        self.json2style(self.buttonAdd2Play, "default")
        self.buttonAdd2Play.setGeometry(QRect(980, 333, 46, 46))

        # actiuni butoane
        self.playMusicFrame.getPlayStopButton().click_signal.connect(lambda: self.checkPath())
        self.playMusicFrame.getButtonNext().click_signal.connect(lambda: self.musicNext())


    # urmeaza a fi implementat daca muzica a fost sau nu stearsa
    def checkPath(self):
        if self.playMusicFrame.getName() == "":
            self.buttonError.show()
            self.errorMessage.show()
        else:
            self.buttonError.hide()
            self.errorMessage.hide()

    def musicNext(self):
        self.playMusicFrame.setPath("")
        self.playMusicFrame.setName("")

        for music in self.musicList:
            if music.getName() != "":
                musicName = music.getName()
                self.playMusicFrame.setPath(music.getPath())
                self.playMusicFrame.setName(musicName)

                music.setName("")
                music.hide()
                break
            print(music.getPath())



    def createSong(self, musicItem):
        musicName = musicItem.getName()
        if self.playMusicFrame.getName() == "":
            self.playMusicFrame.setPath(musicItem.getPath())
            self.playMusicFrame.setName(musicName)
            print("Music was created: "+musicItem.getPath())

        else:
            for music in self.musicList:
                if music.getName() == "":
                    music.setName(musicName)
                    music.show()
                    break

    def clickAdd(self):
        return self.buttonAdd2Play

    def json2style(self, element, action):
        styleValue = ""

        styleJson = self.theme[element.objectName()][action]


        for style in styleJson:
            styleValue += style["name"] + ":" + style["value"] + ";"


        element.setStyleSheet(styleValue)