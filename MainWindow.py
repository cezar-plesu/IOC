import json
import sys
import importlib
import threading
from os import environ

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QFrame, QWidget, QVBoxLayout, \
    QSpacerItem, QSizePolicy, QScrollArea, QLayout, QMainWindow, QHBoxLayout
from PyQt5.QtCore import Qt, QRect, QSize
from playsound import playsound

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

from buttons import Buttons
from buttons_function.cameraModule import CameraModule
from buttons_function.volumeManager import VolumeManager
from musicItem import MusicItem
from playListFrame import PlayListFrame

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setObjectName("mainWindow")
        self.centralWidget = QWidget(self)

        # referinte la functii
        playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\intro.wav",False)

        self.volumeManager = VolumeManager()
        print(self.volumeManager.volumeOn())

        # self.cameraModule = CameraModule(0)
        # print(self.cameraModule.getStatus())
        ##############


        self.mode = None
        with open('style/curentTheme.txt') as f:
            lines = f.readlines()
            self.mode = lines[0]

        f = open(f'style/{self.mode}.json')
        self.theme = json.load(f)

        self.buttonBluetooth = Buttons(self.centralWidget,"Bluetooth_on.svg",29, 24 )

        if self.volumeManager.volumeOn():
            self.buttonSound = Buttons(self.centralWidget, "sound_on_2.svg", 41, 41, "sound_off")
        else:
            self.buttonSound = Buttons(self.centralWidget, "sound_off.svg", 41, 41, "sound_on_2")


        self.buttonCamera = Buttons(self.centralWidget, "camera_off.svg", 41, 41,"camera_on")


        self.buttonMicrophone = Buttons(self.centralWidget, "microphone_off.svg", 41, 41,"microphone_on.svg")
        self.buttonTrash = Buttons(self.centralWidget, "trash.svg", 41, 41)
        self.buttonAddMusic = Buttons(self.centralWidget, "add_music.svg", 41, 41)


        if self.mode == "dayStyle":
            self.themeChangeButton = Buttons(self.centralWidget, "moon.svg", 41, 41, "sun.svg")
        else:
            self.themeChangeButton = Buttons(self.centralWidget, "sun.svg", 41, 41, "moon.svg")
        self.playListFrame = PlayListFrame(self.centralWidget, self.theme)

        self.musicActiveList = []

        #scroll area pt melodii incarcate
        self.attachmentScrollArea = QScrollArea(self)
        self.scrollAreaWidgetContents = QWidget()
        self.verticalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.once = True


        self.setupUI()

    def setupUI(self):
        # self.resize(1256, 681)

        # print(self.theme["songFramePlaylist"]["default"])

        # print(self.json2style(self.theme["songFramePlaylist"]["default"]))

        self.setFixedSize(QSize(1256, 681))
        # self.setStyleSheet(self.json2style(self.theme[self.objectName()]["default"]))
        self.json2style(self,"default")
        self.setWindowTitle("No Hans Player")
        self.setCentralWidget(self.centralWidget)

        self.buttonBluetooth.setObjectName("bluetooth")
        self.json2style(self.buttonBluetooth, "default")
        self.buttonBluetooth.setGeometry(QRect(22, 25, 41, 41))

        self.buttonBluetooth.hide()

        self.buttonBluetooth.click_signal.connect(self.close)

        self.buttonSound.setObjectName("simpleIco")
        self.json2style(self.buttonSound, "default")
        self.buttonSound.setGeometry(QRect(1177, 29, 41, 41))

        self.buttonCamera.setObjectName("simpleIco")
        self.json2style(self.buttonCamera, "default")
        self.buttonCamera.setGeometry(QRect(1077, 29, 41, 41))

        self.buttonMicrophone.setObjectName("simpleIco")
        self.json2style(self.buttonMicrophone, "default")
        self.buttonMicrophone.setGeometry(QRect(977, 29, 41, 41))

        self.buttonTrash.setObjectName("simpleIco")
        self.json2style(self.buttonTrash, "default")
        self.buttonTrash.setGeometry(QRect(1177, 627, 41, 41))

        self.buttonAddMusic.setObjectName("simpleIco")
        self.json2style(self.buttonAddMusic, "default")
        self.buttonAddMusic.setGeometry(QRect(1077, 627, 41, 41))

        self.themeChangeButton.setObjectName("simpleIco")
        self.json2style(self.themeChangeButton, "default")
        self.themeChangeButton.setGeometry(QRect(29, 629, 41, 41))

        self.playListFrame.setObjectName("musicFrame")
        self.json2style(self.playListFrame, "default")
        self.playListFrame.setGeometry(QRect(103, 182, 1040, 393))

        # actiuni butoane
        self.buttonAddMusic.click_signal.connect(lambda: self.addMusicPath())
        self.playListFrame.clickAdd().click_signal.connect(lambda: self.window2playList())
        self.themeChangeButton.click_signal.connect(lambda: self.swapTheme())
        self.buttonSound.click_signal.connect(lambda: self.setVolume())
        self.buttonCamera.click_signal.connect(lambda: self.camera())
        self.buttonTrash.click_signal.connect(lambda: self.removeItem())
        # scoll Areea
        self.attachmentScrollArea.setEnabled(True)
        self.attachmentScrollArea.setGeometry(QRect(106, 97, 1037, 68))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.attachmentScrollArea.setSizePolicy(sizePolicy)
        self.attachmentScrollArea.setMinimumSize(QSize(1037, 68))
        self.attachmentScrollArea.setMaximumSize(QSize(1037, 68))
        self.attachmentScrollArea.setFrameShape(QFrame.NoFrame)
        self.attachmentScrollArea.setLineWidth(0)
        self.attachmentScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.attachmentScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.attachmentScrollArea.setWidgetResizable(False)

        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1037, 68))

        self.verticalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)

        self.attachmentScrollArea.setWidget(self.scrollAreaWidgetContents)
        #####################

        # path = 'D:/SEM_2/IOC/proiect/music/'
        # files = os.listdir(path)
        # for filename in glob.glob(os.path.join(path, '*.wav')):
        #     print(filename)
        #     musicName = filename.split("\\")[-1]
        #     print(musicName)
        #     musicName = musicName.split(".")[0]
        #     if musicName != "":
        #         self.verticalLayout.removeItem(self.spacerItem)
        #
        #         print("got here")
        #         music = MusicItem(self.centralWidget, musicName, self.theme, False)
        #
        #         self.json2style(music, "default")
        #         music.setMinimumSize(133, 62)
        #         music.setMaximumSize(133, 62)
        #         music.click_signal.connect(lambda isPressed: self.selectedMusic(music, isPressed))
        #         self.verticalLayout.addWidget(music)
        #         self.verticalLayout.addSpacerItem(self.spacerItem)
    def swapTheme(self):
        f = open("style/curentTheme.txt", "w")

        print(self.mode)
        if self.mode == "style":
            f.write("dayStyle")
            print("ok")
        else:
            f.write("style")

        f.close()

        importlib.reload(self)


    def camera(self):
        self.cameraModule = CameraModule(0)
        print(self.buttonCamera.isOn())
        if self.buttonCamera.isOn():
            if not self.cameraModule.getStatus():
                self.buttonCamera.set2close()

                playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\camera_error.wav")

            else:
                self.buttonCamera.setWarningSound(None)
                self.buttonCamera.set2open()
        else:
            self.buttonCamera.set2close()

    def setVolume(self):
        self.volumeManager.setVolume()

    def close(self):
        print("close")

    # dupa ce apas dutonul nu isi face refresh pagina
    def addMusicPath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'D:\SEM_2\IOC\proiect\music\\', "Music files (*.wav *.mp3 *.flac)")


        fileName = fname[0]

        musicName = fname[0].split("/")[-1]
        musicName = musicName.split(".")[0]
        if musicName != "":
            self.verticalLayout.removeItem(self.spacerItem)


            music = MusicItem(self.centralWidget, fileName, self.theme, False)

            self.json2style(music, "default")
            music.setMinimumSize(133, 62)
            music.setMaximumSize(133, 62)
            music.click_signal.connect(lambda isPressed: self.selectedMusic(music, isPressed))
            self.verticalLayout.addWidget(music)
            self.verticalLayout.addSpacerItem(self.spacerItem)


            print("ok")
            # threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav",)).start()

            playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav")

    def removeItem(self):
        try:
            selected = None
            for music in self.musicActiveList:
                selected = music
                music.setParent(None)
                self.verticalLayout.removeWidget(music)
                break
            self.musicActiveList.remove(selected)
            threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav",)).start()
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav")
        except:
            threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\error-sound.wav",)).start()
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\error-sound.wav")

    def removeMusicPath(self, music):
        music.setParent(None)
        self.verticalLayout.removeWidget(music)

    def selectedMusic(self, music_obj, isPressed):
        #self.musicActiveList
        if not isPressed:
            # print("default")
            self.musicActiveList.remove(music_obj)
        else:
            # print("pressed")
            self.musicActiveList.append(music_obj)


    def window2playList(self):
        if self.musicActiveList:
            # threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav",)).start()
            playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\success_load.wav")
        else:
            # threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\error-sound.wav",)).start()
            playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\error-sound.wav")

        for music in self.musicActiveList:
            print(music)
            self.playListFrame.createSong(music)
            self.removeMusicPath(music)
            self.musicActiveList.remove(music)

    def json2style(self, element, action):
        styleValue = ""
        styleJson = self.theme[element.objectName()][action]

        for style in styleJson:
            styleValue += style["name"] + ":"+style["value"]+";"

        element.setStyleSheet(styleValue)