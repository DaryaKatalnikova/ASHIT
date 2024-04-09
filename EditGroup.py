import sys
import connect_db
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt, QRegularExpression #QRegExp
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QComboBox,
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

class EditGroup(QWidget):
    def __init__(self, number, name, id_sotr):
        super().__init__()
        self.number = number
        self.name = name
        self.id_sotr = id_sotr

        self.setFixedSize(320, 553)
        self.setWindowTitle("Редактировать")
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_sotrs = "SELECT * FROM sotr"
        sotrs = execute_read_query(connection, select_sotrs)
        lSotrs = list()
        for s in sotrs:
            lSotrs.append(str(s).split(',')[0][1:] + " " + str(s).split(',')[1][2:len(str(s).split(',')[1]) - 1])

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
        self.lineEditName.setObjectName("Название группы")
        self.lineEditName.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-]+")))
        self.lineEditName.move(15, 70)
        
#id_sotr
        labelSotr = QLabel("<font color='#FF3300'>*</font> Наставник", self)
        labelSotr.move(15, 100)
        
        self.lineEditSotr = QComboBox(self)
        self.lineEditSotr.setObjectName("Наставник")
        self.lineEditSotr.addItems(lSotrs)
        for sotr in lSotrs:
            if str(self.id_sotr) in sotr:
                self.lineEditSotr.setCurrentText(sotr)
        self.lineEditSotr.setFixedSize(300, 25)
        self.lineEditSotr.move(15, 115)
        
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
        delete_groups = "delete from groupn where id_group = '%s'" % (number)
        with connection.cursor() as cursor:
            cursor.execute(delete_groups)
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
            cursor = connection.cursor()
            number = int(" ".join(self.lineEditNumber.text().split()).title())
            name = " ".join(self.lineEditName.text().split()).title()
            id_sotr = int(self.lineEditSotr.currentText())
            zapis = (name, id_sotr, number)
            newRow = "Update groupn set name_group = %s, id_sotr = %s where id_group = %s"
      
            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()
            
            self.lineEditNumber.clear()
            self.lineEditNumber.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Информация о группе отредактирована")
            self.close()  
