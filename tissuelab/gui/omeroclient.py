
from ui_omeroclient import Ui_Form
from openalea.vpltk.qt import QtGui

class OmeroClientWidget(QtGui.QWidget, Ui_Form):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
