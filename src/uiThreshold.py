# -*- coding: utf-8 -*-
"""
================================================================================
Name:        uiThreshold
Purpose:     (CZE-ZCU-FAV-KKY) Liver medical project

Author:      Pavel Volkovinsky (volkovinsky.pavel@gmail.com)

Created:     08.11.2012
Copyright:   (c) Pavel Volkovinsky 2012
Licence:     <your licence>
================================================================================
"""

import sys
sys.path.append("../src/")
sys.path.append("../extern/")

import logging
logger = logging.getLogger(__name__)

import numpy
#import scipy.misc
#import scipy.io
import scipy.ndimage

#import unittest
#import argparse

import matplotlib.pyplot as matpyplot
import matplotlib
from matplotlib.widgets import Slider#, Button, RadioButtons

"""
================================================================================
uiThreshold
================================================================================
"""
class uiThreshold:

    def __init__(self, imgUsed, initslice = 0, cmap = matplotlib.cm.Greys_r):

        inputDimension = numpy.ndim(imgUsed)
        print('Dimenze vstupu: ',  inputDimension)
        self.cmap = cmap
        
        if(inputDimension == 2):
            
            self.imgUsed = imgUsed
            self.imgChanged = imgUsed
                
            """
            self.imgChanged1 = self.imgUsed
            self.imgChanged2 = self.imgUsed
            self.imgChanged3 = self.imgUsed
            """
            
            # Zakladni informace o obrazku (+ statisticke)
            """
            print('Image dtype: ', imgUsed.dtype)
            print('Image size: ', imgUsed.size)
            print('Image shape: ', imgUsed.shape[0], ' x ',  imgUsed.shape[1])
            print('Max value: ', imgUsed.max(), ' at pixel ',  imgUsed.argmax())
            print('Min value: ', imgUsed.min(), ' at pixel ',  imgUsed.argmin())
            print('Variance: ', imgUsed.var())
            print('Standard deviation: ', imgUsed.std())
            """
            
            # Ziskani okna (figure)
            self.fig = matpyplot.figure()
            # Pridani subplotu do okna (do figure)
            self.ax1 = self.fig.add_subplot(111)
            """
    #        self.ax0 = self.fig.add_subplot(232)
            self.ax1 = self.fig.add_subplot(131)
            self.ax2 = self.fig.add_subplot(132)
            self.ax3 = self.fig.add_subplot(133)
            """
            # Upraveni subplotu
            self.fig.subplots_adjust(left = 0.1, bottom = 0.25)
            # Vykresli obrazek
    #        self.im0 = self.ax0.imshow(imgUsed)
            self.im1 = self.ax1.imshow(self.imgChanged, self.cmap)
            """
            self.im2 = self.ax2.imshow(imgUsed)
            self.im3 = self.ax3.imshow(imgUsed)
            """
     #       self.fig.colorbar(self.im1)
    
            # Zakladni informace o slideru
            axcolor = 'white' # lightgoldenrodyellow
            axmin = self.fig.add_axes([0.25, 0.16, 0.495, 0.03], axisbg = axcolor)
            axmax  = self.fig.add_axes([0.25, 0.12, 0.495, 0.03], axisbg = axcolor)
            """
            axopening = self.fig.add_axes([0.25, 0.08, 0.495, 0.03], axisbg = axcolor)
            axclosing = self.fig.add_axes([0.25, 0.04, 0.495, 0.03], axisbg = axcolor)
            """
            
            # Vytvoreni slideru
                # Minimalni pouzita hodnota v obrazku
            min0 = imgUsed.min()
                # Maximalni pouzita hodnota v obrazku
            max0 = imgUsed.max()
                # Vlastni vytvoreni slideru
            self.smin = Slider(axmin, 'Minimal threshold', min0, max0, valinit = min0)
            self.smax = Slider(axmax, 'Maximal threshold', min0, max0, valinit = max0)
            """
            self.sopen = Slider(axopening, 'Binary opening', 0, 10, valinit = 0)
            self.sclose = Slider(axclosing, 'Binary closing', 0, 10, valinit = 0)
            """
            
            # Udalost pri zmene hodnot slideru - volani updatu
            self.smin.on_changed(self.updateImg2D)
            self.smax.on_changed(self.updateImg2D)
        
        elif(inputDimension == 3):
            
            # Zakladni informace o obrazcich (+ statisticke)
            """
            print('Image dtype: ', imgUsed.dtype)
            print('Image size: ', imgUsed.size)
            print('Image shape: ', imgUsed.shape[0], ' x ',  imgUsed.shape[1], ' x ',  imgUsed.shape[2])
            print('Max value: ', imgUsed.max(), ' at pixel ',  imgUsed.argmax())
            print('Min value: ', imgUsed.min(), ' at pixel ',  imgUsed.argmin())
            print('Variance: ', imgUsed.var())
            print('Standard deviation: ', imgUsed.std())
            """
            
            self.imgUsed = imgUsed
            self.imgChanged = self.imgUsed
            
            #self.imgMin = numpy.min(self.imgUsed)
            #self.imgMax = numpy.max(self.imgUsed)
            
            self.imgShape = list(self.imgUsed.shape)
            
            self.fig = matpyplot.figure()
            # Pridani subplotu do okna (do figure)
            self.ax1 = self.fig.add_subplot(131)
            self.ax2 = self.fig.add_subplot(132)
            self.ax3 = self.fig.add_subplot(133)
            
            # Upraveni subplotu
            self.fig.subplots_adjust(left = 0.1, bottom = 0.4)
            
            # Nalezeni a pripraveni obrazku k vykresleni
     #       imgShowPlace = numpy.round(self.imgShape[2] / 2).astype(int)
     #       self.imgShow = self.imgUsed[:, :, imgShowPlace]
            self.imgShow = numpy.amax(self.imgUsed, 2)
            
            # Vykreslit obrazek
            self.im1 = self.ax1.imshow(self.imgShow, self.cmap)
            self.im2 = self.ax2.imshow(self.imgShow, self.cmap)
            self.im3 = self.ax3.imshow(self.imgShow, self.cmap)
    
            # Zakladni informace o slideru
            axcolor = 'white' # lightgoldenrodyellow
            axmin = self.fig.add_axes([0.20, 0.24, 0.55, 0.03], axisbg = axcolor)
            axmax  = self.fig.add_axes([0.20, 0.20, 0.55, 0.03], axisbg = axcolor)
            axopening2 = self.fig.add_axes([0.30, 0.16, 0.40, 0.03], axisbg = axcolor)
            axclosing2 = self.fig.add_axes([0.30, 0.12, 0.40, 0.03], axisbg = axcolor)
            axopening3 = self.fig.add_axes([0.30, 0.04, 0.40, 0.03], axisbg = axcolor)
            axclosing3 = self.fig.add_axes([0.30, 0.08, 0.40, 0.03], axisbg = axcolor)
            
            # Vytvoreni slideru
                # Minimalni pouzita hodnota v obrazku
            min0 = numpy.amin(self.imgUsed)
                # Maximalni pouzita hodnota v obrazku
            max0 = numpy.amax(self.imgUsed)
                # Vlastni vytvoreni slideru
                
            self.smin = Slider(axmin, 'Minimal threshold', min0, max0, valinit = min0)
            self.smax = Slider(axmax, 'Maximal threshold', min0, max0, valinit = max0)
            self.sopen2 = Slider(axopening2, 'Binary opening 1', 0, 10, valinit = 1)
            self.sclose2 = Slider(axclosing2, 'Binary closing 1', 0, 10, valinit = 1)
            self.sopen3 = Slider(axopening3, 'Binary opening 2', 0, 10, valinit = 1)
            self.sclose3 = Slider(axclosing3, 'Binary closing 2', 0, 10, valinit = 1)
            
            self.smin.on_changed(self.updateImg1Threshold3D)
            self.smax.on_changed(self.updateImg1Threshold3D)
            self.sopen2.on_changed(self.updateImg2Binary3D)
            self.sclose2.on_changed(self.updateImg2Binary3D)
            self.sopen3.on_changed(self.updateImg3Binary3D)
            self.sclose3.on_changed(self.updateImg3Binary3D)
            
        else:
            
            print('Spatny vstup.\nDimenze vstupu neni 2 ani 3.\nUkoncuji prahovani.')

    def showPlot(self):
        
        # Zobrazeni plot (figure)
        matpyplot.show()
        return self.imgChanged 

    def updateImg2D(self, val):
        
        # Prahovani (smin, smax)
        img1 = self.imgUsed.copy() > self.smin.val
        self.imgChanged = img1 #< self.smax.val
        
        # Predani obrazku k vykresleni
        self.im1 = self.ax1.imshow(self.imgChanged, self.cmap)
        # Prekresleni
        self.fig.canvas.draw()
        
    def updateImg1Threshold3D(self, val):
        
        # Prahovani (smin, smax)
        self.imgChanged = (self.imgUsed > self.smin.val) & (self.imgUsed < self.smax.val)
        
        # Predani obrazku k vykresleni
        self.imgShow = numpy.amax(self.imgChanged, 2)
        self.im1 = self.ax1.imshow(self.imgShow, self.cmap)
        
        # Prekresleni
        self.fig.canvas.draw()
        
    def updateImg2Binary3D(self, val):
        
        imgChanged2 = self.imgChanged
        
        if(self.sopen2.val >= 0.5):
            imgChanged2 = scipy.ndimage.binary_opening(self.imgChanged, structure = None, iterations = int(numpy.round(self.sopen2.val, 0)))
        else:
            imgChanged2 = self.imgChanged2
            
        if(self.sclose2.val >= 0.5):
            self.imgChanged2 = scipy.ndimage.binary_closing(imgChanged2, structure = None, iterations = int(numpy.round(self.sclose2.val, 0)))
        else:
            self.imgChanged2 = imgChanged2
            
        # Predani obrazku k vykresleni
        self.imgShow2 = numpy.amax(self.imgChanged2, 2)
        self.im2 = self.ax2.imshow(self.imgShow2, self.cmap)
        
        # Prekresleni
        self.fig.canvas.draw()
        
    def updateImg3Binary3D(self, val):
        
        imgChanged3 = self.imgChanged
        
        if(self.sclose3.val >= 0.5):
            imgChanged3 = scipy.ndimage.binary_closing(self.imgChanged, structure = None, iterations = int(numpy.round(self.sclose3.val, 0)))
        else:
            imgChanged3 = self.imgChanged
        
        if(self.sopen3.val >= 0.5):
            self.imgChanged3 = scipy.ndimage.binary_opening(imgChanged3, structure = None, iterations = int(numpy.round(self.sopen3.val, 0)))
        else:
            self.imgChanged3 = imgChanged3
            
        # Predani obrazku k vykresleni
        self.imgShow3 = numpy.amax(self.imgChanged3, 2)
        self.im3 = self.ax3.imshow(self.imgShow3, self.cmap)
        
        # Prekresleni
        self.fig.canvas.draw()
    
"""
================================================================================
main
================================================================================
"""
"""
if __name__ == "__main__":
    
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    logging.basicConfig(format='%(message)s')

    formatter = logging.Formatter("%(levelname)-5s [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    parser = argparse.ArgumentParser(description='Segment vessels from liver')
    parser.add_argument('-f','--filename',
            default = 'lena',
            help='*.mat file with variables "data", "segmentation" and "threshod"')
    parser.add_argument('-d', '--debug', action='store_true',
            help='run in debug mode')
    parser.add_argument('-t', '--tests', action='store_true',
            help='run unittest')
    parser.add_argument('-o', '--outputfile', type=str,
        default='output.mat',help='output file name')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.tests:
        sys.argv[1:]=[]
        unittest.main()

    if args.filename == 'lena':
        data = scipy.misc.lena()
    else:
        mat = scipy.io.loadmat(args.filename)
        logger.debug(mat.keys())

        dataraw = scipy.io.loadmat(args.filename)
        
        data = dataraw['data'] * (dataraw['segmentation'] == 1)

    ui = uiThreshold(data)
    output = ui.showPlot()

    scipy.io.savemat(args.outputfile, {'data':output})
"""





