import sys, MainDirector, MainAdministrator
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QPushButton,
    QMainWindow,
    QVBoxLayout,
    QLineEdit
)

class WindowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Академическая школа ИТ")
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        loglabel = QLabel("Логин", self)
        Login = QLineEdit(self)
        #buttonDir = QPushButton("Директор", self)
        #buttonDir.setFixedSize(430, 32)
        layout.addWidget(loglabel)
        layout.addWidget(Login)
        passlabel = QLabel("Пароль", self)
        password = QLineEdit(self)
        #buttonAdmin = QPushButton("Администратор", self)
        #buttonAdmin.setFixedSize(430, 32)
        layout.addWidget(passlabel)
        layout.addWidget(password)
        buttonOk = QPushButton("Войти")
        layout.addWidget(buttonOk)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        #buttonDir.clicked.connect(self.MainDir)
        #buttonAdmin.clicked.connect(self.MainAdmin)

    def MainDir(self):
        self.w = MainDirector.MainDir()
        self.w.show()
        self.close()

    def MainAdmin(self):
        self.w = MainAdministrator.MainAdmin()
        self.w.show()
        self.close()


app = QApplication(sys.argv)
window = WindowMain()
window.show()

app.exec()
