import sys
import Center, Sotr, ZayavkaD, Doki
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QVBoxLayout,
)

class MainDir(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кибертрон/Директор")

        self.setFixedSize(500, 270)
        self.initUI()

    def initUI(self):
        
        buttonCenter = QPushButton("Центр", self)
        buttonCenter.setFixedSize(430, 30)
        buttonCenter.move(30, 30)
       

        buttonSotr = QPushButton("Сотрудники", self)
        buttonSotr.setFixedSize(430, 30)
        buttonSotr.move(30, 75)
       

        buttonZayavka = QPushButton("Заявки", self)
        buttonZayavka.setFixedSize(430, 30)
        buttonZayavka.move(30, 120)

        buttonDoki = QPushButton("Документы", self)
        buttonDoki.setFixedSize(430, 30)
        buttonDoki.move(30, 165)

        buttonExit = QPushButton("Выход", self)
        buttonExit.setFixedSize(430, 30)
        buttonExit.move(30, 210)


    

        buttonCenter.clicked.connect(self.Center)
        #buttonDolg.clicked.connect(self.Dolg)
        buttonSotr.clicked.connect(self.Sotr)
        #buttonStatus.clicked.connect(self.Status)
        buttonDoki.clicked.connect(self.Doki)
        buttonZayavka.clicked.connect(self.Zayavka)
        buttonExit.clicked.connect(self.close)
    

    def Center(self):
        self.w = Center.Center()
        self.w.show()

    def Sotr(self):
        self.w = Sotr.Sotr()
        self.w.show()

    def Zayavka(self):
        self.w = ZayavkaD.ZayavkaD()
        self.w.show()

    def Doki(self):
        self.w = Doki.Doki()
        self.w.show()
