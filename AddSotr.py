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
    QComboBox,
    QRadioButton,
    QDateEdit,
    QButtonGroup,
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

class AddSotr(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 553)
        self.setWindowTitle("Добавить")
        self.initUI()

    def initUI(self):
        select_centers = "SELECT * FROM center"
        centers = execute_read_query(connection, select_centers)
        lCenters = list()
        for c in centers:
            lCenters.append(str(c).split(',')[0][1:] + " " + str(c).split(',')[1][2:len(str(c).split(',')[1]) - 1])

        select_dolgs = "SELECT * FROM dolg"
        dolgs = execute_read_query(connection, select_dolgs)
        lDolgs = list()
        for d in dolgs:
            lDolgs.append(str(d).split(',')[0][1:] + " " + str(d).split(',')[1][2:len(str(d).split(',')[1]) - 1])

        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)

        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_sotr FROM sotr"
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
      
#fio
        labelFio = QLabel("<font color='#FF3300'>*</font> ФИО Сотрудника", self)
        labelFio.move(15, 55)

        self.lineAddFio = QLineEdit(self)
        self.lineAddFio.setObjectName("ФИО Сотрудника")
        self.lineAddFio.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddFio.move(15, 70)
      
#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата рождения", self)
        labelBirthday.move(15, 100)

        self.lineAddBirthday = QDateEdit(self)
        self.lineAddBirthday.setObjectName("Дата рождения")
        self.lineAddBirthday.move(15, 115)


#sex
        labelSex = QLabel("<font color='#FF3300'>*</font> Пол", self)
        labelSex.move(15, 145)

        self.group = QButtonGroup()
        self.lineAddSexF = QRadioButton("Ж", self)
        self.lineAddSexM = QRadioButton("М", self)
        self.group.addButton(self.lineAddSexF)
        self.group.addButton(self.lineAddSexM)
        self.lineAddSexF.move(15, 160)
        self.lineAddSexM.move(55, 160)
        self.group.buttonPressed.connect(self.Variant)
        

#phone
        labelPhone = QLabel("<font color='#FF3300'>*</font> Телефон", self)
        labelPhone.move(15, 190)

        self.lineAddPhone = QLineEdit(self)
        self.lineAddPhone.setObjectName("Телефон")
        self.lineAddPhone.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineAddPhone.move(15, 205)
        
#number_audit
        labelNumberAudit = QLabel("<font color='#FF3300'>*</font> Номер Аудитории", self)
        labelNumberAudit.move(15, 235)

        self.lineAddNumberAudit = QLineEdit(self)
        self.lineAddNumberAudit.setObjectName("Номер Аудитории")
        self.lineAddNumberAudit.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-]+")))
        self.lineAddNumberAudit.move(15, 250)
        
#date start
        labelDateStart = QLabel("<font color='#FF3300'>*</font> Дата начала работы", self)
        labelDateStart.move(15, 280)

        self.lineAddDateStart = QDateEdit(self)
        self.lineAddDateStart.setObjectName("Дата начала работы")
        self.lineAddDateStart.move(15, 295)
#stag
        labelStag = QLabel("<font color='#FF3300'>*</font> Стаж", self)
        labelStag.move(15, 325)

        self.lineAddStag = QLineEdit(self)
        self.lineAddStag.setObjectName("Стаж")
        self.lineAddStag.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineAddStag.move(15, 340)
        
#obrazovanie
        labelObrazovanie = QLabel("<font color='#FF3300'>*</font> Образование", self)
        labelObrazovanie.move(15, 370)

        self.lineAddObrazovanie = QLineEdit(self)
        self.lineAddObrazovanie.setObjectName("Образование")
        self.lineAddObrazovanie.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я-]+")))
        self.lineAddObrazovanie.move(15, 385)

#id_cent
        labelCenter = QLabel("<font color='#FF3300'>*</font> Центр", self)
        labelCenter.move(15, 415)
        
        self.lineAddCenter = QComboBox(self)
        self.lineAddCenter.setObjectName("Центр")
        self.lineAddCenter.addItems(lCenters)
        self.lineAddCenter.move(15, 430)
        

#id_dolg
        labelDolg = QLabel("Должность", self)
        labelDolg.move(15, 460)
        
        self.lineAddDolg = QComboBox(self)
        self.lineAddDolg.setObjectName("Должность")
        self.lineAddDolg.addItems(lDolgs)
        self.lineAddDolg.move(15, 475)
       

        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(154, 520)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 520)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked.connect(self.close)

    def Variant(self, button):
        self.lineAddSex = button.text()
    
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
            yearDS = int(self.lineAddDateStart.date().toString("yyyy.MM.dd").split('.')[0])
            monthDS = int(self.lineAddDateStart.date().toString("yyyy.MM.dd").split('.')[1])
            dayDS = int(self.lineAddDateStart.date().toString("yyyy.MM.dd").split('.')[2])
            
            
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            fio = " ".join(self.lineAddFio.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            sex = self.lineAddSex
            phone = " ".join(self.lineAddPhone.text().split()).title()
            number_audit = " ".join(self.lineAddNumberAudit.text().split()).title()
            date_start = date(yearDS, monthDS, dayDS)
            stag = int(" ".join(self.lineAddStag.text().split()).title())
            obrazovanie = " ".join(self.lineAddObrazovanie.text().split()).title()
            id_cent = int(self.lineAddCenter.currentText()[0])
            id_dolg = int(self.lineAddDolg.currentText()[0])
            zapis = (number, fio, birthday, sex, phone, number_audit, date_start, stag, obrazovanie, id_cent, id_dolg)
            newRow = "INSERT INTO sotr (id_sotr, fio, birthday, sex, phone, number_audit, data_start, stag, obrazovanie, id_cent, id_dolg) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()
            
            self.lineAddNumber.clear()
            self.lineAddFio.clear()
            self.lineAddPhone.clear()
            self.lineAddNumberAudit.clear()
            self.lineAddStag.clear()
            self.lineAddObrazovanie.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новый сотрудник добавлен")
            self.close()


















        
