import sys
import Children, ZayavkaA
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
)

class MainAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кибертрон/Администратор")
        self.setFixedSize(500, 230)
        self.initUI()

    def initUI(self):

        buttonChild = QPushButton("Дети", self)
        buttonChild.setFixedSize(430, 30)
        buttonChild.move(30, 40)
      
  

        buttonZayavka = QPushButton("Заявки", self)
        buttonZayavka.setFixedSize(430, 30)
        buttonZayavka.move(30, 100)
      

        buttonExit = QPushButton("Выход", self)
        buttonExit.setFixedSize(430, 30)
        buttonExit.move(30, 160)

        buttonChild.clicked.connect(self.Children)
        #buttonGroup.clicked.connect(self.Group)
        buttonZayavka.clicked.connect(self.Zayavka)
        buttonExit.clicked.connect(self.close)

    def Children(self):
        self.w = Children.Child()
        self.w.show()


    def Zayavka(self):
        self.w = ZayavkaA.Zayavka()
        self.w.show()

  
