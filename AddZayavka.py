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

class AddZayavka(QWidget):
    def __init__(self):
        super().__init__()

        #self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(320, 553)
        self.setWindowTitle("Добавить")
        self.initUI()

    def initUI(self):
        select_statuss = "SELECT * FROM statusz"
        statuss = execute_read_query(connection, select_statuss)
        lStatuss = list()
        for s in statuss:
            lStatuss.append(str(s).split(',')[0][1:] + " " + str(s).split(',')[1][2:len(str(s).split(',')[1]) - 2])

        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_centers = "SELECT id_zayavka FROM zayavka"
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
        self.lineAddFioRel.setObjectName("ФИО Родителя")
        self.lineAddFioRel.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddFioRel.move(15, 70)
        
#fiochild
        labelChild = QLabel("<font color='#FF3300'>*</font> ФИО Ребенка", self)
        labelChild.move(15, 100)

        self.lineAddFioChild = QLineEdit(self)
        self.lineAddFioChild.setObjectName("ФИО Ребенка")
        self.lineAddFioChild.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineAddFioChild.move(15, 115)

#data_zap
        labelDataZap = QLabel("<font color='#FF3300'>*</font> Дата Заполнения", self)
        labelDataZap.move(15, 145)

        self.lineAddDataZap = QDateEdit(self)
        self.lineAddDataZap.setObjectName("Дата заполнения")
        self.lineAddDataZap.move(15, 160)

#id_stat
        labelStatus = QLabel("Статус Заявки", self)
        labelStatus.move(15, 190)

        self.lineAddStatus = QComboBox(self)
        self.lineAddStatus.setObjectName("Статус заявки")
        self.lineAddStatus.addItems(lStatuss)
        self.lineAddStatus.move(15, 205)
       

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
            yearZ = int(self.lineAddDataZap.date().toString("yyyy.MM.dd").split('.')[0])
            mouthZ = int(self.lineAddDataZap.date().toString("yyyy.MM.dd").split('.')[1])
            dayZ = int(self.lineAddDataZap.date().toString("yyyy.MM.dd").split('.')[2])
        
            number = int(" ".join(self.lineAddNumber.text().split()).title())
            fio_rel = " ".join(self.lineAddFioRel.text().split()).title()
            fio_child = " ".join(self.lineAddFioChild.text().split()).title()
            data_zap = date(yearZ, mouthZ, dayZ)
            id_stat = int(self.lineAddStatus.currentText()[0])
            zapis = (number, fio_rel, fio_child, data_zap, id_stat)
            newRow = "INSERT INTO zayavka (id_zayavka, fio_rel, fio_chil, date_zap, id_stat) VALUES (%s, %s, %s, %s, %s)"
            
            cursor.execute(newRow, zapis)  
            connection.commit()
            connection.close()
        
            self.lineAddNumber.clear()
            self.lineAddFioRel.clear()
            self.lineAddFioChild.clear()
            self.lineAddDataZap.clear()
            self.lineAddStatus.clear()

            QMessageBox.information(self, "Новая заявка", "Добавлена")
            self.close()
        
      























        
