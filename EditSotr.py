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



class EditSotr(QWidget):
    def __init__(self, number, fio, birthday, sex, phone, number_audit, data_start, stag, obrazovanie, id_cent, id_dolg):
        super().__init__()
        self.number = number
        self.fio = fio
        self.birthday = birthday
        self.sex = sex
        self.phone = phone
        self.number_audit = number_audit
        self.data_start = data_start
        self.stag = stag
        self.obrazovanie = obrazovanie
        self.id_cent = id_cent
        self.id_dolg = id_dolg

        self.setFixedSize(320, 553)
        self.setWindowTitle("Редактировать")
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

        self.lineEditNumber = QLineEdit(self)
        self.lineEditNumber.setFixedSize(300, 25)
        self.lineEditNumber.setText(str(self.number))
        self.lineEditNumber.setObjectName("Номер")
        self.lineEditNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditNumber.move(15, 25)
  
#fio
        labelFio = QLabel("<font color='#FF3300'>*</font> ФИО Сотрудника", self)
        labelFio.move(15, 55)

        self.lineEditFio = QLineEdit(self)
        self.lineEditFio.setFixedSize(300, 25)
        self.lineEditFio.setText(self.fio)
        self.lineEditFio.setObjectName("ФИО Сотрудника")
        self.lineEditFio.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditFio.move(15, 70)

#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата рождения", self)
        labelBirthday.move(15, 100)

        self.lineEditBirthday = QDateEdit(self)
        self.lineEditBirthday.setFixedSize(300, 25)
        self.lineEditBirthday.setDate(self.birthday)
        self.lineEditBirthday.setObjectName("Дата рождения")
        self.lineEditBirthday.move(15, 115)

#sex
        labelSex = QLabel("<font color='#FF3300'>*</font> Пол", self)
        labelSex.move(15, 145)

        self.group = QButtonGroup()
        self.lineEditSexF = QRadioButton("Ж", self)
        self.lineEditSexM = QRadioButton("М", self)
        self.group.addButton(self.lineEditSexF)
        self.group.addButton(self.lineEditSexM)
        if self.lineEditSexF.text() == self.sex:
            self.lineEditSexF.click()
        else:
            self.lineEditSexM.click()
        self.lineEditSexF.move(15, 160)
        self.lineEditSexM.move(55, 160)

#phone
        labelPhone = QLabel("<font color='#FF3300'>*</font> Телефон", self)
        labelPhone.move(15, 190)

        self.lineEditPhone = QLineEdit(self)
        self.lineEditPhone.setFixedSize(300, 25)
        self.lineEditPhone.setText(self.phone)
        self.lineEditPhone.setObjectName("Телефон")
        self.lineEditPhone.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineEditPhone.move(15, 205)
#number_audit
        labelNumberAudit = QLabel("<font color='#FF3300'>*</font> Номер Аудитории", self)
        labelNumberAudit.move(15, 235)

        self.lineEditNumberAudit = QLineEdit(self)
        self.lineEditNumberAudit.setFixedSize(300, 25)
        self.lineEditNumberAudit.setText(str(self.number_audit))
        self.lineEditNumberAudit.setObjectName("Номер Аудитории")
        self.lineEditNumberAudit.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-]+")))
        self.lineEditNumberAudit.move(15, 250)
#date statrt
        labelDateStart = QLabel("<font color='#FF3300'>*</font> Дата начала работы", self)
        labelDateStart.move(15, 280)

        self.lineEditDateStart = QDateEdit(self)
        self.lineEditDateStart.setFixedSize(300, 25)
        self.lineEditDateStart.setDate(self.data_start)
        self.lineEditDateStart.setObjectName("Дата начала работы")
        self.lineEditDateStart.move(15, 295)
#stag
        labelStag = QLabel("<font color='#FF3300'>*</font> Стаж", self)
        labelStag.move(15, 325)

        self.lineEditStag = QLineEdit(self)
        self.lineEditStag.setFixedSize(300, 25)
        self.lineEditStag.setText(str(self.stag))
        self.lineEditStag.setObjectName("Стаж")
        self.lineEditStag.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditStag.move(15, 340)
#obrazovanie
        labelObrazovanie = QLabel("<font color='#FF3300'>*</font> Образование", self)
        labelObrazovanie.move(15, 370)

        self.lineEditObrazovanie = QLineEdit(self)
        self.lineEditObrazovanie.setFixedSize(300, 25)
        self.lineEditObrazovanie.setText(self.obrazovanie)
        self.lineEditObrazovanie.setObjectName("Образование")
        self.lineEditObrazovanie.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я-]+")))
        self.lineEditObrazovanie.move(15, 385)

#id_cent
        labelCenter = QLabel("<font color='#FF3300'>*</font> Центр", self)
        labelCenter.move(15, 415)
        
        self.lineEditCenter = QComboBox(self)
        self.lineEditCenter.setObjectName("Центр")
        self.lineEditCenter.addItems(lCenters)
        for cent in lCenters:
            if self.id_cent in cent:
                self.lineEditCenter.setCurrentText(cent)
        self.lineEditCenter.setFixedSize(300, 25)
        self.lineEditCenter.move(15, 430)
        

#id_dolg
        labelDolg = QLabel("<font color='#FF3300'>*</font> Должность", self)
        labelDolg.move(15, 460)
        
        self.lineEditDolg = QComboBox(self)
        self.lineEditDolg.setObjectName("Должность")
        self.lineEditDolg.addItems(lDolgs)
        self.lineEditDolg.setFixedSize(300, 25) 
        if self.id_dolg != None:
            for dol in lDolgs:
                if self.id_dolg in dol:
                    self.lineEditDolg.setCurrentText(dol)
        self.lineEditDolg.move(15, 475)

        
        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(72, 520)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 520)

        buttonDelete = QPushButton("Удалить", self)
        buttonDelete.move(154, 520)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked.connect(self.close)
        buttonDelete.clicked.connect(self.Deleting)

    def Deleting(self):
        number = int(self.lineEditNumber.text())
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        delete_status = "DELETE FROM sotr WHERE id_sotr = '%d'" % (number)
        with connection.cursor() as cursor:
            cursor.execute(delete_status)
            connection.commit()
            self.close()

    def Variant(self, button):
        self.lineEditSex = button.text()

    def Acept(self):
        lineEdits =  self.findChildren(QLineEdit)
        text = ''
        for lineEdit in lineEdits:
            if not lineEdit.text():
                text = f'{text}Заполните {lineEdit.objectName()}\n'
        if text:
            msg = QMessageBox.information(self, 'Внимание', text)
        else:
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            cursor = connection.cursor()
            yearB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[0])
            monthB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[1])
            dayB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[2])
            yearDS = int(self.lineEditDateStart.date().toString("yyyy.MM.dd").split('.')[0])
            monthDS = int(self.lineEditDateStart.date().toString("yyyy.MM.dd").split('.')[1])
            dayDS = int(self.lineEditDateStart.date().toString("yyyy.MM.dd").split('.')[2])
            self.lineEditSex = self.group.checkedButton().text()

            number = int(" ".join(self.lineEditNumber.text().split()).title())
            fio = " ".join(self.lineEditFio.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            sex = self.lineEditSex
            phone = " ".join(self.lineEditPhone.text().split()).title()
            number_audit = " ".join(self.lineEditNumberAudit.text().split()).title()
            date_start = date(yearDS, monthDS, dayDS)
            stag = int(" ".join(self.lineEditStag.text().split()).title())
            obrazovanie = " ".join(self.lineEditObrazovanie.text().split()).title()
            id_cent = int(self.lineEditCenter.currentText()[0])
            id_dolg = int(self.lineEditDolg.currentText()[0])
            zapis = (fio, birthday, sex, phone, number_audit, date_start, stag, obrazovanie, id_cent, id_dolg, number)
            newRow = "UPDATE sotr SET fio = %s, birthday = %s, sex = %s, phone = %s, number_audit = %s, data_start = %s, stag = %s, obrazovanie = %s, id_cent = %s, id_dolg = %s WHERE id_sotr = %s"

            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()
            
            self.lineEditNumber.clear()
            self.lineEditFio.clear()
            self.lineEditPhone.clear()
            self.lineEditNumberAudit.clear()
            self.lineEditStag.clear()
            self.lineEditObrazovanie.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Информация о сотруднике отредактирована")
            self.close()  




















        
