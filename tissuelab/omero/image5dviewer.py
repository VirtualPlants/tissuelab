# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

__all__ = ['Image5DViewer']

import time

from openalea.vpltk.qt import QtGui, QtCore

from slider import Slider
from utils import to_qimg


def hash_plane(*args):
    return args[0].getId(), str(tuple(args[1]))


class Image5DViewer(QtGui.QWidget):
    # Implements IImage5DViewer

    def __init__(self):

        self._img = None

        QtGui.QWidget.__init__(self)

        self.grid = QtGui.QGridLayout(self)

        self.image = QtGui.QLabel()
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        self.image.setSizePolicy(size_policy)

        self.l_status = QtGui.QLabel()

        self.slider_z = Slider('z', 'z', QtCore.Qt.Vertical)
        self.slider_c = Slider('c', 'c', QtCore.Qt.Vertical)
        self.slider_t = Slider('t', 't')

        self._dimension = list('zct')
        self._slider = [self.slider_z, self.slider_c, self.slider_t]
        for slider in self._slider:
            slider.hide()

        self.grid.addWidget(self.slider_c, 0, 0)
        self.grid.addWidget(self.slider_z, 0, 1)
        self.grid.addWidget(self.image, 0, 2)
        self.grid.addWidget(self.slider_t, 1, 2)
        self.grid.addWidget(self.l_status, 2, 0, 1, 3)

        for slider in self._slider:
            slider.setValue(0)
            slider.valueChanged.connect(self.update)

    def setData(self, data):
        # if previous image, clear old cache
        if self._img is not None:
            self.pixmap.clear_cache(self._img.getId())

        self._img = data
        if self._img is None:
            return

        for i, k in enumerate(self._dimension):
            get = getattr(self._img, 'getSize%s' % k.upper())
            slider = self._slider[i]
            slider.setValue(0)
            slider.setRange(0, get() - 1)
            if slider.vmax():
                slider.show()
            else:
                slider.hide()

        self.update()

    def sliderValues(self):
        values = [slider.value() for slider in self._slider]
        return values

    # @memoized(hash_plane, 500)
    def pixmap(self, img, values):
        pixels = img.getPrimaryPixels()
        plane = pixels.getPlane(*values)
        qimg = to_qimg(plane)
        # pixmap = QtGui.QPixmap.fromImage(qimg)
        return qimg

    def update(self, *args):
        values = self.sliderValues()
        disp = (values[0], self._slider[0].vmax(),
                values[1], self._slider[1].vmax(),
                values[2], self._slider[2].vmax())
        self.l_status.setText('z = %d/%d  -  c = %d/%d  -  t=%d/%d' % disp)

        if self._img is not None:
            t = time.time()
            size = self.image.size()
            self.image.setPixmap(self.pixmap(self._img, values).scaled(size.height(), size.width()))
