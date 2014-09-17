
from openalea.vpltk.qt import QtGui, QtCore

class Slider(QtGui.QWidget):
    
    valueChanged = QtCore.Signal(int)
    
    def __init__(self, key, label=u'label', orientation=QtCore.Qt.Horizontal):
        QtGui.QWidget.__init__(self)
        
        self.key = key
        
        if orientation == QtCore.Qt.Horizontal :
            self._layout = QtGui.QHBoxLayout(self)
        else :
            self._layout = QtGui.QVBoxLayout(self)
            
        self._value = 0
        self._vmax = 0

        #size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        #self.setSizePolicy(size_policy)

        self.label = QtGui.QLabel(label)
        
        self.spinbox = QtGui.QSpinBox()
        self.slider = QtGui.QSlider()
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
        if value != self._value :
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