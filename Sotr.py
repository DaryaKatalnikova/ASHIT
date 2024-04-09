import sys
import connect_db, AddSotr, EditSotr, AddDolg, EditDolg
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

class Sotr(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Сотрудники")
        self.initUI()
        
        
    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_sotrs = "select sotr.id_sotr, sotr.fio, sotr.birthday, sotr.sex, sotr.phone, sotr.number_audit, sotr.data_start, sotr.stag, sotr.obrazovanie, center.nameCenter, dolg.nameDolg from sotr left join center on sotr.id_cent = center.id_cent left join dolg on sotr.id_dolg = dolg.id_dolg order by sotr.id_sotr"
        sotrs = execute_read_query(connection, select_sotrs)
        print(sotrs)
        layout = QGridLayout()
        AddSotrButton = QPushButton("Добавить", self)
        RefreshButton = QPushButton("Обновить", self)
        AddDolgButton = QPushButton("Добавить новую должность", self)
        self.setLayout(layout)
        layout.addWidget(AddSotrButton, 0, 8)
        layout.addWidget(RefreshButton, 0, 9)
        layout.addWidget(AddDolgButton, 0, 0, 1, 2)
        #layout.addWidget(QLabel("Номер"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Дата рождения"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Пол"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Телефон"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Номер аудитории"), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Дата начала работы"), 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Стаж"), 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Образование"), 1, 7, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Центр"), 1, 8, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Должность"), 1, 9, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0     
        for s in sotrs:
            self.setLayout(layout)
            l = QPushButton()
            l.setFixedSize(220, 25)
            namel = str(s[0]) + "  " + s[1]
            l.setText(namel)
            l.name = namel
            q = QPushButton()
            q.setFixedSize(100, 25)
            nameq = s[10]
            q.setText(nameq)
            q.name = nameq
            layout.addWidget(l, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            l.clicked.connect(self.EditSotr)
            j += 1
            layout.addWidget(QLabel(str(s[2])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(s[3]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(s[4]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(s[5])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(s[6])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(str(s[7])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(s[8]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(s[9]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(q, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            q.clicked.connect(self.EditDolg)
            i += 1
            j = 0
            

        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 9)
        
        
        AddSotrButton.clicked.connect(self.AddSotr)
        RefreshButton.clicked.connect(self.Refresh)
        AddDolgButton.clicked.connect(self.AddDolg)
        BackButton.clicked.connect(self.close)

    def AddSotr(self):
        self.w = AddSotr.AddSotr()
        self.w.show()

    def Refresh(self):
        self.close()
        self.w = Sotr()
        self.w.show()

    def AddDolg(self):
        self.w = AddDolg.AddDolg()
        self.w.show()

    def EditSotr(self):
        num = int(self.sender().name[0])
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        eSotrZ = """select sotr.id_sotr, sotr.fio, sotr.birthday, sotr.sex, sotr.phone, 
        sotr.number_audit, sotr.data_start, sotr.stag, sotr.obrazovanie, 
        center.nameCenter, dolg.nameDolg from sotr 
        inner join center on sotr.id_cent = center.id_cent and sotr.id_sotr = '%s' 
        left join dolg on sotr.id_dolg = dolg.id_dolg 
        order by sotr.id_sotr""" % (num)
        with connection.cursor() as cursor:
            cursor.execute(eSotrZ)
            for st in cursor.fetchall():
                eSotr = st
        self.number = num
        self.fio = eSotr[1]
        self.birthday = eSotr[2]
        self.sex = eSotr[3]
        self.phone = eSotr[4]
        self.number_audit = eSotr[5]
        self.data_start = eSotr[6]
        self.stag = eSotr[7]
        self.obrazovanie = eSotr[8]
        self.id_cent = eSotr[9]
        self.id_dolg = eSotr[10]
        self.w = EditSotr.EditSotr(self.number, self.fio, self.birthday, self.sex, self.phone, self.number_audit, self.data_start, self.stag, self.obrazovanie, self.id_cent, self.id_dolg)       
        self.w.show()

    def EditDolg(self):
        nameDolgs = self.sender().name
        if nameDolgs != None:
            zapis = [nameDolgs]
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            eDolgZ = "select * from dolg where nameDolg = %s" 
            with connection.cursor() as cursor:
                cursor.execute(eDolgZ, zapis)
                for dolg in cursor.fetchall():
                    eDolg = dolg
            self.number = eDolg[0]
            self.nameD = eDolg[1]
            self.oklad = eDolg[2]
            self.w = EditDolg.EditDolg(self.number, self.nameD, self.oklad)
            self.w.show()