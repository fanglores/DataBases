import sys
import psycopg2 as pc2
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#click functions
def update_click():
    print('Got click!')







#create connection
db_con = pc2.connect(database='TelephonesArchive', user='postgres', password='1557', host='localhost', port=5432)
cursor = db_con.cursor()

#create application
app = QApplication(sys.argv)

#create window
window = QWidget()

#window init
window.setWindowTitle('DataBase Interface v1.0')
window.setFixedSize(PyQt5.QtCore.QSize(720, 480))

button = QPushButton(window)
button.setText('UPDATE')
button.move(100, 100)
button.clicked.connect(update_click)

window.layout()

window.show()



#start the event loop
app.exec()

#clear connection
cursor.close()
db_con.close()

