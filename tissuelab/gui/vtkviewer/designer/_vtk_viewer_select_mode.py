# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tissuelab/gui/vtkviewer/designer/vtk_viewer_select_mode.ui'
#
# Created: Thu Jun 11 16:51:24 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_vtk_viewer_select_mode(object):
    def setupUi(self, vtk_viewer_select_mode):
        vtk_viewer_select_mode.setObjectName(_fromUtf8("vtk_viewer_select_mode"))
        vtk_viewer_select_mode.resize(306, 66)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(vtk_viewer_select_mode.sizePolicy().hasHeightForWidth())
        vtk_viewer_select_mode.setSizePolicy(sizePolicy)
        vtk_viewer_select_mode.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        vtk_viewer_select_mode.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_2 = QtGui.QGridLayout(vtk_viewer_select_mode)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cb_interactor_choice = QtGui.QComboBox(vtk_viewer_select_mode)
        self.cb_interactor_choice.setObjectName(_fromUtf8("cb_interactor_choice"))
        self.gridLayout_2.addWidget(self.cb_interactor_choice, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.image1_label = QtGui.QLabel(vtk_viewer_select_mode)
        self.image1_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.image1_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.image1_label.setObjectName(_fromUtf8("image1_label"))
        self.gridLayout.addWidget(self.image1_label, 2, 2, 1, 1)
        self.image2_label = QtGui.QLabel(vtk_viewer_select_mode)
        self.image2_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.image2_label.setObjectName(_fromUtf8("image2_label"))
        self.gridLayout.addWidget(self.image2_label, 1, 2, 1, 1)
        self.image2_cb = QtGui.QComboBox(vtk_viewer_select_mode)
        self.image2_cb.setObjectName(_fromUtf8("image2_cb"))
        self.gridLayout.addWidget(self.image2_cb, 1, 3, 1, 1)
        self.image1_cb = QtGui.QComboBox(vtk_viewer_select_mode)
        self.image1_cb.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.image1_cb.setObjectName(_fromUtf8("image1_cb"))
        self.gridLayout.addWidget(self.image1_cb, 2, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 2, 1)
        self.action_launch_button = QtGui.QPushButton(vtk_viewer_select_mode)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.action_launch_button.sizePolicy().hasHeightForWidth())
        self.action_launch_button.setSizePolicy(sizePolicy)
        self.action_launch_button.setMinimumSize(QtCore.QSize(0, 0))
        self.action_launch_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.action_launch_button.setBaseSize(QtCore.QSize(0, 0))
        self.action_launch_button.setIconSize(QtCore.QSize(16, 10))
        self.action_launch_button.setObjectName(_fromUtf8("action_launch_button"))
        self.gridLayout_2.addWidget(self.action_launch_button, 1, 0, 1, 1)

        self.retranslateUi(vtk_viewer_select_mode)
        QtCore.QMetaObject.connectSlotsByName(vtk_viewer_select_mode)

    def retranslateUi(self, vtk_viewer_select_mode):
        vtk_viewer_select_mode.setWindowTitle(_translate("vtk_viewer_select_mode", "Form", None))
        self.cb_interactor_choice.setToolTip(_translate("vtk_viewer_select_mode", "choose your interaction mode", None))
        self.image1_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your segmented matrix", None))
        self.image1_label.setText(_translate("vtk_viewer_select_mode", "<html><head/><body><p>Segmented</p></body></html>", None))
        self.image2_label.setToolTip(_translate("vtk_viewer_select_mode", "choose your intensity matrix", None))
        self.image2_label.setText(_translate("vtk_viewer_select_mode", "<html><head/><body><p>Intensity</p></body></html>", None))
        self.action_launch_button.setToolTip(_translate("vtk_viewer_select_mode", "Start the selected cell edition", None))
        self.action_launch_button.setText(_translate("vtk_viewer_select_mode", "Edit Cell", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    vtk_viewer_select_mode = QtGui.QWidget()
    ui = Ui_vtk_viewer_select_mode()
    ui.setupUi(vtk_viewer_select_mode)
    vtk_viewer_select_mode.show()
    sys.exit(app.exec_())

