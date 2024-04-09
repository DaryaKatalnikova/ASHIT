import sys
import connect_db
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt, QRegularExpression #QRegExp
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QMessageBox,
)

class EditCenter(QWidget):
    def __init__(self, number, name, urad, factad, phone, email, site, schet, gendir):
        super().__init__()
        
        self.number = number
        self.name = name
        self.urad = urad
        self.factad = factad
        self.phone = phone
        self.email = email
        self.site = site
        self.schet = schet
        self.gendir = gendir

        self.setFixedSize(320, 478)
        self.setWindowTitle("Редактировать")
        self.initUI()

    def initUI(self):
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        self.lineEditNumber = QLineEdit(self)
        self.lineEditNumber.setFixedSize(300, 25)
        self.lineEditNumber.setText(str(self.number))
        self.lineEditNumber.setObjectName("Номер")
        self.lineEditNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditNumber.move(15, 25)
   
#Name
        labelName = QLabel("<font color='#FF3300'>*</font> Название", self)
        labelName.move(15, 55)

        self.lineEditName = QLineEdit(self)
        self.lineEditName.setFixedSize(300, 25)
        self.lineEditName.setText(self.name)
        self.lineEditName.setObjectName("Название")
        self.lineEditName.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditName.move(15, 70)
        
        
#urad
        labelUrAd = QLabel("<font color='#FF3300'>*</font> Юридический адрес", self)
        labelUrAd.move(15, 100)

        self.lineEditUrAd = QLineEdit(self)
        self.lineEditUrAd.setFixedSize(300, 25)
        self.lineEditUrAd.setText(self.urad)
        self.lineEditUrAd.setObjectName("Юридический адрес")
        self.lineEditUrAd.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-]+")))
        self.lineEditUrAd.move(15, 115)

#factad
        labelFactAd = QLabel("<font color='#FF3300'>*</font> Фактический адрес", self)
        labelFactAd.move(15, 145)

        self.lineEditFactAd = QLineEdit(self)
        self.lineEditFactAd.setFixedSize(300, 25)
        self.lineEditFactAd.setText(self.factad)
        self.lineEditFactAd.setObjectName("Фактический адрес")
        self.lineEditFactAd.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-]+")))
        self.lineEditFactAd.move(15, 160)
        
#phone
        labelPhone = QLabel("<font color='#FF3300'>*</font> Телефон", self)
        labelPhone.move(15, 190)

        self.lineEditPhone = QLineEdit(self)
        self.lineEditPhone.setFixedSize(300, 25)
        self.lineEditPhone.setText(self.phone)
        self.lineEditPhone.setObjectName("Телефон")
        self.lineEditPhone.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))
        self.lineEditPhone.move(15, 205)
#e-mail
        labelEmail = QLabel("<font color='#FF3300'>*</font> E-mail", self)
        labelEmail.move(15, 235)

        self.lineEditEmail = QLineEdit(self)
        self.lineEditEmail.setFixedSize(300, 25)
        self.lineEditEmail.setText(self.email)
        self.lineEditEmail.setObjectName("Email")
        self.lineEditEmail.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9@._-]+")))
        self.lineEditEmail.move(15, 250)
#site
        labelSite = QLabel("<font color='#FF3300'>*</font> Сайт", self)
        labelSite.move(15, 280)

        self.lineEditSite = QLineEdit(self)
        self.lineEditSite.setFixedSize(300, 25)
        self.lineEditSite.setText(self.site)
        self.lineEditSite.setObjectName("Сайт")
        self.lineEditSite.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.]+")))
        self.lineEditSite.move(15, 295)
#schet
        labelSchet = QLabel("<font color='#FF3300'>*</font> Счет", self)
        labelSchet.move(15, 325)

        self.lineEditSchet = QLineEdit(self)
        self.lineEditSchet.setFixedSize(300, 25)
        self.lineEditSchet.setText(str(self.schet))
        self.lineEditSchet.setObjectName("Счет")
        self.lineEditSchet.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9.]+")))
        self.lineEditSchet.move(15, 340)
#gendir
        labelGenDir = QLabel("<font color='#FF3300'>*</font> Директор", self)
        labelGenDir.move(15, 370)

        self.lineEditGenDir = QLineEdit(self)
        self.lineEditGenDir.setFixedSize(300, 25)
        self.lineEditGenDir.setText(self.gendir)
        self.lineEditGenDir.setObjectName("Директор")
        self.lineEditGenDir.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditGenDir.move(15, 385)

        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(72, 445)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 445)

        buttonDelete = QPushButton("Удалить", self)
        buttonDelete.move(154, 445)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked.connect(self.close)
        buttonDelete.clicked.connect(self.Deleting)

    def Deleting(self):
        number = int(" ".join(self.lineEditNumber.text().split()).title())
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        delete_status = "DELETE FROM center WHERE id_cent = '%d'" % (number)
        with connection.cursor() as cursor:
            cursor.execute(delete_status)
            connection.commit()
            self.close()

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
        number = int(" ".join(self.lineEditNumber.text().split()).title())
        name = " ".join(self.lineEditName.text().split()).title()
        urad = " ".join(self.lineEditUrAd.text().split()).title()
        factad = " ".join(self.lineEditFactAd.text().split()).title()
        phone = " ".join(self.lineEditPhone.text().split()).title()
        email = " ".join(self.lineEditEmail.text().split()).title()
        site = " ".join(self.lineEditSite.text().split()).title()
        schet = float(" ".join(self.lineEditSchet.text().split()).title())
        gendir = " ".join(self.lineEditGenDir.text().split()).title()

        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        cursor = connection.cursor()
        zapis = (name, urad, factad, phone, email, site, schet, gendir, number)
        newRow = "UPDATE center SET nameCenter = %s, ur_adr = %s, fact_adr = %s, phone = %s, e_mail = %s, site = %s, finansy = %s, director = %s WHERE id_cent = %s"
        with connection.cursor() as cursor:
            for result in cursor.execute(newRow, zapis, multi=True):
                connection.commit()
                break
            connection.close()
            
        self.lineEditNumber.clear()
        self.lineEditName.clear()
        self.lineEditUrAd.clear()
        self.lineEditFactAd.clear()
        self.lineEditPhone.clear()
        self.lineEditEmail.clear()
        self.lineEditSite.clear()
        self.lineEditSchet.clear()
        self.lineEditGenDir.clear()
        
        dialog = QMessageBox.information(self, "Отредактировано", "Центр отредактирован")
        self.close() 

    





















        
