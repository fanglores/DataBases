import sys
import time

import psycopg2 as pc2
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot

class Window1(QWidget):
    def __init__(self):
        super(Window1, self).__init__()
        self.setWindowTitle('DataBase Interface v1.1')
        self.setFixedSize(720, 480)

#buttons init
    #insert
        self.insert_button = QPushButton(self)
        self.insert_button.setText('INSERT')
        self.insert_button.setFont(QFont('Arial', 10))
        self.insert_button.move(160, 150)
        self.insert_button.clicked.connect(self.insert_button_click)
        self.insert_button.setToolTip('Adds a new entry in DB. For insertion required surname, name, patronymic and telephone.')

    #update
        self.update_button = QPushButton(self)
        self.update_button.setText('UPDATE')
        self.update_button.setFont(QFont('Arial', 10))
        self.update_button.move(260, 150)
        self.update_button.clicked.connect(self.update_button_click)
        self.update_button.setToolTip('Edits an entry in DB.')

    #delete
        self.delete_button = QPushButton(self)
        self.delete_button.setText('DELETE')
        self.delete_button.setFont(QFont('Arial', 10))
        self.delete_button.move(360, 150)
        self.delete_button.clicked.connect(self.delete_button_click)
        self.delete_button.setToolTip('Removes an entry from DB.')

    #search
        self.search_button = QPushButton(self)
        self.search_button.setText('SEARCH')
        self.search_button.setFont(QFont('Arial', 10))
        self.search_button.move(460, 150)
        self.search_button.clicked.connect(self.search_button_click)
        self.search_button.setToolTip('Searches entries in DB by specified parameters.')

#comboboxes init
        self.surname_cbox = QComboBox(self)
        self.surname_cbox.setFont(QFont('Arial', 10))
        self.surname_cbox.setFixedSize(150, 24)
        self.surname_cbox.move(40, 54)

        self.name_cbox = QComboBox(self)
        self.name_cbox.setFont(QFont('Arial', 10))
        self.name_cbox.setFixedSize(150, 24)
        self.name_cbox.move(280, 54)

        self.patronymic_cbox = QComboBox(self)
        self.patronymic_cbox.setFont(QFont('Arial', 10))
        self.patronymic_cbox.setFixedSize(150, 24)
        self.patronymic_cbox.move(520, 54)

#textboxes init
    #surname
        self.surname_label = QLabel(self)
        self.surname_label.setFont(QFont('Arial', 12))
        self.surname_label.setText('Фамилия:')
        self.surname_label.move(40, 10)

        self.surname_textbox = QLineEdit(self)
        self.surname_textbox.setFont(QFont('Arial', 12))
        self.surname_textbox.move(40, 30)

    #name
        self.name_label = QLabel(self)
        self.name_label.setFont(QFont('Arial', 12))
        self.name_label.setText('Имя:')
        self.name_label.move(280, 10)

        self.name_textbox = QLineEdit(self)
        self.name_textbox.setFont(QFont('Arial', 12))
        self.name_textbox.move(280, 30)

    #patronymic
        self.patronymic_label = QLabel(self)
        self.patronymic_label.setFont(QFont('Arial', 12))
        self.patronymic_label.setText('Отчество:')
        self.patronymic_label.move(520, 10)

        self.patronymic_textbox = QLineEdit(self)
        self.patronymic_textbox.setFont(QFont('Arial', 12))
        self.patronymic_textbox.move(520, 30)

    #city
        self.city_label = QLabel(self)
        self.city_label.setFont(QFont('Arial', 12))
        self.city_label.setText('Город:')
        self.city_label.move(40, 80)

        self.city_textbox = QLineEdit(self)
        self.city_textbox.setFont(QFont('Arial', 12))
        self.city_textbox.move(40, 100)

    #house No
        self.house_label = QLabel(self)
        self.house_label.setFont(QFont('Arial', 12))
        self.house_label.setText('Номер дома:')
        self.house_label.move(280, 80)

        self.house_textbox = QLineEdit(self)
        self.house_textbox.setFont(QFont('Arial', 12))
        self.house_textbox.move(280, 100)

    #telephone No
        self.telephone_label = QLabel(self)
        self.telephone_label.setFont(QFont('Arial', 12))
        self.telephone_label.setText('Телефон:')
        self.telephone_label.move(520, 80)

        self.telephone_textbox = QLineEdit(self)
        self.telephone_textbox.setFont(QFont('Arial', 12))
        self.telephone_textbox.move(520, 100)

    #edit table buttons
        self.surname_edit_button = QPushButton(self)
        self.surname_edit_button.setText('...')
        self.surname_edit_button.setFont(QFont('Arial', 10))
        self.surname_edit_button.setFixedSize(26, 26)
        self.surname_edit_button.move(188, 29)
        self.surname_edit_button.clicked.connect(lambda: edit_table('s'))

        self.name_edit_button = QPushButton(self)
        self.name_edit_button.setText('...')
        self.name_edit_button.setFont(QFont('Arial', 10))
        self.name_edit_button.setFixedSize(26, 26)
        self.name_edit_button.move(428, 29)
        self.name_edit_button.clicked.connect(lambda: edit_table('n'))

        self.patronymic_edit_button = QPushButton(self)
        self.patronymic_edit_button.setText('...')
        self.patronymic_edit_button.setFont(QFont('Arial', 10))
        self.patronymic_edit_button.setFixedSize(26, 26)
        self.patronymic_edit_button.move(668, 29)
        self.patronymic_edit_button.clicked.connect(lambda: edit_table('p'))

    #output table init
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Surname', 'Name', 'Patronymic', 'City', 'House', 'Telephone'])
        self.table.setColumnWidth(0, 20)
        self.table.setColumnWidth(5, 70)
        self.table.setFixedSize(630, 240)
        self.table.move(40, 200)

        self.comboboxinit()
        self.update_table()

    def update_table(self):
        cursor.execute(
            "SELECT uid, surname_v, name_v, patronymic_v, city, house, telephone FROM main join surname_db on main.surname = surname_db.uid_s "
            + "join name_db on main.name = name_db.uid_n join patronymic_db on main.patronymic = patronymic_db.uid_p")
        ls = cursor.fetchall()

        self.table.setRowCount(len(ls))
        for i in range(len(ls)):
            self.table.setItem(i, 0, QTableWidgetItem(str(ls[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(ls[i][1]))
            self.table.setItem(i, 2, QTableWidgetItem(ls[i][2]))
            self.table.setItem(i, 3, QTableWidgetItem(ls[i][3]))
            self.table.setItem(i, 4, QTableWidgetItem(ls[i][4]))
            self.table.setItem(i, 5, QTableWidgetItem(ls[i][5]))
            self.table.setItem(i, 6, QTableWidgetItem(ls[i][6]))

    # click functions
    def insert_button_click(self):
        try:
            s = n = p = c = h = t = None
            err = ""

            if (self.surname_textbox.text()):
                s = self.surname_textbox.text()
            else:
                err += "surname "

            if (self.name_textbox.text()):
                n = self.name_textbox.text()
            else:
                err += "name "

            if (self.patronymic_textbox.text()):
                p = self.patronymic_textbox.text()
            else:
                err += "patronymic "

            if (self.city_textbox.text()): c = self.city_textbox.text()
            if (self.house_textbox.text()): h = self.house_textbox.text()

            if (self.telephone_textbox.text()):
                t = self.telephone_textbox.text()
            else:
                err += "telephone "

            if (err):
                emsgb = QMessageBox(window)
                emsgb.setIcon(QMessageBox.Critical)
                emsgb.setWindowTitle("Insertion error")
                emsgb.setText("Some parameters are not specified!")
                emsgb.setInformativeText("Not specified: " + err)
                emsgb.show()
                return None

            print(
                "[DEBUG][QUERY] \'INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)",
                (s, n, p, c, h, t))
        except:
            print("[ERROR] Error while creating insert query!\n")
            return None

        try:
            # check if name, surname, petronymic is already existing, if yes - get their id and paste it, otherwise insert in table, then get id
            s = get_id(s, 's')
            n = get_id(n, 'n')
            p = get_id(p, 'p')
            print('[DEBUG] Parsed to ', s, n, p)

            cursor.execute(
                "INSERT INTO main (surname, name, patronymic, city, house, telephone) VALUES (%s, %s, %s, %s, %s, %s)",
                (s, n, p, c, h, t))
            db_con.commit()

            self.update_table()

            print('Insertion!\n')
        except:
            print("[ERROR] Error while executing insert query!\n")
            return None

    def update_button_click(self):
        try:
            sri = self.table.selectionModel().currentIndex().row()

            if (sri == -1):
                wmsgb = QMessageBox(window)
                wmsgb.setIcon(QMessageBox.Warning)
                wmsgb.setWindowTitle("Update error")
                wmsgb.setText("Select a table row first!")
                wmsgb.show()
                return None

            query = ""

            if (self.surname_textbox.text()):
                s = get_id(self.surname_textbox.text(), 's')
                query += "surname = " + str(s) + ", "

            if (self.name_textbox.text()):
                n = get_id(self.name_textbox.text(), 'n')
                query += "name = " + str(n) + ", "

            if (self.patronymic_textbox.text()):
                p = get_id(self.patronymic_textbox.text(), 'p')
                query += "patronymic = " + str(p) + ", "

            if (self.city_textbox.text()):
                query += "city = \'" + self.city_textbox.text() + "\', "

            if (self.house_textbox.text()):
                query += "house = \'" + self.house_textbox.text() + "\', "

            if (self.telephone_textbox.text()):
                query += "telephone = \'" + self.telephone_textbox.text() + "\', "

            if (not query):
                raise "QE"
            else:
                query = query[0:-2]

            qid = self.table.item(sri, 0).text()
            # update query?????

            print("[DEBUG][QUERY] \'UPDATE main SET " + query + " WHERE uid = " + qid + "\'")
        except:
            print("[ERROR] Error while creating update query!\n")
            return None

        try:
            cursor.execute("UPDATE main SET " + query + " WHERE uid = " + qid)
            db_con.commit()

            self.update_table()

            print('Updating!\n')
        except:
            print("[ERROR] Error while executing a query!")
            return None

    def delete_button_click(self):
        try:
            sri = self.table.selectionModel().currentIndex().row()

            if (sri == -1):
                wmsgb = QMessageBox(window)
                wmsgb.setIcon(QMessageBox.Warning)
                wmsgb.setWindowTitle("Delete error")
                wmsgb.setText("Select a table row first!")
                wmsgb.show()
                return None

            wmsgb = QMessageBox(window)
            wmsgb.setIcon(QMessageBox.Warning)
            wmsgb.setWindowTitle("Delete warning")
            wmsgb.setText("You are going to delete the record! Are you sure?")
            wmsgb.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            wmsgb.setDefaultButton(QMessageBox.Cancel)

            qid = self.table.item(sri, 0).text()
            print("[DEBUG][QUERY] DELETE FROM main WHERE id = " + qid)

            if (wmsgb.exec() == QMessageBox.Cancel):
                print("[DEBUG] Delete request cancelled")
                return None
        except:
            print("[ERROR] Error while creating query!")
            return None

        try:
            cursor.execute("DELETE FROM main WHERE uid = " + qid)
            db_con.commit()

            self.update_table()

            print('Annihilation!\n')

        except:
            print("[ERROR] Error while executing query!")
            return None

    def search_button_click(self):
        try:
            query = ""
            print(self.surname_cbox.currentText())
            query += (" surname_v = \'" + self.surname_cbox.currentText() + "\' AND")
            query += (" name_v = \'" + self.name_cbox.currentText() + "\' AND")
            query += (" patronymic_v = \'" + self.patronymic_cbox.currentText() + "\' AND")
            if (self.city_textbox.text()): query += (" city = \'" + self.city_textbox.text() + "\' AND")
            if (self.house_textbox.text()): query += (" house = \'" + self.house_textbox.text() + "\' AND")
            if (self.telephone_textbox.text()): query += (" telephone = \'" + self.telephone_textbox.text() + "\'")
            if (not query):
                query = " true"
            elif (query[-1] == 'D'):
                query = query[0: -3]

            print("[DEBUG][QUERY] \'SELECT * FROM main WHERE" + query + "\'")
        except:
            print("[ERROR] Error while creating search query!\n")
            return None

        try:
            cursor.execute((
                                       "SELECT uid, surname_v, name_v, patronymic_v, city, house, telephone FROM main join surname_db on main.surname = surname_db.uid_s "
                                       + "join name_db on main.name = name_db.uid_n join patronymic_db on main.patronymic = patronymic_db.uid_p WHERE" + query))
            data_array = cursor.fetchall()
            print(data_array)
            print('Google!\n')
        except:
            print("[ERROR] Error while executing search query!\n")
            return None

        try:
            self.table.setRowCount(len(data_array))
            for i in range(len(data_array)):
                self.table.setItem(i, 0, QTableWidgetItem(str(data_array[i][0])))
                self.table.setItem(i, 1, QTableWidgetItem(data_array[i][1]))
                self.table.setItem(i, 2, QTableWidgetItem(data_array[i][2]))
                self.table.setItem(i, 3, QTableWidgetItem(data_array[i][3]))
                self.table.setItem(i, 4, QTableWidgetItem(data_array[i][4]))
                self.table.setItem(i, 5, QTableWidgetItem(data_array[i][5]))
                self.table.setItem(i, 6, QTableWidgetItem(data_array[i][6]))
            # table.resizeColumnsToContents()
        except:
            print("[ERROR] Error while updating a table!\n")
            return None

    def comboboxinit(self):
        cursor.execute("SELECT name_v FROM name_db")
        ns = cursor.fetchall()

        cursor.execute("SELECT surname_v FROM surname_db")
        ss = cursor.fetchall()

        cursor.execute("SELECT patronymic_v FROM patronymic_db")
        ps = cursor.fetchall()

        for i in range(0, len(ss)):
            self.surname_cbox.addItem(ss[i][0])

        for i in range(0, len(ns)):
            self.name_cbox.addItem(ns[i][0])

        for i in range(0, len(ps)):
            self.patronymic_cbox.addItem(ps[i][0])

class Window2(QWidget):
    def __init__(self, v):
        super(Window2, self).__init__()
        self.setWindowTitle('ParentTable EditTool v0.1')
        self.setFixedSize(480, 360)

        if (v == 's'): self.code = 'surname'
        elif (v == 'n'): self.code = 'name'
        else: self.code = 'patronymic'

#buttons init
    #insert
        self.insert_button = QPushButton(self)
        self.insert_button.setText('INSERT')
        self.insert_button.setFont(QFont('Arial', 10))
        self.insert_button.move(39, 65)
        self.insert_button.clicked.connect(self.insert_button_click)

    #update
        self.update_button = QPushButton(self)
        self.update_button.setText('UPDATE')
        self.update_button.setFont(QFont('Arial', 10))
        self.update_button.move(139, 65)
        self.update_button.clicked.connect(self.update_button_click)

    #delete
        self.delete_button = QPushButton(self)
        self.delete_button.setText('DELETE')
        self.delete_button.setFont(QFont('Arial', 10))
        self.delete_button.move(239, 65)
        self.delete_button.clicked.connect(self.delete_button_click)

#textbox init
        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 12))
        self.label.move(40, 10)

        if(self.code == 'surname'):
            self.label.setText('Фамилия:')
        elif(self.code == 'name'):
            self.label.setText('Имя:')
        else: self.label.setText('Отчетство:')

        self.textbox = QLineEdit(self)
        self.textbox.setFont(QFont('Arial', 12))
        self.textbox.move(40, 30)

    #output table init
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['ID', self.code])
        self.table.setColumnWidth(0, 30)
        self.table.setFixedSize(400, 240)
        self.table.move(40, 100)

    #init substances
        self.update_table()

    def update_table(self):
        cursor.execute("SELECT * FROM " + self.code + "_db")
        ls = cursor.fetchall()

        self.table.setRowCount(len(ls))
        for i in range(len(ls)):
            self.table.setItem(i, 0, QTableWidgetItem(str(ls[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(ls[i][1]))

    def insert_button_click(self):
        try:
            query = self.textbox.text()

            print("[DEBUG][QUERY] INSERT INTO " + self.code + "_db (" + self.code + "_v) VALUES(%s)")
        except:
            print('[ERROR] Error while creating query!')
            return None

        try:
            cursor.execute("INSERT INTO " + self.code + "_db (" + self.code + "_v) VALUES (\'" + query + "\')")
            db_con.commit()

            self.update_table()

            print('Secondary Insertion!\n')
        except:
            print('[ERROR] Error while executing query!')
            return None

    def update_button_click(self):
        try:
            sri = self.table.selectionModel().currentIndex().row()

            if (sri == -1):
                wmsgb = QMessageBox(window)
                wmsgb.setIcon(QMessageBox.Warning)
                wmsgb.setWindowTitle("Update error")
                wmsgb.setText("Select a table row first!")
                wmsgb.show()
                return None

            if (not self.textbox.text()):
                raise "QE"

            qid = self.table.item(sri, 0).text()

            print("[DEBUG][QUERY] \'UPDATE " + self.code + "_db SET " + self.code + " = \'" + self.textbox.text() + "\' WHERE uid_" + self.code[0] + " = " + qid + "\'")
        except:
            print("[ERROR] Error while creating update query!\n")
            return None

        try:
            cursor.execute("UPDATE " + self.code + "_db SET " + self.code + " = \'" + self.textbox.text() + "\' WHERE uid_" + self.code[0] + " = " + qid)
            db_con.commit()

            self.update_table()

            print('Secondary Updating!\n')
        except:
            print("[ERROR] Error while executing a query!")
            return None

    def delete_button_click(self):
        try:
            sri = self.table.selectionModel().currentIndex().row()

            if (sri == -1):
                wmsgb = QMessageBox(window)
                wmsgb.setIcon(QMessageBox.Warning)
                wmsgb.setWindowTitle("Delete error")
                wmsgb.setText("Select a table row first!")
                wmsgb.show()
                return None

            wmsgb = QMessageBox(window)
            wmsgb.setIcon(QMessageBox.Warning)
            wmsgb.setWindowTitle("Delete warning")
            wmsgb.setText("You are going to delete the record! Are you sure?")
            wmsgb.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            wmsgb.setDefaultButton(QMessageBox.Cancel)

            qid = self.table.item(sri, 0).text()
            print("[DEBUG][QUERY] DELETE FROM " + self.code + "_db WHERE uid_" + self.code[0] + " = " + qid)

            if (wmsgb.exec() == QMessageBox.Cancel):
                print("[DEBUG] Delete request cancelled")
                return None
        except:
            print("[ERROR] Error while creating query!")
            return None

        try:
            cursor.execute("DELETE FROM " + self.code + "_db WHERE uid_" + self.code[0] + " = " + qid)
            db_con.commit()

            self.update_table()

            print('Secondary Annihilation!\n')

        except:
            print("[ERROR] Error while executing query!")
            return None

    def closeEvent(self, event):
        print('Terminated')
        event.accept()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')

    def show_window_1(self):
        self.w1 = Window1()
        self.w1.show()

    def show_window_2(self, code):
        self.w2 = Window2(code)
        self.w2.show()

#sub functions
def get_id(val, tab):
    if (tab == 's'): path = 'surname_'
    elif(tab == 'n'): path = 'name_'
    else: path = 'patronymic_'

    print("[DEBUG][QUERY] SELECT * FROM " + path + "db WHERE " + path + "v = \'" + val + "\'")
    cursor.execute("SELECT * FROM " + path + "db WHERE " + path + "v = \'" + val + "\'")
    ls = cursor.fetchall()

    if(len(ls) > 0):
        return ls[0][0]
    else:
        wmsgb = QMessageBox(window)
        wmsgb.setIcon(QMessageBox.Warning)
        wmsgb.setWindowTitle("Insert error")
        wmsgb.setText("No such " + path[0:-1] + " in database! Try to insert it manually first.")
        wmsgb.exec()

        raise "Parse error"
        return None

#edit table func
def edit_table(val):
    print(val)
    try:
        window.show_window_2(val)

    except:
        print("[ERROR] Error while creating secondary window")

#create connection
try:
    db_con = pc2.connect(database='TelephonesArchive', user='postgres', password='1557', host='localhost', port=5432)
    cursor = db_con.cursor()
    print("[DEBUG] Loud and clear!")
except:
    print('[ERROR] Error while connecting to a database!\n')
    exit(1)

#start the application
try:
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show_window_1()
    app.exec()

    print('[DEBUG] Safe and sound!')
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
