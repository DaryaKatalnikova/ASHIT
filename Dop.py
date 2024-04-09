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
        select_groups = "SELECT * FROM groupn"
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
        for g in groups:
            lGroups.append(str(g).split(',')[1][2:len(str(g).split(',')[1]) - 1])
        disp = ["Кибергигиена", "Основы программирования. Python", "Системное администрирование", "VR/AR", "Мобильная разработка", "Компьютерная графика"]



       



