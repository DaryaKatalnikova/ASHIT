import sys
import connect_db, AddKvit
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout

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


class Kvit(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Оплата")
        self.initUI()
        
    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_kvits = """select children.id_child, children.fio_child, kvit.summa, kvit.date_opl from children, kvit
        where kvit.id_child = children.id_child order by children.id_child"""
        kvits = execute_read_query(connection, select_kvits)
        layout = QGridLayout()
        RefreshButton = QPushButton("Обновить", self)
        AddKvitButton = QPushButton("Добавить оплату", self)
        self.setLayout(layout)
        layout.addWidget(AddKvitButton, 0, 2)
        layout.addWidget(RefreshButton, 0, 3)
            
        layout.addWidget(QLabel("№"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО ребенка"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Сумма"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Дата оплаты"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0
        for c in kvits:
            self.setLayout(layout)
            layout.addWidget(QLabel(str(c[0])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[1]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(c[2])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(c[3])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            i += 1
            j = 0

        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 3)    
        
        AddKvitButton.clicked.connect(self.AddKvit)
        RefreshButton.clicked.connect(self.Refresh)
        BackButton.clicked.connect(self.close)

    def AddKvit(self):
        self.w = AddKvit.AddKvit()
        self.w.show()

    def Refresh(self):
        self.close()
        self.w = Kvit()
        self.w.show()

  