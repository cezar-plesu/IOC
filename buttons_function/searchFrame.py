from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class SearchFrame(QLabel):
    def __init__(self, parent):
        super(SearchFrame, self).__init__(parent)
        self.textSearch = QLabel(self)
        self.setupUI()

    def setupUI(self):
        self.textSearch.setGeometry(27, 15, 600, 20)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(55)
        self.textSearch.setFont(font)
        self.textSearch.setText("Say 'Hey Siri' to start vocal control")

      #  self.textSearch.setStyleSheet("background-color: #FFBB50;")


    def setText(self, text):
        self.textSearch.setText(text)

