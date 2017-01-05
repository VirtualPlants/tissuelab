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

from Qt import QtCore, QtGui, QtWidgets

class Slider(QtWidgets.QWidget):

    valueChanged = QtCore.Signal(int)

    def __init__(self, key, label=u'label', orientation=QtCore.Qt.Horizontal):
        QtWidgets.QWidget.__init__(self)

        self.key = key

        if orientation == QtCore.Qt.Horizontal:
            self._layout = QtWidgets.QHBoxLayout(self)
        else:
            self._layout = QtWidgets.QVBoxLayout(self)

        self._value = 0
        self._vmax = 0

        #size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        #self.setSizePolicy(size_policy)

        self.label = QtWidgets.QLabel(label)

        self.spinbox = QtWidgets.QSpinBox()
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(orientation)

        self.slider.valueChanged.connect(self.setValue)
        self.spinbox.valueChanged.connect(self.setValue)

        self._layout.addWidget(self.label)
        self._layout.addWidget(self.spinbox)
        self._layout.addWidget(self.slider)

    def setRange(self, vmin, vmax):
        self.spinbox.setRange(vmin, vmax)
        self.slider.setRange(vmin, vmax)
        self._vmax = vmax

    def setValue(self, value):
        if value != self._value:
            self.spinbox.setValue(value)
            self.slider.setValue(value)
            self._value = value
            self.valueChanged.emit(value)

    def value(self):
        return self.spinbox.value()

    def vmax(self):
        return self._vmax

    def setVmax(self, vmax):
        self.setRange(self.range()[0], vmax)
