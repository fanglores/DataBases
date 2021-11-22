import sys
import time

import psycopg2 as pc2
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot

#sub functions
def get_id(val, tab):
    if (tab == 's'): path = 'surname_'
    elif(tab == 'n'): path = 'name_'
    else: path = 'patronymic_'

    print("[DEBUG][QUERY] SELECT * FROM " + path + "db WHERE " + path + "v = \'" + val + "\'")
    cursor.execute("SELECT * FROM " + path + "db WHERE " + path + "v = \'" + val + "\'")
    ls = cursor.fetchall()

    if(len(ls) != 0):
        return ls[0][0]
    else:
        print("[DEBUG][QUERY] INSERT INTO " + path + "db (" + path + "v) VALUES (\'" + val + "\')")
        cursor.execute("INSERT INTO " + path + "db (" + path + "v) VALUES (\'" + val + "\')")
        db_con.commit()
        time.sleep(1)

        cursor.execute("SELECT * FROM " + path + "db WHERE " + path + "v = \'" + val + "\'")
        ls = cursor.fetchall()
        return ls[0][0]

#click functions
def insert_button_click():
    try:
        s = n = p = c = h = t = None
        err = ""

        if (surname_textbox.text()): s = surname_textbox.text()
        else: err += "surname "

        if (name_textbox.text()): n = name_textbox.text()
        else: err += "name "

        if (patronymic_textbox.text()): p = patronymic_textbox.text()
        else: err += "patronymic "

        if (city_textbox.text()): c = city_textbox.text()
        if (house_textbox.text()): h = house_textbox.text()

        if (telephone_textbox.text()): t = telephone_textbox.text()
        else: err += "telephone "

        if(err):
            emsgb = QMessageBox(window)
            emsgb.setIcon(QMessageBox.Critical)
            emsgb.setWindowTitle("Insertion error")
            emsgb.setText("Some parameters are not specified!")
            emsgb.setInformativeText("Not specified: " + err)
            emsgb.show()
            return None

        print("[DEBUG][QUERY] \'INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)", (s, n, p, c, h, t))
    except:
        print("[ERROR] Error while creating insert query!\n")
        return None

    try:
        #check if name, surname, petronymic is already existing, if yes - get their id and paste it, otherwise insert in table, then get id
        s = get_id(s, 's')
        n = get_id(n, 'n')
        p = get_id(p, 'p')
        print('[DEBUG] Parsed to ', s, n, p)

        cursor.execute("INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)", (s, n, p, c, h, t))
        db_con.commit()
        print('Insertion!\n')
    except:
        print("[ERROR] Error while executing insert query!\n")
        return None

def update_button_click():

    try:
        sri = table.selectionModel().currentIndex().row()

        if(sri == -1):
            wmsgb = QMessageBox(window)
            wmsgb.setIcon(QMessageBox.Warning)
            wmsgb.setWindowTitle("Update error")
            wmsgb.setText("Select a table row first!")
            #wmsgb.setInformativeText("Not specified:")
            wmsgb.show()
            return None

        print("[DEBUG][QUERY]")
    except:
        print("[ERROR] Error while creating a query!")
        return None

    try:
        #execute a query
        print("UPDATE main SET surname = %s, name = %s WHERE uid = sri[0]")

        print('Updating!\n')
    except:
        print("[ERROR] Error while executing a query!")
        return None

def delete_button_click():
    #make msgbox
    try:
###warning! It will be insert into parent table if no such surname, name or patronymic were found
        query = ""
        if (surname_textbox.text()): query += (" surname = " + str(get_id(surname_textbox.text(), 's')) + " AND")
        if (name_textbox.text()): query += (" name = " + str(get_id(name_textbox.text(), 'n')) + " AND")
        if (patronymic_textbox.text()): query += (" patronymic = " + str(get_id(patronymic_textbox.text(), 'p')) + " AND")
        if (city_textbox.text()): query += (" city = \'" + city_textbox.text() + "\' AND")
        if (house_textbox.text()): query += (" house = \'" + house_textbox.text() + "\' AND")
        if (telephone_textbox.text()): query += (" telephone = \'" + telephone_textbox.text() + "\'")
        if (not query):
            query = " true"
        elif (query[-1] == 'D'):
            query = query[0: -3]

        wmsgb = QMessageBox(window)
        wmsgb.setIcon(QMessageBox.Warning)
        wmsgb.setWindowTitle("Delete warning")
        wmsgb.setText("You are going to delete some records!")
        wmsgb.setInformativeText("You are going to execute following query: DELETE FROM main WHERE" + query)
        wmsgb.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        wmsgb.setDefaultButton(QMessageBox.Cancel)

        print("[DEBUG][QUERY] DELETE FROM main WHERE" + query)

        if(wmsgb.exec() == QMessageBox.Cancel):
            print("[DEBUG] Delete request cancelled")
            return None
    except:
        print("[ERROR] Error while creating query!")
        return None

    try:
        cursor.execute("DELETE FROM main WHERE" + query)
        db_con.commit()

        print('Annihilation!\n')
    except:
        print("[ERROR] Error while executing query!")
        return None

def search_button_click():
    try:
        query = ""
        if (surname_textbox.text()): query += (" surname_v = \'" + surname_textbox.text() + "\' AND")
        if (name_textbox.text()): query += (" name_v = \'" + name_textbox.text() + "\' AND")
        if (patronymic_textbox.text()): query += (" patronymic_v = \'" + patronymic_textbox.text() + "\' AND")
        if (city_textbox.text()): query += (" city = \'" + city_textbox.text() + "\' AND")
        if (house_textbox.text()): query += (" house = \'" + house_textbox.text() + "\' AND")
        if (telephone_textbox.text()): query += (" telephone = \'" + telephone_textbox.text() + "\'")
        if (not query): query = " true"
        elif (query[-1] == 'D'): query = query[0: -3]

        print("[DEBUG][QUERY] \'SELECT * FROM main WHERE" + query + "\'")
    except:
        print("[ERROR] Error while creating search query!\n")
        return None

    try:
        cursor.execute(("SELECT uid, surname_v, name_v, patronymic_v, city, house, telephone FROM main join surname_db on main.surname = surname_db.uid_s "
                        + "join name_db on main.name = name_db.uid_n join patronymic_db on main.patronymic = patronymic_db.uid_p WHERE" + query))
        data_array = cursor.fetchall()
        print(data_array)
        print('Google!\n')
    except:
        print("[ERROR] Error while executing search query!\n")
        return None

    try:
        table.setRowCount(len(data_array))
        for i in range (len(data_array)):
            table.setItem(i, 0, QTableWidgetItem(str(data_array[i][0])))
            table.setItem(i, 1, QTableWidgetItem(data_array[i][1]))
            table.setItem(i, 2, QTableWidgetItem(data_array[i][2]))
            table.setItem(i, 3, QTableWidgetItem(data_array[i][3]))
            table.setItem(i, 4, QTableWidgetItem(data_array[i][4]))
            table.setItem(i, 5, QTableWidgetItem(data_array[i][5]))
            table.setItem(i, 6, QTableWidgetItem(data_array[i][6]))
        #table.resizeColumnsToContents()
    except:
        print("[ERROR] Error while updating a table!\n")
        return None

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
    window.setWindowTitle('DataBase Interface v0.3')
    window.setFixedSize(PyQt5.QtCore.QSize(720, 480))

#buttons init
    #insert
    insert_button = QPushButton(window)
    insert_button.setText('INSERT')
    insert_button.setFont(QFont('Arial', 10))
    insert_button.move(160, 150)
    insert_button.clicked.connect(insert_button_click)
    insert_button.setToolTip('Adds a new entry in DB. For insertion required surname, name, patronymic and telephone.')

    #update
    update_button = QPushButton(window)
    update_button.setText('UPDATE')
    update_button.setFont(QFont('Arial', 10))
    update_button.move(260, 150)
    update_button.clicked.connect(update_button_click)
    update_button.setToolTip('Edits an entry in DB.')

    #delete
    delete_button = QPushButton(window)
    delete_button.setText('DELETE')
    delete_button.setFont(QFont('Arial', 10))
    delete_button.move(360, 150)
    delete_button.clicked.connect(delete_button_click)
    delete_button.setToolTip('Removes an entry from DB.')

    #search
    search_button = QPushButton(window)
    search_button.setText('SEARCH')
    search_button.setFont(QFont('Arial', 10))
    search_button.move(460, 150)
    search_button.clicked.connect(search_button_click)
    search_button.setToolTip('Searches entries in DB by specified parameters.')

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

    #info
    info_label = QLabel(window)
    info_label.setStyleSheet("background-color: white; border-top: 1px solid black")
    info_label.setFont(QFont('Arial', 12))
    info_label.setText('\t\tThis is an info label!\tYou will see important information here!')
    info_label.setFixedSize(720, 20)
    info_label.move(0, 460)

#output table init
    table = QTableWidget(window)
    table.setColumnCount(7)
    table.setHorizontalHeaderLabels(['ID', 'Surname', 'Name', 'Patronymic', 'City', 'House', 'Telephone'])
    table.setColumnWidth(0, 20)
    table.setColumnWidth(5, 70)
    table.setFixedSize(630,240)
    table.move(40, 200)

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
