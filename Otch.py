import sys
import connect_db, jinja2, pdfkit
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (    
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableView,
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


class Otch(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("отчет")
        self.initUI()

    def initUI(self):
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
            self.close()
        except:
            print("случилась ошибка")



      

       



