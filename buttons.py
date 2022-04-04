import multiprocessing
import sys
import threading
from multiprocessing import Process

from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent
from PyQt5.QtWidgets import QPushButton

from playsound import playsound
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

from gtts import gTTS
import os


class Buttons(QPushButton):
    click_signal = pyqtSignal()
    def __init__(self, container,image, ico_sie_w, ico_sie_h, image_pressed = None):
        super(Buttons, self).__init__(container)
        self.isActive = False
        self.icon_default = QIcon(f"icons\\{image}")
        self.ico_sie_w = ico_sie_w
        self.ico_sie_h = ico_sie_h
        self.image_pressed = None

        if image_pressed is not None:
            self.image_pressed = QIcon(f"icons\\{image_pressed}")

        self.module = None
        self.warning_sound = None
        self.song = None
        self.player = None
        self.isException = False
        self.textErr = ""
        # print(info)
        # variabile pentru erori vocale
        self.language = 'en'
        self.error_created = None
        ###############
        self.setupUI()

    def setupUI(self):
        self.setIcon(self.icon_default)
        self.setIconSize(QSize(self.ico_sie_w, self.ico_sie_h))
        self.setCursor(QCursor(Qt.PointingHandCursor))
    def isOn(self):
        return self.isActive

    def thread_function(self):
        try:
            mixer.init()
            if self.isActive:

                print(f"---------------- > thread_function with path: \t{self.song}")
                mixer.music.load(self.song)
                print("---------------- > load ok")
                mixer.music.play()
            else:
                mixer.music.stop()

                print("Thread : finishing")
        except:
            # songName = self.song.split("/")[-1]
            # print(songName)
            # self.textErr = f"File {songName} not found"
            # self.error_created = gTTS(text=self.textErr , lang=self.language, slow=False)
            # self.error_created.save(f"D:\\SEM_2\\IOC\\proiect\\buttonSound\\file-error")
            # self.isException = True
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\file-error.wav")
            print("error")
            self.set2close()


    def set2close(self):
        self.setIcon(self.icon_default)
        self.isActive = False

    def set2open(self):
        self.setIcon(self.image_pressed)
        self.isActive = True

    def setWarningSound(self, sound):
        self.warning_sound = sound
        self.isActive = (not self.isActive)

    def setSong(self, spath):
        self.song = spath

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if self.warning_sound is None:
            self.isActive = (not self.isActive)

        if self.isActive and (self.image_pressed is not None) and (self.warning_sound is None):

            self.setIcon(self.image_pressed)
            self.setIconSize(QSize(self.ico_sie_w, self.ico_sie_h))
            self.setCursor(QCursor(Qt.PointingHandCursor))

            try:
                mixer.init()
                mixer.music.load("D:\\SEM_2\\IOC\\proiect\\buttonSound\\enable.wav")
                mixer.music.play()
            except:
                pass
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\enable.wav")

            # x = threading.Thread(target=self.thread_function, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\enable.wav",))
            # x.start()

        elif self.image_pressed is not None and self.warning_sound is None:
            self.setIcon(self.icon_default)
            self.setIconSize(QSize(self.ico_sie_w, self.ico_sie_h))
            self.setCursor(QCursor(Qt.PointingHandCursor))
            try:
                mixer.init()
                mixer.music.load("D:\\SEM_2\\IOC\\proiect\\buttonSound\\disable.wav")
                mixer.music.play()
            except:
                pass
            # playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\disable.wav")

        elif self.warning_sound is None:
            try:
                playsound("D:\\SEM_2\\IOC\\proiect\\buttonSound\\click.wav")
            except:
                pass
        else:
            print(self.warning_sound)
            try:
                mixer.init()
                mixer.music.load(f"D:\\SEM_2\\IOC\\proiect\\buttonSound\\{self.warning_sound}.wav")
                mixer.music.play()
            except:
                threading.Thread(target=playsound, args=("D:\\SEM_2\\IOC\\proiect\\buttonSound\\error-sound.wav",)).start()

            # playsound(f"D:\\SEM_2\\IOC\\proiect\\buttonSound\\{self.warning_sound}")

        # print(self.song)

        if (self.warning_sound is None) and self.song is not None:
            print("play "+self.song)
            self.thread_function()



        self.click_signal.emit()
    #QHoverEvent
