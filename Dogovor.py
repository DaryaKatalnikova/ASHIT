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
    QDateEdit,
    QComboBox

)
import jinja2
import pdfkit


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


class Dogovor(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(320, 550)
        self.setWindowTitle("Договор")
        self.initUI()

    def initUI(self):

        select_centers = "SELECT * FROM center"
        select_rels = "SELECT * FROM relation"
        select_childs = "SELECT * FROM children"
        #select_groups = "SELECT * FROM groupn"
        centers = execute_read_query(connection, select_centers)
        lCenters = list()
        for c in centers:
            lCenters.append(str(c).split(',')[1][2:len(str(c).split(',')[1]) - 1])
        rels = execute_read_query(connection, select_rels)
        lRels = list()
        for r in rels:
            lRels.append(str(r).split(',')[1][2:len(str(r).split(',')[1]) - 1])
        childs = execute_read_query(connection, select_childs)
        lChilds = list()
        for ch in childs:
            lChilds.append(str(ch).split(',')[0][1:] + " " + str(ch).split(',')[1][2:len(str(ch).split(',')[1]) - 1])
        groups = execute_read_query(connection, select_rels)  
        lGroups = list()
        #for g in groups:
         #   lGroups.append(str(g).split(',')[1][2:len(str(g).split(',')[1]) - 1])
        #disp = ["Кибергигиена", "Основы программирования. Python", "Системное администрирование", "VR/AR", "Мобильная разработка", "Компьютерная графика"]

        IdLabel = QLabel("Номер договора", self)
        IdLabel.move(15, 10)
        
        self.lineAddNumber = QLineEdit(self)
        self.lineAddNumber.setObjectName("Номер")
        self.lineAddNumber.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-zА-Яа-я0-9-]+")))
        self.lineAddNumber.move(15, 25)

        labelCenter = QLabel("Центр", self)
        labelCenter.move(15, 60)
        
        self.lineAddCenter = QComboBox(self)
        self.lineAddCenter.setObjectName("Центр")
        self.lineAddCenter.addItems(lCenters)
        self.lineAddCenter.move(15, 75)
        self.lineAddCenter.currentTextChanged.connect(self.CityAndDir)
        

        labelcity = QLabel("Город", self)
        labelcity.move(15, 110)

        self.lineAddcity = QLineEdit(self)
        self.lineAddcity.setObjectName("Город")
        self.lineAddcity.move(15, 125)
        
        labeldir = QLabel("Директор", self)
        labeldir.move(15, 160)

        self.lineAdddir = QLineEdit(self)
        self.lineAdddir.setObjectName("Директор")
        self.lineAdddir.move(15, 175)

        labelData = QLabel("Дата", self)
        labelData.move(15, 210)

        self.lineAddData = QDateEdit(self)
        self.lineAddData.setObjectName("Дата")
        self.lineAddData.move(15, 225)

        labelFioRel = QLabel("ФИО Родителя", self)
        labelFioRel.move(15, 260)

        self.lineAddFioRel = QComboBox(self)
        self.lineAddFioRel.setObjectName("ФИО Родителя")
        self.lineAddFioRel.addItems(lRels)
        self.lineAddFioRel.move(15, 275)

        labelFioChil = QLabel("ФИО Ребенка", self)
        labelFioChil.move(15, 310)

        self.lineAddFioChil = QComboBox(self)
        self.lineAddFioChil.setObjectName("ФИО Ребенка")
        self.lineAddFioChil.addItems(lChilds)
        self.lineAddFioChil.move(15, 325)
        self.lineAddFioChil.currentTextChanged.connect(self.BirandAdr)
        
        labeldataCh = QLabel("Дата рождения", self)
        labeldataCh.move(15, 360)

        self.lineEditBirthday = QDateEdit(self)
        self.lineEditBirthday.setFixedSize(300, 25)
        self.lineEditBirthday.setObjectName("Дата рождения")
        self.lineEditBirthday.move(15, 375)

        labeldataAdr = QLabel("Адрес", self)
        labeldataAdr.move(15, 410)

        self.lineAddAdr = QLineEdit(self)
        self.lineAddAdr.setObjectName("Адрес")
        self.lineAddAdr.move(15, 425)

        buttonAcept = QPushButton("Создать договор", self)
        buttonAcept.move(72, 490)

        buttonCerrar = QPushButton("Отмена", self)
        buttonCerrar.move(236, 490)

        buttonAcept.clicked.connect(self.Acept)
        buttonCerrar.clicked.connect(self.close)

    def Acept(self):
        yearP = int(self.lineAddData.date().toString("yyyy.MM.dd").split('.')[0])
        monthP = int(self.lineAddData.date().toString("yyyy.MM.dd").split('.')[1])
        dayP = int(self.lineAddData.date().toString("yyyy.MM.dd").split('.')[2])
        yearB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[0])
        monthB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[1])
        dayB = int(self.lineEditBirthday.date().toString("yyyy.MM.dd").split('.')[2])

        self.number = self.lineAddNumber.text()
        self.center = self.lineAddCenter.currentText()
        self.city = self.lineAddcity.text()
        self.dir = self.lineAdddir.text()
        self.data = date(yearP, monthP, dayP)
        self.rel = self.lineAddFioRel.currentText()
        self.chil = self.lineAddFioChil.currentText()
        self.bir = date(yearB, monthB, dayB)
        self.adr = self.lineAddAdr.text()


        context = {'number': self.number, 'city':self.city, 'data':self.data, 
        'center':self.center, 'director':self.dir, 'rel':self.rel, 'chil':self.chil,
        'bir':self.bir, 'adr':self.adr}
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('Dogovor.html')
        output_text = template.render(context)
        try:
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config)
            self.close()
        except:
            print("случилась ошибка")

    def CityAndDir(self, s):
        center = [s]
        cityanddir = "select fact_adr, director from center where nameCenter = %s"
        with connection.cursor() as cursor:
            cursor.execute(cityanddir, center)
            for result in cursor.fetchall():
                cd = result
        self.lineAddcity.setText(cd[0].split()[0])
        self.lineAdddir.setText(cd[1])


    def BirandAdr(self, s):
        child = [s]
        birandadr = "select birthday, address from children where id_child = %s"
        with connection.cursor() as cursor:
            cursor.execute(birandadr, child)
            for result in cursor.fetchall():
                cd = result
        self.lineEditBirthday.setDate(cd[0])                
        self.lineAddAdr.setText(cd[1])

     


#https://python-forum.io/thread-36741.html
