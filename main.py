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
    def on_pushsave_clicked(self):
        print("min a ={} - min b = {}".format(self.doubleSpinBox.value(),self.doubleSpinBox_2.value()))
        print("max a ={} - max b = {}".format(self.doubleSpinBox_3.value(), self.doubleSpinBox_4.value()))
        if ( self.doublemina.value()>self.doubleSpinBox.value()):
            self.doublemina.setValue(self.doubleSpinBox.value())
        if (self.doublemaxa.value() < self.doubleSpinBox_2.value()):
            self.doublemaxa.setValue(self.doubleSpinBox_2.value())
        if (self.doubleminb.value() > self.doubleSpinBox.value()):
            self.doubleminb.setValue(self.doubleSpinBox_3.value())
        if (self.doublemaxb.value() < self.doubleSpinBox_4.value()):
            self.doublemaxb.setValue(self.doubleSpinBox_4.value())

        pass

    @QtCore.pyqtSlot()
    def on_pushclear_clicked(self):
        self.doublemina.setValue(0.00)
        self.doublemaxa.setValue(0.00)
        self.doubleminb.setValue(0.00)
        self.doublemaxb.setValue(0.00)

    @QtCore.pyqtSlot()
    def on_pushload_clicked(self):
        diap = [[self.doublemina.value(), self.doublemaxa.value()],
                [self.doubleminb.value(), self.doublemaxb.value()]]
        gui.Mask(diap)


    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        gui.saveMask(gui.immask)

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


            gui.Open()

            timer = QTimer(self)
            timer.timeout.connect(self.obnow)
            timer.start()

    @QtCore.pyqtSlot()
    def on_pushsavepoint_clicked(self):
        pass


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

        elif (gui.mina != self.doubleSpinBox.value() or
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











if __name__ == '__main__':
    gui = GUI()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))  # Более современная тема оформления
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Берём цвета из темы оформления
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
