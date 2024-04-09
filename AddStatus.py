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

class AddStatus(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setFixedSize(320, 478)
        self.setWindowTitle("Добавить")
        self.initUI()

    def initUI(self):
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)

        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_status FROM statusz"
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
        
        self.lineAddStatus = QLineEdit(self)
        self.lineAddStatus.setObjectName("Номер")
        self.lineAddStatus.setText(k)
        self.lineAddStatus.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineAddStatus.move(15, 25)
      
#Name
        labelName = QLabel("<font color='#FF3300'>*</font> Название", self)
        labelName.move(15, 55)

        self.lineAddName = QLineEdit(self)
        self.lineAddName.setObjectName("Название")
        self.lineAddName.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddName.move(15, 70)


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
            number = int(" ".join(self.lineAddStatus.text().split()).title())
            name = " ".join(self.lineAddName.text().split()).title()
            zapis = (number, name)
            newRow = "INSERT INTO statusz ( id_stat, nameStat ) VALUES ( %s, %s )"
            
            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()
            
            self.lineAddStatus.clear()
            self.lineAddName.clear()

            dialog = QMessageBox.information(self, "Добавлено", "Новый статус добавлен")
            self.close()
        






















        
