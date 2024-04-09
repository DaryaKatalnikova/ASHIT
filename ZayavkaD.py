import sys
import connect_db, AddStatus, EditStatus
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

class ZayavkaD(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Заявки")
        self.initUI()
        
    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_zayavkas = "SELECT zayavka.id_zayavka, zayavka.fio_rel, zayavka.fio_chil, zayavka.date_zap, statusz.nameStat FROM zayavka left JOIN statusz on zayavka.id_stat = statusz.id_stat"
        zayavkas = execute_read_query(connection, select_zayavkas)
        layout = QGridLayout(self)
        #AddZayavkaButton = QPushButton("Добавить", self)
        RefreshButton = QPushButton("Обновить", self)
        AddStatusButton = QPushButton("Добавить новый статус", self)
        self.setLayout(layout)
        #layout.addWidget(AddZayavkaButton, 0, 3)
        layout.addWidget(RefreshButton, 0, 4)
        layout.addWidget(AddStatusButton, 0, 0, 1, 2)
        layout.addWidget(QLabel("Номер заявки"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО родителя"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО ребенка"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Дата заполнения"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Статус заявки"), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0

        for z in zayavkas:
            self.setLayout(layout)
           
            s = QPushButton()
            s.setFixedSize(150, 25)
            names = z[4]
            s.setText(names)
            s.name = names
        
            layout.addWidget(QLabel(str(z[0])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(z[1]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(z[2]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(z[3])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(s, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            s.clicked.connect(self.EditStatus)
            i += 1
            j = 0

        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 4)

        #AddZayavkaButton.clicked.connect(self.AddZayavka)
        RefreshButton.clicked.connect(self.Refresh)
        AddStatusButton.clicked.connect(self.AddStatus)
        BackButton.clicked.connect(self.close)

   
    def Refresh(self):
        self.close()
        self.w = ZayavkaD()
        self.w.show()

    def AddStatus(self):
        self.w = AddStatus.AddStatus()
        self.w.show()

    def EditStatus(self):
        nameStatus = self.sender().name
        if nameStatus != None:
            zapis = [nameStatus]
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            eStatZ = "select * from statusz where nameStat = %s"
            with connection.cursor() as cursor:
                cursor.execute(eStatZ, zapis)
                for stat in cursor.fetchall():
                    eStat = stat
            self.number = eStat[0]
            self.nameStat = eStat[1]
            self.w = EditStatus.EditStatus(self.number, self.nameStat)
            self.w.show()
