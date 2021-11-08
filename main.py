import sys
import psycopg2 as pc2
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#click functions
def insert_button_click():
    print('Insertion!')

def update_button_click():
    print('Updating!')

def delete_button_click():
    print('Annihilation!')

def search_button_click(self):
    print('Google!')




#create connection
try:
    db_con = pc2.connect(database='TelephonesArchive', user='postgres', password='1557', host='localhost', port=5432)
    cursor = db_con.cursor()
except:
    print('Error while connecting to a database')
    exit(1)

#create application
try:
    app = QApplication(sys.argv)

    #create window
    window = QWidget()

    #window init
    window.setWindowTitle('DataBase Interface v1.0')
    window.setFixedSize(PyQt5.QtCore.QSize(720, 480))

    insert_button = QPushButton(window)
    insert_button.setText('INSERT')
    insert_button.move(160, 200)
    insert_button.clicked.connect(insert_button_click)

    update_button = QPushButton(window)
    update_button.setText('UPDATE')
    update_button.move(260, 200)
    update_button.clicked.connect(update_button_click)

    delete_button = QPushButton(window)
    delete_button.setText('DELETE')
    delete_button.move(360, 200)
    delete_button.clicked.connect(delete_button_click)

    search_button = QPushButton(window)
    search_button.setText('SEARCH')
    search_button.move(460, 200)
    search_button.clicked.connect(search_button_click)
except:
    print('Error while initializing application')
    app.closeAllWindows()
    cursor.close()
    db_con.close()
    exit(1)

#start the application
try:
    window.show()
    app.exec()
except:
    print('Runtime error')
    app.closeAllWindows()
    cursor.close()
    db_con.close()
    exit(1)

#clear all
app.closeAllWindows()
cursor.close()
db_con.close()
exit(0)
