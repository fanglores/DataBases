import sys
import psycopg2 as pc2
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot

#click functions
def insert_button_click():
    try:
        s = n = p = c = h = t = None
        if (surname_textbox.text()): s = surname_textbox.text()
        if (name_textbox.text()): n = name_textbox.text()
        if (patronymic_textbox.text()): p = patronymic_textbox.text()
        if (city_textbox.text()): c = city_textbox.text()
        if (house_textbox.text()): h = house_textbox.text()
        if (telephone_textbox.text()): t = telephone_textbox.text()

        print("[DEBUG] Current query is \'INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)", (s, n, p, c, h, t))
    except:
        print("[ERROR] Error while creating insert query!\n")

    try:
        cursor.execute("INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)", (s, n, p, c, h, t))
        db_con.commit()
        print('Insertion!\n')
    except:
        print("[ERROR] Error while executing insert query!\n")

def update_button_click():
    print('Updating!\n')

def delete_button_click():
    #make msgbox
    print('Annihilation!\n')

def search_button_click(self):
    try:
        query = ""
        if (surname_textbox.text()): query += (" surname = " + surname_textbox.text() + " AND")
        if (name_textbox.text()): query += (" name = " + name_textbox.text() + " AND")
        if (patronymic_textbox.text()): query += (" patronymic = " + patronymic_textbox.text() + " AND")
        if (city_textbox.text()): query += (" city = \'" + city_textbox.text() + "\' AND")
        if (house_textbox.text()): query += (" house = \'" + house_textbox.text() + "\' AND")
        if (telephone_textbox.text()): query += (" telephone = \'" + telephone_textbox.text() + "\'")
        if (not query): query = " true"
        elif (query[-1] == 'D'): query = query[0: -3]

        print("[DEBUG] Current query is \'SELECT * FROM main WHERE" + query + "\'")
    except:
        print("[ERROR] Error while creating search query!\n")

    try:
        cursor.execute(("SELECT * FROM main WHERE" + query))
        print(cursor.fetchall())
        print('Google!\n')
    except:
        print("[ERROR] Error while executing search query!\n")

#create connection
try:
    db_con = pc2.connect(database='TelephonesArchive', user='postgres', password='1557', host='localhost', port=5432)
    cursor = db_con.cursor()
    print("[DEBUG] Loud and clear!")
except:
    print('[ERROR] Error while connecting to a database!\n')
    exit(1)

#create application
try:
    app = QApplication(sys.argv)

    #create window
    window = QWidget()

    #window init
    window.setWindowTitle('DataBase Interface v0.1')
    window.setFixedSize(PyQt5.QtCore.QSize(720, 480))

#buttons init
    #insert
    insert_button = QPushButton(window)
    insert_button.setText('INSERT')
    insert_button.setFont(QFont('Arial', 10))
    insert_button.move(160, 200)
    insert_button.clicked.connect(insert_button_click)

    #update
    update_button = QPushButton(window)
    update_button.setText('UPDATE')
    update_button.setFont(QFont('Arial', 10))
    update_button.move(260, 200)
    update_button.clicked.connect(update_button_click)

    #delete
    delete_button = QPushButton(window)
    delete_button.setText('DELETE')
    delete_button.setFont(QFont('Arial', 10))
    delete_button.move(360, 200)
    delete_button.clicked.connect(delete_button_click)

    #search
    search_button = QPushButton(window)
    search_button.setText('SEARCH')
    search_button.setFont(QFont('Arial', 10))
    search_button.move(460, 200)
    search_button.clicked.connect(search_button_click)

#textboxes init
    #surname
    surname_label = QLabel(window)
    surname_label.setFont(QFont('Arial', 12))
    surname_label.setText('Фамилия:')
    surname_label.move(40, 10)

    surname_textbox = QLineEdit(window)
    surname_textbox.setFont(QFont('Arial', 12))
    surname_textbox.move(40, 30)

    #name
    name_label = QLabel(window)
    name_label.setFont(QFont('Arial', 12))
    name_label.setText('Имя:')
    name_label.move(280, 10)

    name_textbox = QLineEdit(window)
    name_textbox.setFont(QFont('Arial', 12))
    name_textbox.move(280, 30)

    #patronymic
    patronymic_label = QLabel(window)
    patronymic_label.setFont(QFont('Arial', 12))
    patronymic_label.setText('Отчество:')
    patronymic_label.move(520, 10)

    patronymic_textbox = QLineEdit(window)
    patronymic_textbox.setFont(QFont('Arial', 12))
    patronymic_textbox.move(520, 30)

    #city
    city_label = QLabel(window)
    city_label.setFont(QFont('Arial', 12))
    city_label.setText('Город:')
    city_label.move(40, 80)

    city_textbox = QLineEdit(window)
    city_textbox.setFont(QFont('Arial', 12))
    city_textbox.move(40, 100)

    #house No
    house_label = QLabel(window)
    house_label.setFont(QFont('Arial', 12))
    house_label.setText('Номер дома:')
    house_label.move(280, 80)

    house_textbox = QLineEdit(window)
    house_textbox.setFont(QFont('Arial', 12))
    house_textbox.move(280, 100)

    #telephone No
    telephone_label = QLabel(window)
    telephone_label.setFont(QFont('Arial', 12))
    telephone_label.setText('Телефон:')
    telephone_label.move(520, 80)

    telephone_textbox = QLineEdit(window)
    telephone_textbox.setFont(QFont('Arial', 12))
    telephone_textbox.move(520, 100)

    print("[DEBUG] Safe and sound!")
except:
    print('[ERROR] Error while initializing application!\n')
    app.closeAllWindows()
    cursor.close()
    db_con.close()
    exit(1)

#start the application
try:
    window.show()
    app.exec()
except:
    print('[ERROR] Runtime error!\n')
    app.closeAllWindows()
    cursor.close()
    db_con.close()
    exit(1)

#clear all
app.closeAllWindows()
cursor.close()
db_con.close()
exit(0)
