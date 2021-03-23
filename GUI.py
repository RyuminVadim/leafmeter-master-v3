from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import os
import matplotlib.pyplot as plt
from skimage import io, color
from PIL import Image



class GUI():
    def __init__(self):
        super().__init__()

        #app1.aboutToQuit.connect(self.closeEvent)  # вызывается при закрытии окна
        #self.w = pg.GraphicsLayoutWidget(size=(800, 800), border=True)
        self.w = pg.GraphicsLayoutWidget(size=(800, 800), border=True)
        self.values()

    def values(self):
        #self.rois = [[0], [0]]
        self.x , self.y ,self.width ,self.height = 0, 0, 0, 0
        self._L, self._a, self._b = 0, 1, 2
        self.mina, self.maxa, self.minb, self.maxb = 0,0,0,0
        self.pros= 0
        self.lastRoi = None
        self.file = "7"
        self.teg = True




    def Open(self):
        self.CreateImage()
        self.TopRight()
        self.BottomPlot()
        self._L, self._a, self._b = 0, 1, 2
        rois = []
        rois.append(pg.TestROI([0, 0], [20, 20], maxBounds=QtCore.QRectF(-20, -20, self.width+40, self.height+40), pen=(0, 9)))
        #rois.append(pg.TestROI([0, 0], [20, 20], maxBounds=QtCore.QRectF(0, 0, 200, 200), pen=(0, 9)))
        listarray = []
        for r in rois:
            self.v.addItem(r)
            c = self.pi1.plot(x=[1, 2, 3], y=[1, 4, 9], pen=(0, 0, 0), symbol='o', symbolSize=5)
            r.curve = c
            r.sigRegionChanged.connect(self.updateRoi)

        self.w.show()


    def CreateImage(self):
        Q = 100
        im = Image.open(self.file + ".jpg")
        (self.width, self.height) = im.size
        self.width = self.width * 1.1
        self.height = self.height *1.1
        #print(" width = {}\n height = {}".format(self.width,self.height))
        self.rgb = plt.imread(self.file + '.jpg')
        self.lab = np.load(self.file + '.npz')['arr_0']
        #arr = self.lab[:, :, 0]
        # This is the main graphics widget
        # Top-left scene in the graphics widget
        self.v = self.w.addViewBox(0, 0)
        self.v.invertY(True)  ## Images usually have their Y-axis pointing downward
        self.v.setAspectLocked(True)
        self.im1 = pg.ImageItem()  # Create image widget, add to scene and set position
        self.im1.setImage(self.rgb)
        self.v.addItem(self.im1)
        self.v.setRange(QtCore.QRectF(0, 0, 200, 120))

    def TopRight(self):
        v2 = self.w.addViewBox(0, 1)
        self.im3 = pg.ImageItem()
        v2.addItem(self.im3)
        v2.setRange(QtCore.QRectF(0, 0, 60, 60))
        v2.invertY(True)
        v2.setAspectLocked(True)
        self.im3.setZValue(10)

    def BottomPlot(self):
        self.pi1 = self.w.addPlot(1, 0, colspan=2)
        self.pi1.setXRange(-100, 100, padding=0)
        self.pi1.setYRange(-100, 100, padding=0)
        self.pi1.showGrid(x=True, y=True, alpha=0.3)

    def updateRoi(self,roi):
        #global im1, im3, arr  # , lastRoi
        if roi is None:
            return
        # print(roi.pos(), roi.size(), roi.getAffineSliceParams(im1.image, im1))
        self.x, self.y = roi.pos() + roi.size() / 2
        self.pos = roi.pos()
        x, y = roi.pos() + roi.size() / 2
        #print(x)
        #print(y)
        a = roi.getArrayRegion(self.lab[:, :, 1], img=self.im1)
        b = roi.getArrayRegion(self.lab[:, :, 2], img=self.im1)

        self.updateRoiPlot(roi, a, b)
        self.Mask()

    def Mask(self,diap=""):
        if(diap == ""):
            self.mask = (self.lab[:, :, self._a] > self.mina) & (self.lab[:, :, self._a] < self.maxa) & \
                   (self.lab[:, :, self._b] > self.minb) & (self.lab[:, :, self._b] < self.maxb)
        else:
            self.mask = (self.lab[:, :, self._a] > min(diap[0])) & (self.lab[:, :, self._a] < max(diap[0])) & \
                   (self.lab[:, :, self._b] > min(diap[1])) & (self.lab[:, :, self._b] < max(diap[1]))
        rgbm = self.rgb.copy()
        rgbm[~self.mask] = [0, 30, 30]
        self.im3.setImage(rgbm)
        self.immask = rgbm
        self.percent(rgbm)

    def percent(self, rgbm):
        x= [0,30,30]
        selected,full = 0, 0

        for ry in rgbm:
            for rx in ry:
                if(not np.array_equal(rx, x)):
                    selected+=1
                full+=1
        self.pros=(selected/full)*100
        #print("Full = {}, selected = {}, % = {}".format(full,selected,self.pros))
        pass

    def saveMask(self,rgbm):
        x = [0, 30, 30]


        for ry in rgbm:
            for rx in ry:
                if (not np.array_equal(rx, x)):
                    rx=[0,0,0]
                else:
                    rx = [0, 255, 255]

        rgbm[~self.mask] = [0, 0, 0]
        rgbm[self.mask] = [255, 255, 255]
        im = Image.fromarray(rgbm)
        im.save(self.file + "_mask.jpg")

        #self.im3.setImage(rgbm)





    def updateRoiPlot(self,roi, a=None, b=None):
        if a is None:
            a = roi.getArrayRegion(self.lab[:, :, 1], img=self.im1)
            b = roi.getArrayRegion(self.lab[:, :, 2], img=self.im1)
        if a is not None:
            #self.rois=[a.flatten(),b.flatten()]
            self.mina,self.maxa,self.minb,self.maxb = min(a.flatten()),max(a.flatten()),min(b.flatten()),max(b.flatten())
            self.teg=True

            roi.curve.setData({'x': a.flatten(), 'y': b.flatten()})  # data.mean(axis=1))



if __name__ == '__main__':
    import sys


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()