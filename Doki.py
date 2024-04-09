import sys, jinja2, pdfkit, connect_db
import Dogovor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QVBoxLayout,
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

class Doki(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кибертрон/Директор")

        self.setFixedSize(500, 230)
        self.initUI()

    def initUI(self):

        buttonDog = QPushButton("Договора", self)
        buttonDog.setFixedSize(430, 30)
        buttonDog.move(30, 50)
        
     

        buttonOtch = QPushButton("Отчет о должниках", self)
        buttonOtch.setFixedSize(430, 30)
        buttonOtch.move(30, 100)
    

        buttonExit = QPushButton("Назад", self)
        buttonExit.setFixedSize(430, 30)
        buttonExit.move(30, 165)
    
        buttonDog.clicked.connect(self.Dogovor)

        buttonOtch.clicked.connect(self.Otch)
        buttonExit.clicked.connect(self.close)
    

    def Dogovor(self):
        self.w = Dogovor.Dogovor()
        self.w.show()


    def Otch(self):
        connection = connect_db.create_connection("localhost", "root", "HarryPotterand3", "kibertrone")

        select_dolg = """Select Children.fio_child, relation.fio_rel From children 
        Inner join relation on relation.id_rel = children.id_rel left join kvit
        on children.id_child = kvit.id_child where kvit.id_child is null"""
        dolgs = execute_read_query(connection, select_dolg)
        lDolg = list()
        for i in dolgs:
            lDolg.append(i[0] + " " + i[1])

        context = {'context': lDolg}
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template('dolgnikiOtch.html')
        output_text = template.render(context)
        try:
            config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
            pdfkit.from_string(output_text, 'Dolgniki.pdf', configuration=config)
        except:
            print("случилась ошибка")

