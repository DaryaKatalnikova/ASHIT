import sys
import connect_db
from datetime import date 
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt, QRegularExpression #QRegExp
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QDateEdit,
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

class EditZayavka(QWidget):
    def __init__(self, number, fio_rel, fio_child, date_zap, id_stat):
        super().__init__()
        
        self.number = number
        self.fio_rel = fio_rel
        self.fio_child = fio_child
        self.date_zap = date_zap
        self.id_stat = id_stat
    
        self.setFixedSize(320, 553)
        self.setWindowTitle("Редактирование")
        self.initUI()

    def initUI(self):
        select_statuss = "SELECT * FROM statusz"
        statuss = execute_read_query(connection, select_statuss)
        lStatuss = list()
        for s in statuss:
            lStatuss.append(str(s).split(',')[0][1:] + " " + str(s).split(',')[1][2:len(str(s).split(',')[1]) - 2])
        
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        self.lineEditNumber = QLineEdit(self)
        self.lineEditNumber.setFixedSize(300, 25)
        self.lineEditNumber.setText(str(self.number))
        self.lineEditNumber.setObjectName("Номер")
        self.lineEditNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditNumber.move(15, 25)
   
#fio_rel
        labelFioRel = QLabel("<font color='#FF3300'>*</font> ФИО Родителя", self)
        labelFioRel.move(15, 55)

        self.lineEditFioRel = QLineEdit(self)
        self.lineEditFioRel.setFixedSize(300, 25)
        self.lineEditFioRel.setText(self.fio_rel)
        self.lineEditFioRel.setObjectName("ФИО Родителя")
        self.lineEditFioRel.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditFioRel.move(15, 70)
        
        
#fio_child
        labelFioChild = QLabel("<font color='#FF3300'>*</font> ФИО Ребенка", self)
        labelFioChild.move(15, 100)

        self.lineEditFioChild = QLineEdit(self)
        self.lineEditFioChild.setFixedSize(300, 25)
        self.lineEditFioChild.setText(self.fio_child)
        self.lineEditFioChild.setObjectName("ФИО Ребенка")
        self.lineEditFioChild.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditFioChild.move(15, 115)

#data_zap
        labelDateZap = QLabel("<font color='#FF3300'>*</font> Дата Заполнения", self)
        labelDateZap.move(15, 145)

        self.lineEditDateZap = QDateEdit(self)
        self.lineEditDateZap.setFixedSize(300, 25)
        self.lineEditDateZap.setDate(self.date_zap)
        self.lineEditDateZap.setObjectName("Дата заполнения")
        self.lineEditDateZap.move(15, 160)
        
#id_stat
        labelStatus = QLabel("<font color='#FF3300'>*</font> Статус заявки", self)
        labelStatus.move(15, 190)

        self.lineEditStatus = QComboBox(self)
        self.lineEditStatus.setFixedSize(300, 25)
        self.lineEditStatus.setObjectName("Статус")
        self.lineEditStatus.addItems(lStatuss)
        for stat in lStatuss:
            if self.id_stat != None and self.id_stat in stat:
                self.lineEditStatus.setCurrentText(stat)
        self.lineEditStatus.move(15, 205)

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
        delete_zayavka = "DELETE FROM zayavka WHERE id_zayavka = '%d'" % (number)
        with connection.cursor() as cursor:
            cursor.execute(delete_zayavka)
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
            yearZ = int(self.lineEditDateZap.date().toString("yyyy.MM.dd").split('.')[0])
            mouthZ = int(self.lineEditDateZap.date().toString("yyyy.MM.dd").split('.')[1])
            dayZ = int(self.lineEditDateZap.date().toString("yyyy.MM.dd").split('.')[2])
        
            number = int(" ".join(self.lineEditNumber.text().split()).title())
            fio_rel = " ".join(self.lineEditFioRel.text().split()).title()
            fio_child = " ".join(self.lineEditFioChild.text().split()).title()
            data_zap = date(yearZ, mouthZ, dayZ)
            id_stat = int(self.lineEditStatus.currentText()[0])

            zapis = (fio_rel, fio_child, data_zap, id_stat, number)
            newRow = "Update zayavka SET fio_rel = %s, fio_chil = %s, date_zap = %s, id_stat = %s where id_zayavka = %s"

            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()

            self.lineEditNumber.clear()
            self.lineEditFioRel.clear()
            self.lineEditFioChild.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Информация о заявке отредактирована")
            self.close()  