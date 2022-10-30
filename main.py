
import sys
sys.path.append('C:\\Users\Max\AppData\Local\Programs\Python\Python310\Lib\site-packages')
import numpy as np
import pandas as pd
import solver as slv
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
    global form
    n_0, a, m, t, step, c, start, prob, j = getData()
    time, res = slv.count_common(n_0=n_0, a=a, m=m, t=t, step=step, c=c, epid=j, prolongation=start, prob=prob)
    for i in range(time.shape[0]):
        form.lineEdit_2.setText(str(np.sum(res[:, i])))
        form.lineEdit_3.setText(str(time[i]))
    slv.draw(time=time, res=res, pop_number=res.shape[0], step_count=time.shape[0])
    res_table = np.vstack((time, res))
    heading = ['Time', 'Population 1']
    for i in range(2, res.shape[0]+1):
        heading.append('Population ' + str(i))
    print(res_table)
    df = pd.DataFrame(res_table.T, columns=np.array(heading))
    df.to_csv('res.csv')


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
    epidemic_probability = float(form.lineEdit_6.text())
    epidemic_time = int(form.lineEdit_5.text())
    epidemic_coeff = float(form.lineEdit_7.text())
    population_num = int(form.lineEdit_8.text())
    print(modelling_time)
    print(step)
    print(initial_population)
    print(interaction_coeffs)
    print(interaction_matrix)
    print(epidemic_probability)
    print(epidemic_time)
    print(epidemic_coeff)
    print(population_num)
    return initial_population, interaction_coeffs, interaction_matrix, modelling_time, step, epidemic_coeff, epidemic_time, epidemic_probability, population_num


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