import sys
import connect_db
from datetime import date 
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt, QRegularExpression #QRegExp
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QMessageBox,
    QDateEdit,
    QComboBox,
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

class AddChild(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 553)
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")

        select_rels = "SELECT * FROM relation"
        rels = execute_read_query(connection, select_rels)
        lRels = list()
        for r in rels:
            lRels.append(str(r).split(',')[0][1:] + " " + str(r).split(',')[1][2:len(str(r).split(',')[1]) - 1])

        select_groups = "SELECT * FROM groupn"
        groups = execute_read_query(connection, select_groups)
        lGroups = list()
        for g in groups:
            lGroups.append(str(g).split(',')[0][1:] + " " +str(g).split(',')[1][2:len(str(g).split(',')[1]) - 1])
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_child FROM children"
        centers = execute_read_query(connection, select_centers)
        lCenters = list()
        for c in centers:
            lCenters.append(str(c).split(",")[0][1:])
        count = 0
        for i in range(1, 1000):
                for j in lCenters:
                        if j == str(i):
                                count += 1
                if count == 0:
                        k = str(i)
                        break
                else:
                        count = 0

        self.lineAddNumber = QLineEdit(self)
        self.lineAddNumber.setObjectName("Номер")
        self.lineAddNumber.setText(k)
        self.lineAddNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineAddNumber.move(15, 25)
      
#fiochild
        labelFioChild = QLabel("<font color='#FF3300'>*</font> ФИО Ребенка", self)
        labelFioChild.move(15, 55)

        self.lineAddFioChild = QLineEdit(self)
        self.lineAddFioChild.setObjectName("ФИО Ребенка")
        self.lineAddFioChild.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddFioChild.move(15, 70)
        

#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата Рождения", self)
        labelBirthday.move(15, 100)

        self.lineAddBirthday = QDateEdit(self)
        self.lineAddBirthday.setObjectName("Дата рождения")
        self.lineAddBirthday.move(15, 115)

#adres
        labelAddress = QLabel("<font color='#FF3300'>*</font> Адрес", self)
        labelAddress.move(15, 145)

        self.lineAddAddress = QLineEdit(self)
        self.lineAddAddress.setObjectName("Адрес")
        self.lineAddAddress.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-/]+")))
        self.lineAddAddress.move(15, 160)

#id_rel
        labelRel = QLabel("<font color='#FF3300'>*</font> Родитель", self)
        labelRel.move(15, 190)
        
        self.lineAddRel = QComboBox(self)
        self.lineAddRel.setObjectName("Родители")
        self.lineAddRel.addItems(lRels)
        self.lineAddRel.move(15, 205)
       

#id_group
        labelGroup = QLabel("Группа", self)
        labelGroup.move(15, 235)
        
        self.lineAddGroup = QComboBox(self)
        self.lineAddGroup.setObjectName("ГРуппа")
        self.lineAddGroup.addItems(lGroups)
        self.lineAddGroup.move(15, 250)

        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(154, 520)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 520)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked.connect(self.close)

    def Acept(self):
        lineEdits = self.findChildren(QLineEdit)
        text = ''
        for lineEdit in lineEdits:
            if not lineEdit.text():
                text = f'{text}Заполните {lineEdit.objectName()}\n'
        if text:
            msg = QMessageBox.information(self, 'Внимание', text)
        else:
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            cursor = connection.cursor()
            yearB = int(self.lineAddBirthday.date().toString("yyyy.MM.dd").split('.')[0])
            monthB = int(self.lineAddBirthday.date().toString("yyyy.MM.dd").split('.')[1])
            dayB = int(self.lineAddBirthday.date().toString("yyyy.MM.dd").split('.')[2])
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            fio_child = " ".join(self.lineAddFioChild.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            address = " ".join(self.lineAddAddress.text().split()).title()
            id_rel = int(self.lineAddRel.currentText()[0])
            id_group = int(self.lineAddGroup.currentText()[0])
            zapis = (number, fio_child, birthday, address, id_rel, id_group)
            newRow = "Insert Into children (id_child, fio_child, birthday, address, id_rel, id_group) Values (%s, %s, %s, %s, %s, %s)"

            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()

            self.lineAddNumber.clear()
            self.lineAddFioChild.clear()
            self.lineAddAddress.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новый ребенок добавлен")
            self.close()




