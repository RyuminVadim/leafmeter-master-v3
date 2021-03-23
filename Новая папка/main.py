from PyQt5 import QtWidgets, QtCore, uic
from skimage import io, color
#import gpu
import matplotlib.pyplot as plt
import sys
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import os
import pyqtgraph as pg
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from GUITest import GUI
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt


class ExampleApp(QtWidgets.QMainWindow):
    # Основное поведение класса наследуется из Qt, а виджеты - из design.py
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        pg.setConfigOption('background', 'w')  # default background is black, making it white
        pg.setConfigOption('foreground', 'k')
        self.lastpoint = [0.00,0.00,0.00,0.00]



        #self.setupUi(self)  # Этот метод из design.py, он инициализирует виджеты
        #self.graphicsView(labels={'left': 'Voltage', 'bottom': 'Horisont'})

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        gui.saveMask(gui.immask)
        #print("%")
       # print(gui.immask)
        #gui.percent(gui.immask)
        pass

    @QtCore.pyqtSlot()
    def on_pushOpen_clicked(self):

        filename, filetype = QFileDialog.getOpenFileName(self,"Выбрать файл",".","JPG Files(*.jpg);;\
                                                         NPZ Files(*.npz);;All Files(*)")
        if (filename !=""):
            file = "Выбрали файл: {}".format(filename)
            self.label.setText("Выбрали файл: {}".format(filename, filetype))
            #
            self.creareNPZ(filename)
            gui.file= filename[:-4]
            #self.doubleSpinBox_6.setMaximum(gui.height)
            #self.doubleSpinBox_5.setMaximum(gui.width)

            gui.Open()

            timer = QTimer(self)
            timer.timeout.connect(self.obnow)
            timer.start()


    @QtCore.pyqtSlot()
    def on_pushpoint_clicked(self):
        diap = [[ self.doubleSpinBox.value(),self.doubleSpinBox_2.value()],[self.doubleSpinBox_3.value(),self.doubleSpinBox_4.value()]]
        gui.Mask(diap)
        #print("min a ={} - min b = {}".format(min(diap[0]),min(diap[1])))
        #print("max a ={} - max b = {}".format(max(diap[0]), max(diap[1])))
        #print(gui.immask[50])
        '''сохранить маску в файл'''
        pass


       #self.GPU()

    def creareNPZ(self,adres):
        name = adres[:-4]
        rgb = plt.imread(name + '.jpg')
        lab = color.rgb2lab(rgb).astype(np.int8)
        np.savez_compressed(name + '.npz', lab)

    def obnow(self):
        if (gui.mina !=self.doubleSpinBox.value() or
            gui.maxa != self.doubleSpinBox_2.value() or
            gui.minb != self.doubleSpinBox_3.value() or
            gui.maxb != self.doubleSpinBox_4.value()):
            diap = [[self.doubleSpinBox.value(), self.doubleSpinBox_2.value()],
                    [self.doubleSpinBox_3.value(), self.doubleSpinBox_4.value()]]
            gui.Mask(diap)
            self.doubleSpinBox_7.setValue(gui.pros)
            self.doubleSpinBox_8.setValue(100 - gui.pros)
            gui.mina = self.doubleSpinBox.value()
            gui.maxa = self.doubleSpinBox_2.value()
            gui.minb = self.doubleSpinBox_3.value()
            gui.maxb = self.doubleSpinBox_4.value()


        if(gui.teg):
            gui.teg=False

            self.doubleSpinBox.setValue(gui.mina)
            self.doubleSpinBox_2.setValue(gui.maxa)
            self.doubleSpinBox_3.setValue(gui.minb)
            self.doubleSpinBox_4.setValue(gui.maxb)
            self.doubleSpinBox_5.setValue(gui.x)
            self.doubleSpinBox_6.setValue(gui.y)
            self.doubleSpinBox_7.setValue(gui.pros)
            self.doubleSpinBox_8.setValue(100-gui.pros)


            '''
            self.lastpoint[0] =self.doubleSpinBox.value()
            self.lastpoint[1] = self.doubleSpinBox_2.value()
            self.lastpoint[2] = self.doubleSpinBox_3.value()
            self.lastpoint[3] = self.doubleSpinBox_4.value()
            '''











if __name__ == '__main__':
    gui = GUI()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))  # Более современная тема оформления
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Берём цвета из темы оформления
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
