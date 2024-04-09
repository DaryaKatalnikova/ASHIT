import sys
import connect_db, AddCenter, EditCenter
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableView,
    QListWidget,
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

class Center(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Центры")
        self.initUI()
        
        
    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT * FROM center"
        centers = execute_read_query(connection, select_centers)
        layout = QGridLayout()
        AddCenterButton = QPushButton("Добавить", self)
        RefreshButton = QPushButton("Обновить", self)
        self.setLayout(layout)
        layout.addWidget(AddCenterButton, 0, 6)
        layout.addWidget(RefreshButton,0, 7)

        #layout.addWidget(QLabel("Номер"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Название центра"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Юридический адрес"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("фактический адрес"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Телефон"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("E-mail"), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Сайт"), 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Счет"), 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Директор"), 1, 7, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0
        print(centers)
        for c in centers:
            self.setLayout(layout)
            l = QPushButton()
            l.setFixedSize(150, 25)
            namel = str(c[0]) + "  " + c[1]
            l.setText(namel)
            l.name = namel
            layout.addWidget(l, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            l.clicked.connect(self.EditCenter)
            j += 1
            layout.addWidget(QLabel(c[2]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[3]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[4]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[5]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[6]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(c[7])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[8]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            i += 1
            j = 0
        
        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 7)
        
        AddCenterButton.clicked.connect(self.AddCenter)
        RefreshButton.clicked.connect(self.Refresh)
        BackButton.clicked.connect(self.close)
        

    def AddCenter(self):
        self.w = AddCenter.AddCenter()
        self.w.show()

    def Refresh(self):
        self.close()
        self.w = Center()
        self.w.show()

    def EditCenter(self):
        num = int(self.sender().name[0])
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        eCentZ = "select * from center where id_cent = '%s'" % (num)
        with connection.cursor() as cursor:
            cursor.execute(eCentZ)
            for cent in cursor.fetchall():
                eCent = cent

        self.number = num
        self.name = eCent[1]
        self.urad = eCent[2]
        self.factad = eCent[3]
        self.phone = eCent[4]
        self.email = eCent[5]
        self.site = eCent[6]
        self.schet = eCent[7]
        self.gendir = eCent[8]
        self.w = EditCenter.EditCenter(self.number, self.name, self.urad, self.factad, self.phone, self.email, self.site, self.schet, self.gendir)       
        self.w.show()


