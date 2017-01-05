from tissuelab.mockup.ui_omeroclient import Ui_Form
from Qt import QtWidgets

class OmeroClientWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
