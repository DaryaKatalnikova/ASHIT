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
    QComboBox
    
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

class EditRel(QWidget):
    def __init__(self, number, fio, birthday, address, phoneL, email, job, phoneJ, id_zayavka):
        super().__init__()

        self.number = number
        self.fio = fio
        self.birthday = birthday
        self.address = address
        self.phoneL = phoneL
        self.email = email
        self.job = job
        self.phoneJ = phoneJ
        self.id_zayavka = id_zayavka

        self.setFixedSize(320, 553)
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_zayavkas = "SELECT * FROM zayavka"
        zayavkas = execute_read_query(connection, select_zayavkas)
        lZayavkas = list()
        for z in zayavkas:
            lZayavkas.append(str(z).split(',')[0][1:] + " " + str(z).split(',')[1][2:len(str(z).split(',')[1]) - 1])

        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        self.lineEditNumber = QLineEdit(self)
        self.lineEditNumber.setFixedSize(300, 25)
        self.lineEditNumber.setText(str(self.number))
        self.lineEditNumber.setObjectName("Номер")
        self.lineEditNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditNumber.move(15, 25)
      
#fiorel
        labelFioRel = QLabel("<font color='#FF3300'>*</font> ФИО Родителя", self)
        labelFioRel.move(15, 55)

        self.lineEditFioRel = QLineEdit(self)
        self.lineEditFioRel.setFixedSize(300, 25)
        self.lineEditFioRel.setText(self.fio)
        self.lineEditFioRel.setObjectName("ФИО родителя")
        self.lineEditFioRel.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я ]+")))
        self.lineEditFioRel.move(15, 70)
        
#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата Рождения", self)
        labelBirthday.move(15, 100)

        self.lineEditBirthday = QDateEdit(self)
        self.lineEditBirthday.setFixedSize(300, 25)
        self.lineEditBirthday.setDate(self.birthday)
        self.lineEditBirthday.setObjectName("Дата рождения")
        self.lineEditBirthday.move(15, 115)

#address
        labelAdress = QLabel("<font color='#FF3300'>*</font> Адрес", self)
        labelAdress.move(15, 145)

        self.lineEditAdress = QLineEdit(self)
        self.lineEditAdress.setFixedSize(300, 25)
        self.lineEditAdress.setText(self.address)
        self.lineEditAdress.setObjectName("Адрес")
        self.lineEditAdress.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-.,/ ]+")))
        self.lineEditAdress.move(15, 160)

#phoneL
        labelPhoneL = QLabel("<font color='#FF3300'>*</font> Номер Телефона (личный)", self)
        labelPhoneL.move(15, 190)
        
        self.lineEditPhoneL = QLineEdit(self)
        self.lineEditPhoneL.setFixedSize(300, 25)
        self.lineEditPhoneL.setText(self.phoneL)
        self.lineEditPhoneL.setObjectName("Телефон л")
        self.lineEditPhoneL.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineEditPhoneL.move(15, 205)
     
#email
        labelEmail = QLabel("Email", self)
        labelEmail.move(15, 235)
        
        self.lineEditEmail = QLineEdit(self)
        self.lineEditEmail.setFixedSize(300, 25)
        self.lineEditEmail.setText(self.email)
        self.lineEditEmail.setObjectName("Email")
        self.lineEditEmail.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я.@_]+")))
        self.lineEditEmail.move(15, 250)

#Job
        labelJob = QLabel("Место работы", self)
        labelJob.move(15, 280)
        
        self.lineEditJob = QLineEdit(self)
        self.lineEditJob.setFixedSize(300, 25)
        self.lineEditJob.setText(self.job)
        self.lineEditJob.setObjectName("Место работы")
        self.lineEditJob.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,/-_ ]+")))
        self.lineEditJob.move(15, 295)

#phoneJ
        labelPhoneJ = QLabel("Номер Телефона (Рабочий)", self)
        labelPhoneJ.move(15, 325)
        
        self.lineEditPhoneJ = QLineEdit(self)
        self.lineEditPhoneJ.setFixedSize(300, 25)
        self.lineEditPhoneJ.setText(self.phoneJ)
        self.lineEditPhoneJ.setObjectName("Телефон h")
        self.lineEditPhoneJ.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineEditPhoneJ.move(15, 340)

#id_zayavka
        labelZayavka = QLabel("Номер заявки", self)
        labelZayavka.move(15, 370)
        
        self.lineEditZayavka = QComboBox(self)
        self.lineEditZayavka.addItems(lZayavkas)
        self.lineEditZayavka.setFixedSize(300, 25)
        for zay in lZayavkas:
            if str(self.id_zayavka) in zay:
                self.lineEditZayavka.setCurrentText(zay)
        self.lineEditZayavka.move(15, 385)
        

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
        delete_status = "DELETE FROM relation WHERE id_rel = '%d'" % (number)
        with connection.cursor() as cursor:
            cursor.execute(delete_status)
            connection.commit()
            self.close()

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
            yearB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[0])
            monthB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[1])
            dayB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[2])

            number = int(" ".join(self.lineEditNumber.text().split()).title())
            fio_rel = " ".join(self.lineEditFioRel.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            address = " ".join(self.lineEditAdress.text().split()).title()
            phoneL = " ".join(self.lineEditPhoneL.text().split()).title()
            email = " ".join(self.lineEditEmail.text().split()).title()
            job = " ".join(self.lineEditJob.text().split()).title()
            phoneJ = " ".join(self.lineEditPhoneJ.text().split()).title()
            id_zayavka = int(self.lineEditZayavka.currentText()[0])
            
            zapis = (fio_rel, birthday, address, phoneL, email, job, phoneJ, id_zayavka, number)
            newRow = "update relation set fio_rel =%s, birthday = %s, address = %s, phoneL = %s, e_mail = %s, job = %s, phoneJ = %s, id_zayavka = %s where id_rel = %s"

            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()

            self.lineEditNumber.clear()
            self.lineEditFioRel.clear()
            self.lineEditAdress.clear()
            self.lineEditPhoneL.clear()
            self.lineEditEmail.clear()
            self.lineEditJob.clear()
            self.lineEditPhoneJ.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Информация о родителе отредактирована")
            self.close()