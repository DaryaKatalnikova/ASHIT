import sys
import connect_db, AddZayavka, EditZayavka
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
)

connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

class Zayavka(QWidget):
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
        AddZayavkaButton = QPushButton("Добавить", self)
        RefreshButton = QPushButton("Обновить", self)
        #AddStatusButton = QPushButton("Добавить новый статус", self)
        self.setLayout(layout)
        layout.addWidget(AddZayavkaButton, 0, 3)
        layout.addWidget(RefreshButton, 0, 4)
        #layout.addWidget(AddStatusButton, 0, 0, 1, 2)
        layout.addWidget(QLabel("Номер заявки"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО родителя"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО ребенка"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Дата заполнения"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Статус заявки"), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0

        for z in zayavkas:
            self.setLayout(layout)
            n = QPushButton()
            n.setFixedSize(50, 25)
            namen = str(z[0]) 
            n.setText(namen)
            n.name = namen
            layout.addWidget(n, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            n.clicked.connect(self.EditZayavka)
            j += 1
            layout.addWidget(QLabel(z[1]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(z[2]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(z[3])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(z[4]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            i += 1
            j = 0

        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 4)

        AddZayavkaButton.clicked.connect(self.AddZayavka)
        RefreshButton.clicked.connect(self.Refresh)
        BackButton.clicked.connect(self.close)

    def AddZayavka(self):
        self.w = AddZayavka.AddZayavka()
        self.w.show()

    def Refresh(self):
        self.close()
        self.w = Zayavka()
        self.w.show()

    def EditZayavka(self):
        num = int(self.sender().name)
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        eZayavkaZ = """SELECT zayavka.id_zayavka, zayavka.fio_rel, zayavka.fio_chil, zayavka.date_zap, statusz.nameStat FROM zayavka left JOIN statusz on zayavka.id_stat = statusz.id_stat AND zayavka.id_zayavka = '%s'""" % (num)
        with connection.cursor() as cursor:
            cursor.execute(eZayavkaZ)
            for zt in cursor.fetchall():
                eZayavka = zt
        self.number = num
        self.fio_rel = zt[1]
        self.fio_child = zt[2]
        self.date_zap = zt[3]
        self.id_stat = zt[4]
        self.w = EditZayavka.EditZayavka(self.number, self.fio_rel, self.fio_child, self.date_zap, self.id_stat)       
        self.w.show()


