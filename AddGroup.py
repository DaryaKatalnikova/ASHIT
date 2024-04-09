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


class AddGroup(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 553)
        self.setWindowTitle("Добавить")
        self.initUI()

    def initUI(self):

        select_sotrs = "SELECT * FROM sotr"
        sotrs = execute_read_query(connection, select_sotrs)
        lSotrs = list()
        for s in sotrs:
            lSotrs.append(str(s).split(',')[0][1:] + " " + str(s).split(',')[1][2:len(str(s).split(',')[1]) - 1])
        
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_group FROM groupn"
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
        labelName.move(15, 60)

        self.lineAddName = QLineEdit(self)
        self.lineAddName.setObjectName("Название группы")
        self.lineAddName.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9-]+")))
        self.lineAddName.move(15, 75)
        
#id_stat
        labelSotr = QLabel("<font color='#FF3300'>*</font>Наставник", self)
        labelSotr.move(15, 100)
        
        self.lineAddSotr = QComboBox(self)
        self.lineAddSotr.setObjectName("Сотрудник")
        self.lineAddSotr.addItems(lSotrs)
        self.lineAddSotr.move(15, 115)
       
        
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
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            name = " ".join(self.lineAddName.text().split()).title()
            id_sotr = int(self.lineAddSotr.currentText()[0])
            zapis = (number, name, id_sotr)
            newRow = "insert into groupn (id_group, name_group, id_sotr) Values (%s, %s, %s)"

            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()

            self.lineAddNumber.clear()
            self.lineAddName.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новая группа добавлена")
            self.close()






















        
