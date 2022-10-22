
import sys
sys.path.append('C:\\Users\Max\AppData\Local\Programs\Python\Python310\Lib\site-packages')

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from pyqtgraph import PlotWidget

selected_row = 2
selected_column = 2

def add_planet():
    form.tableWidget.insertRow(form.tableWidget.rowCount())
    form.tableWidget_2.insertRow(form.tableWidget_2.rowCount())
    form.tableWidget.insertColumn(form.tableWidget.columnCount())
    form.tableWidget_2.insertColumn(form.tableWidget_2.columnCount())


def delete_planet():
    if form.tableWidget.rowCount()>1:
        form.tableWidget.removeRow(form.tableWidget.rowCount()-1)
        form.tableWidget_2.removeRow(form.tableWidget_2.rowCount() - 1)
        form.tableWidget.removeColumn(form.tableWidget.columnCount() - 1)
        form.tableWidget_2.removeColumn(form.tableWidget_2.columnCount() - 1)

def draw():
    pass

def cellClick(row, col):
    selected_row = row
    selected_column = col
    print(row)

Form, Window = uic.loadUiType('D:\PythonProjects\MathMod2\interface.ui')
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(add_planet)
form.pushButton_2.clicked.connect(delete_planet)
form.pushButton_3.clicked.connect(draw)
form.tableWidget.cellClicked.connect(cellClick)
window.show()
app.exec_()