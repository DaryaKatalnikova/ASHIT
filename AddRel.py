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

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

class AddRel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить")
        self.setFixedSize(320, 553)
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_zayavkas = "SELECT * FROM zayavka"
        zayavkas = execute_read_query(connection, select_zayavkas)
        lZayavkas = list()
        for z in zayavkas:
            lZayavkas.append(str(z).split(',')[0][1:]+ ' ' + str(z).split(',')[2][2:len(str(z).split(',')[2]) - 1])


        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_rel FROM relation"
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
      
#fiorel
        labelFioRel = QLabel("<font color='#FF3300'>*</font> ФИО Родителя", self)
        labelFioRel.move(15, 55)

        self.lineAddFioRel = QLineEdit(self)
        self.lineAddFioRel.setObjectName("ФИО родителя")
        self.lineAddFioRel.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddFioRel.move(15, 70)
        
#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата Рождения", self)
        labelBirthday.move(15, 100)

        self.lineAddBirthday = QDateEdit(self)
        self.lineAddBirthday.setObjectName("Дата рождения")
        self.lineAddBirthday.move(15, 115)

#address
        labelAdress = QLabel("<font color='#FF3300'>*</font> Адрес", self)
        labelAdress.move(15, 145)

        self.lineAddAdress = QLineEdit(self)
        self.lineAddAdress.setObjectName("Адрес")
        self.lineAddAdress.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-.,/]+")))
        self.lineAddAdress.move(15, 160)

#phoneL
        labelPhoneL = QLabel("<font color='#FF3300'>*</font> Номер Телефона (личный)", self)
        labelPhoneL.move(15, 190)
        
        self.lineAddPhoneL = QLineEdit(self)
        self.lineAddPhoneL.setObjectName("Телефон л")
        self.lineAddPhoneL.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineAddPhoneL.move(15, 205)
     
#email
        labelEmail = QLabel("Email", self)
        labelEmail.move(15, 235)
        
        self.lineAddEmail = QLineEdit(self)
        self.lineAddEmail.setObjectName("Email")
        self.lineAddEmail.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я.@_]+")))
        self.lineAddEmail.move(15, 250)

#Job
        labelJob = QLabel("Место работы", self)
        labelJob.move(15, 280)
        
        self.lineAddJob = QLineEdit(self)
        self.lineAddJob.setObjectName("Место работы")
        self.lineAddJob.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,/-_]+")))
        self.lineAddJob.move(15, 295)

#phoneJ
        labelPhoneJ = QLabel("Номер Телефона (Рабочий)", self)
        labelPhoneJ.move(15, 325)
        
        self.lineAddPhoneJ = QLineEdit(self)
        self.lineAddPhoneJ.setObjectName("Телефон h")
        self.lineAddPhoneJ.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineAddPhoneJ.move(15, 340)

#id_zayavka
        labelZayavka = QLabel("Номер заявки", self)
        labelZayavka.move(15, 370)
        
        self.lineAddZayavka = QComboBox(self)
        self.lineAddZayavka.setObjectName("Заявка")
        self.lineAddZayavka.addItems(lZayavkas)
        self.lineAddZayavka.move(15, 385)
       

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
            fio_rel = " ".join(self.lineAddFioRel.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            address = " ".join(self.lineAddAdress.text().split()).title()
            phoneL = " ".join(self.lineAddPhoneL.text().split()).title()
            email = " ".join(self.lineAddEmail.text().split()).title()
            job = " ".join(self.lineAddJob.text().split()).title()
            phoneJ = " ".join(self.lineAddPhoneJ.text().split()).title()
            id_zayavka = int(self.lineAddZayavka.currentText()[0])
            
            zapis = (number, fio_rel, birthday, address, phoneL, email, job, phoneJ, id_zayavka)
            newRow = """insert into relation (id_rel, fio_rel, bithday, address, phoneL, email, job, phoneJ, id_zayavka) 
            Values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()
            self.lineAddNumber.clear()
            self.lineAddFioRel.clear()
            self.lineAddAdress.clear()
            self.lineAddPhoneL.clear()
            self.lineAddEmail.clear()
            self.lineAddJob.clear()
            self.lineAddPhoneJ.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новый родитель добавлен")
            self.close()