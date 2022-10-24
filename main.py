
import sys
sys.path.append('C:\\Users\Max\AppData\Local\Programs\Python\Python310\Lib\site-packages')
import numpy as np

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from pyqtgraph import PlotWidget



def add_planet():
    form.tableWidget.insertRow(form.tableWidget.rowCount())
    form.tableWidget_2.insertRow(form.tableWidget_2.rowCount())
    form.tableWidget.insertColumn(form.tableWidget.columnCount())
    form.tableWidget_2.insertColumn(form.tableWidget_2.columnCount())


def delete_planet():
    if form.tableWidget.rowCount()>2:
        form.tableWidget.removeRow(form.tableWidget.rowCount()-1)
        form.tableWidget_2.removeRow(form.tableWidget_2.rowCount() - 1)
        form.tableWidget.removeColumn(form.tableWidget.columnCount() - 1)
        form.tableWidget_2.removeColumn(form.tableWidget_2.columnCount() - 1)

def draw():
    getData()

def getPopulation():
    initial_population = np.empty((form.tableWidget.rowCount()))
    for i in range(form.tableWidget.rowCount()):
        initial_population[i] = int(form.tableWidget.item(i, 0).text())
    return initial_population


def getInteractionCoeffs():
    interaction_coeffs = np.empty((form.tableWidget.rowCount()))
    for i in range(form.tableWidget.rowCount()):
        interaction_coeffs[i] = float(form.tableWidget.item(i, 1).text())
    return interaction_coeffs

def getInteractionMatrix():
    interaction_matrix = np.empty((form.tableWidget_2.rowCount(), form.tableWidget_2.columnCount()))
    for i in range(form.tableWidget_2.rowCount()):
        for j in range(form.tableWidget_2.columnCount()):
            interaction_matrix[i, j] = float(form.tableWidget_2.item(i, j).text())
    return interaction_matrix

def getData():
    modelling_time = int(form.lineEdit_4.text())
    step = float(form.lineEdit.text())
    initial_population = getPopulation()
    interaction_coeffs = getInteractionCoeffs()
    interaction_matrix = getInteractionMatrix()

    print(modelling_time)
    print(step)
    print(initial_population)
    print(interaction_coeffs)
    print(interaction_matrix)

Form, Window = uic.loadUiType('interface.ui')
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(add_planet)
form.pushButton_2.clicked.connect(delete_planet)
form.pushButton_3.clicked.connect(draw)
window.show()
app.exec_()