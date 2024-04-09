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

class EditStatus(QWidget):
    def __init__(self, number, name):
        super().__init__()
        
        self.number = number
        self.name = name
      
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
        delete_status = "DELETE FROM statusz WHERE id_stat = '%d'" % (number)
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
            zapis = (name, number)
            newRow = "UPDATE statusz SET nameStat = %s WHERE id_stat = %s"
            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()
            
            self.lineEditNumber.clear()
            self.lineEditName.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Статус отредактирован")
            self.close()   
    





















        
