import sys
import connect_db, AddChild, EditChild, Kvit, AddRel, EditRel, AddGroup, EditGroup
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QMenuBar,
    QGridLayout,
    QToolBar
    
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


class Child(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1000, 500)
        self.setWindowTitle("Дети")
        self.initUI()
        
        
    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_childs = """SELECT id_child, fio_child, children.birthday, children.address, relation.id_rel, relation.fio_rel, groupn.name_group FROM children
        join relation on relation.id_rel = children.id_rel
        join groupn on groupn.id_group = children.id_group"""
        childs = execute_read_query(connection, select_childs)

      

        layout = QGridLayout()
        AddChildButton = QPushButton("Добавить", self)
        RefreshButton = QPushButton("Обновить", self)
        AddRelButton = QPushButton("Добавить нового родителя", self)
        AddGroupButton = QPushButton("Добавить новую группу", self)
        self.setLayout(layout)
        layout.addWidget(AddChildButton, 0, 3)
        layout.addWidget(RefreshButton, 0, 4)
        layout.addWidget(AddRelButton, 0, 0)
        layout.addWidget(AddGroupButton, 0, 1)
        layout.addWidget(QLabel("ФИО ребенка"), 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("День рождения"), 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Адрес"), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("ФИО родителя"), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Группа"), 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        i = 2
        j = 0

        for c in childs:
            self.setLayout(layout)
            ch = QPushButton()
            ch.setFixedSize(200, 25)
            namech = str(c[0]) + " " + c[1]
            ch.setText(namech)
            ch.name = namech
            r = QPushButton()
            r.setFixedSize(200, 25)
            namer = c[5]
            r.setText(namer)
            if c[4] != None and c[5] != None:
                r.name = str(c[4]) + " " + c[5]
            else:
                r.name = None
            g = QPushButton()
            g.setFixedSize(100, 25)
            nameg = c[6]
            g.setText(nameg)
            g.name = nameg
            layout.addWidget(ch, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            ch.clicked.connect(self. EditChild)
            j += 1
            layout.addWidget(QLabel(str(c[2])), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(QLabel(c[3]), i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            j += 1
            layout.addWidget(r, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            r.clicked.connect(self.EditRel)
            j += 1
            layout.addWidget(g, i, j, alignment=Qt.AlignmentFlag.AlignCenter)
            g.clicked.connect(self.EditGroup)
            i += 1
            j = 0

        BackButton = QPushButton("Назад", self)
        self.setLayout(layout)
        layout.addWidget(BackButton, i, 4)    
        kvitButton = QPushButton("Оплата", self)
        self.setLayout(layout)
        layout.addWidget(kvitButton, i, 0)
            

        AddChildButton.clicked.connect(self.AddChild)
        RefreshButton.clicked.connect(self.Refresh)
        AddRelButton.clicked.connect(self.AddRel)
        AddGroupButton.clicked.connect(self.AddGroup)
        BackButton.clicked.connect(self.close)
        kvitButton.clicked.connect(self.Kvit)
        

    def AddChild(self):
        self.w = AddChild.AddChild()
        self.w.show()

    def AddRel(self):
        self.w = AddRel.AddRel()
        self.w.show()

    def AddGroup(self):
        self.w = AddGroup.AddGroup()
        self.w.show()

    def Refresh(self):
        self.close()
        self.w = Child()
        self.w.show()

    def EditChild(self):
        num = int(self.sender().name[0])
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        eChildZ = """SELECT * from children where children.id_child = '%s' """ % (num)
        with connection.cursor() as cursor:
            cursor.execute(eChildZ)
            for st in cursor.fetchall():
                eChild = st
        self.number = num
        self.fio_child = eChild[1]
        self.birthday = eChild[2]
        self.address = eChild[3]
        self.id_rel = eChild[4]
        self.id_group = eChild[5]
        self.w = EditChild.EditChild(self.number, self.fio_child, self.birthday, self.address, self.id_rel, self.id_group)       
        self.w.show()

    def EditRel(self):
        if self.sender().name != None:
            numRel = self.sender().name[0]
            if numRel != None:
                zapis = [numRel]
                connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
                eRelZ = "select * from relation where id_rel = %s"
                with connection.cursor() as cursor:
                    cursor.execute(eRelZ, zapis)
                    for rel in cursor.fetchall():
                        eRel = rel
                self.number = eRel[0]
                self.fio_rel = eRel[1]
                self.birthday = eRel[2]
                self.address = eRel[3]
                self.phoneL = eRel[4]
                self.e_mail = eRel[5]
                self.job = eRel[6]
                self.phoneJ = eRel[7]
                self.id_zayavka = eRel[8] 
                self.w = EditRel.EditRel(self.number, self.fio_rel, self.birthday, self.address, self.phoneL, self.e_mail, self.job, self.phoneJ, self.id_zayavka)
                self.w.show()
            
    def EditGroup(self):
        nameGroup = self.sender().name
        if nameGroup != None:
            zapis = [nameGroup]
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            eGroupZ = "select * from groupn where name_group = %s"
            with connection.cursor() as cursor:
                cursor.execute(eGroupZ, zapis)
                for group in cursor.fetchall():
                    eGroup = group
            self.number = eGroup[0]
            self.name_group = eGroup[1]
            self.id_sotr = eGroup[2]
            self.w = EditGroup.EditGroup(self.number, self.name_group, self.id_sotr)
            self.w.show()

    def Kvit(self):
        self.w = Kvit.Kvit()
        self.w.show()