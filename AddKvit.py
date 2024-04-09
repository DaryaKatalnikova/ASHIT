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

class AddKvit(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(320, 478)
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_kvits = """select children.id_child, children.fio_child from children, kvit
        where kvit.id_child = children.id_child"""
        kvits = execute_read_query(connection, select_kvits)
        lkvits = set()
        for c in kvits:
            lkvits.add(str(c).split(',')[0][1:] + " " + str(c).split(',')[1][2:len(str(c).split(',')[1]) - 2])
      
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)

        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_kvit FROM kvit"
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
      
        labelChild = QLabel("<font color='#FF3300'>*</font> Ребенок", self)
        labelChild.move(15, 90)
        
        self.lineAddChild = QComboBox(self)
        self.lineAddChild.addItems(lkvits)
        self.lineAddChild.move(15, 105)

#summa
        labelSumma = QLabel("<font color='#FF3300'>*</font> Сумма", self)
        labelSumma.move(15, 50)

        self.lineAddSumma = QLineEdit(self)
        self.lineAddSumma.setObjectName("Номер")
        self.lineAddSumma.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9.,]+")))
        self.lineAddSumma.move(15, 65)


#date_opl
        labelDateOpl = QLabel("<font color='#FF3300'>*</font> Дата Оплаты", self)
        labelDateOpl.move(15, 130)

        self.lineAddDateOpl = QDateEdit(self)
        self.lineAddDateOpl.move(15, 145)

        

        buttonAcept = QPushButton("Сохранить", self)
        buttonAcept.move(154, 445)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 445)

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
            yearB = int(self.lineAddDateOpl.date().toString("yyyy.MM.dd").split('.')[0])
            monthB = int(self.lineAddDateOpl.date().toString("yyyy.MM.dd").split('.')[1])
            dayB = int(self.lineAddDateOpl.date().toString("yyyy.MM.dd").split('.')[2])
            
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            summa = int(" ".join(self.lineAddSumma.text().split()).title())
            id_child = int(self.lineAddChild.currentText()[0])
            date_opl = date(yearB, monthB, dayB)

            zapis = (number, summa, id_child, date_opl)
            newRow = "insert into kvit (id_kvit, summa, id_child, date_opl) values (%s, %s, %s, %s)"

            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()

            self.lineAddNumber.clear()
            self.lineAddSumma.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новая оплата добавлена")
            self.close()




















        
