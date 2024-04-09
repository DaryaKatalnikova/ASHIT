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
    QComboBox,
    QDateEdit
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

class EditChild(QWidget):
    def __init__(self, number, fio_child, birthday, address, id_rel, id_group):
        super().__init__()

        self.number = number
        self.fio_child = fio_child
        self.birthday = birthday
        self.address = address
        self.id_rel = id_rel
        self.id_group = id_group

        #self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(320, 553)
        self.initUI()

    def initUI(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
        select_rels = "SELECT * FROM relation"
        rels = execute_read_query(connection, select_rels)
        lRels = list()
        for r in rels:
            lRels.append(str(r).split(',')[0][1:] + " " + str(r).split(',')[1][2:len(str(r).split(',')[1]) - 1])
        print(lRels)

        select_groups = "SELECT * FROM groupn"
        groups = execute_read_query(connection, select_groups)
        lGroups = list()
        for g in groups:
            lGroups.append(str(g).split(',')[0][1:] + " " +str(g).split(',')[1][2:len(str(g).split(',')[1]) - 1])
        
        IdLabel = QLabel("<font color='#FF3300'>*</font> Номер", self)
        IdLabel.move(15, 10)
        
        self.lineEditNumber = QLineEdit(self)
        self.lineEditNumber.setFixedSize(300, 25)
        self.lineEditNumber.setText(str(self.number))
        self.lineEditNumber.setObjectName("Номер")
        self.lineEditNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]+")))
        self.lineEditNumber.move(15, 25)
      
#fiochild
        labelFioChild = QLabel("<font color='#FF3300'>*</font> ФИО Ребенка", self)
        labelFioChild.move(15, 55)

        self.lineEditFioChild = QLineEdit(self)
        self.lineEditFioChild.setFixedSize(300, 25)
        self.lineEditFioChild.setText(self.fio_child)
        self.lineEditFioChild.setObjectName("ФИО Ребенка")
        self.lineEditFioChild.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я]+")))
        self.lineEditFioChild.move(15, 70)
        

#birthday
        labelBirthday = QLabel("<font color='#FF3300'>*</font> Дата Рождения", self)
        labelBirthday.move(15, 100)

        self.lineEditBirthday = QDateEdit(self)
        self.lineEditBirthday.setFixedSize(300, 25)
        self.lineEditBirthday.setDate(self.birthday)
        self.lineEditBirthday.setObjectName("Дата рождения")
        self.lineEditBirthday.move(15, 115)

#adres
        labelAddress = QLabel("<font color='#FF3300'>*</font> Адрес", self)
        labelAddress.move(15, 145)

        self.lineEditAddress = QLineEdit(self)
        self.lineEditAddress.setFixedSize(300, 25)
        self.lineEditAddress.setText(self.address)
        self.lineEditAddress.setObjectName("Адрес")
        self.lineEditAddress.setValidator(QRegularExpressionValidator(QRegularExpression("[a-zA-Zа-яА-Я0-9.,-/]+")))
        self.lineEditAddress.move(15, 160)

#id_rel
        labelRel = QLabel("<font color='#FF3300'>*</font> Родитель", self)
        labelRel.move(15, 190)
        
        self.lineEditRel = QComboBox(self)
        self.lineEditRel.addItems(lRels)
        self.lineEditRel.setFixedSize(300, 25)
        for rel in lRels:
            if str(self.id_rel) in rel:
                self.lineEditRel.setCurrentText(rel)
        self.lineEditRel.move(15, 205)
    

#id_group
        labelGroup = QLabel("Группа", self)
        labelGroup.move(15, 235)
        
        self.lineEditGroup = QComboBox(self)
        self.lineEditGroup.addItems(lGroups)
        self.lineEditGroup.setFixedSize(300, 25)
        for group in lGroups:
            if str(self.id_group) in group:
                self.lineEditGroup.setCurrentText(group)
        self.lineEditGroup.move(15, 250)
        

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
        delete_status = "DELETE FROM children WHERE id_child = '%d'" % (number)
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
            cursor = connection.cursor()
            connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")
            cursor = connection.cursor()
            yearB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[0])
            monthB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[1])
            dayB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[2])
            number = int(" ".join(self.lineEditNumber.text().split()).title())
            fio_child = " ".join(self.lineEditFioChild.text().split()).title()
            birthday = date(yearB, monthB, dayB)
            address = " ".join(self.lineEditAddress.text().split()).title()
            id_rel = int(self.lineEditRel.currentText()[0])
            id_group = int(self.lineEditGroup.currentText()[0])
            zapis = (fio_child, birthday, address, id_rel, id_group, number)
            newRow = "Update children set fio_child = %s, birthday = %s, address = %s, id_rel = %s, id_group = %s where id_child = %s"

            with connection.cursor() as cursor:
                for result in cursor.execute(newRow, zapis, multi=True):
                    connection.commit()
                    break
                connection.close()
       
            self.lineEditNumber.clear()
            self.lineEditFioChild.clear()
            self.lineEditAddress.clear()

            dialog = QMessageBox.information(self, "Отредактировано", "Информация о ребенке отредактирована")
            self.close() 