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

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

class AddCenter(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 478)
        self.setWindowTitle("Добавить")
        self.initUI()

    def initUI(self):
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_cent FROM center"
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
      
#Name
        labelName = QLabel("<font color='#FF3300'>*</font> Название", self)
        labelName.move(15, 55)

        self.lineAddName = QLineEdit(self)
        self.lineAddName.setObjectName("Название")
        self.lineAddName.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9]+")))
        self.lineAddName.move(15, 70)
        
#urad
        labelUrAd = QLabel("<font color='#FF3300'>*</font> Юридический адрес", self)
        labelUrAd.move(15, 100)

        self.lineAddUrAd = QLineEdit(self)
        self.lineAddUrAd.setObjectName("Юридический адрес")
        self.lineAddUrAd.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-]+")))
        self.lineAddUrAd.move(15, 115)

#factad
        labelFactAd = QLabel("<font color='#FF3300'>*</font> Фактический адрес", self)
        labelFactAd.move(15, 145)

        self.lineAddFactAd = QLineEdit(self)
        self.lineAddFactAd.setObjectName("Фактический адрес")
        self.lineAddFactAd.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-]+")))
        self.lineAddFactAd.move(15, 160)
        
#phone
        labelPhone = QLabel("<font color='#FF3300'>*</font> Телефон", self)
        labelPhone.move(15, 190)

        self.lineAddPhone = QLineEdit(self)
        self.lineAddPhone.setObjectName("Телефон")
        self.lineAddPhone.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9-]+")))#
        self.lineAddPhone.move(15, 205)
#e-mail
        labelEmail = QLabel("<font color='#FF3300'>*</font> E-mail", self)
        labelEmail.move(15, 235)

        self.lineAddEmail = QLineEdit(self)
        self.lineAddEmail.setObjectName("Email")
        self.lineAddEmail.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9@._-]+")))#
        self.lineAddEmail.move(15, 250)
#site
        labelSite = QLabel("<font color='#FF3300'>*</font> Сайт", self)
        labelSite.move(15, 280)

        self.lineAddSite = QLineEdit(self)
        self.lineAddSite.setObjectName("Сайт")
        self.lineAddSite.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.]+")))#
        self.lineAddSite.move(15, 295)
#schet
        labelSchet = QLabel("<font color='#FF3300'>*</font> Счет", self)
        labelSchet.move(15, 325)

        self.lineAddSchet = QLineEdit(self)
        self.lineAddSchet.setObjectName("Счет")
        self.lineAddSchet.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9.]+")))
        self.lineAddSchet.move(15, 340)
#gendir
        labelGenDir = QLabel("<font color='#FF3300'>*</font> Директор", self)
        labelGenDir.move(15, 370)

        self.lineAddGenDir = QLineEdit(self)
        self.lineAddGenDir.setObjectName("Директор")
        self.lineAddGenDir.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddGenDir.move(15, 385)

        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(154, 445)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 445)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked .connect(self.close)

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
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            name = " ".join(self.lineAddName.text().split()).title()
            urad = " ".join(self.lineAddUrAd.text().split()).title()
            factad = " ".join(self.lineAddFactAd.text().split()).title()
            phone = " ".join(self.lineAddPhone.text().split()).title()
            email = " ".join(self.lineAddEmail.text().split()).title()
            site = " ".join(self.lineAddSite.text().split()).title()
            schet = float(" ".join(self.lineAddSchet.text().split()).title())
            gendir = " ".join(self.lineAddGenDir.text().split()).title()
            
            zapis = (number, name, urad, factad, phone, email, site, schet, gendir)
            newRow = "INSERT INTO center (id_cent, nameCenter, ur_adr, fact_adr, phone, e_mail, site, finansy, director) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()
            
            self.lineAddNumber.clear()
            self.lineAddName.clear()
            self.lineAddUrAd.clear()
            self.lineAddFactAd.clear()
            self.lineAddPhone.clear()
            self.lineAddEmail.clear()
            self.lineAddSite.clear()
            self.lineAddSchet.clear()
            self.lineAddGenDir.clear()
            
            dialog = QMessageBox.information(self, "Добавлено", "Новый центр добавлен")
            self.close()
        
      





















        
