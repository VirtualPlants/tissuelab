# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panel_control_editor.ui'
#
# Created: Fri May 29 15:26:06 2015
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

class Ui_panel_control_editor(object):
    def setupUi(self, panel_control_editor):
        panel_control_editor.setObjectName(_fromUtf8("panel_control_editor"))
        panel_control_editor.resize(446, 82)
        self.gridLayout = QtGui.QGridLayout(panel_control_editor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.sb_cut_plane = QtGui.QSpinBox(panel_control_editor)
        self.sb_cut_plane.setMinimumSize(QtCore.QSize(60, 0))
        self.sb_cut_plane.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sb_cut_plane.setObjectName(_fromUtf8("sb_cut_plane"))
        self.gridLayout.addWidget(self.sb_cut_plane, 1, 4, 1, 1)
        self.bp_moins = QtGui.QPushButton(panel_control_editor)
        self.bp_moins.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_moins.setMaximumSize(QtCore.QSize(60, 27))
        self.bp_moins.setObjectName(_fromUtf8("bp_moins"))
        self.gridLayout.addWidget(self.bp_moins, 1, 3, 1, 1)
        self.bp_save = QtGui.QPushButton(panel_control_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_save.sizePolicy().hasHeightForWidth())
        self.bp_save.setSizePolicy(sizePolicy)
        self.bp_save.setMinimumSize(QtCore.QSize(50, 27))
        self.bp_save.setMaximumSize(QtCore.QSize(80, 27))
        self.bp_save.setObjectName(_fromUtf8("bp_save"))
        self.gridLayout.addWidget(self.bp_save, 1, 8, 1, 1)
        self.bp_plus = QtGui.QPushButton(panel_control_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_plus.sizePolicy().hasHeightForWidth())
        self.bp_plus.setSizePolicy(sizePolicy)
        self.bp_plus.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_plus.setMaximumSize(QtCore.QSize(60, 27))
        self.bp_plus.setObjectName(_fromUtf8("bp_plus"))
        self.gridLayout.addWidget(self.bp_plus, 1, 7, 1, 1)
        self.bp_z = QtGui.QPushButton(panel_control_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_z.sizePolicy().hasHeightForWidth())
        self.bp_z.setSizePolicy(sizePolicy)
        self.bp_z.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_z.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_z.setObjectName(_fromUtf8("bp_z"))
        self.gridLayout.addWidget(self.bp_z, 1, 2, 1, 1)
        self.bp_y = QtGui.QPushButton(panel_control_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_y.sizePolicy().hasHeightForWidth())
        self.bp_y.setSizePolicy(sizePolicy)
        self.bp_y.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_y.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_y.setObjectName(_fromUtf8("bp_y"))
        self.gridLayout.addWidget(self.bp_y, 1, 1, 1, 1)
        self.bp_x = QtGui.QPushButton(panel_control_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_x.sizePolicy().hasHeightForWidth())
        self.bp_x.setSizePolicy(sizePolicy)
        self.bp_x.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_x.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_x.setObjectName(_fromUtf8("bp_x"))
        self.gridLayout.addWidget(self.bp_x, 1, 0, 1, 1)
        self.bp_select = QtGui.QPushButton(panel_control_editor)
        self.bp_select.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_select.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_select.setObjectName(_fromUtf8("bp_select"))
        self.gridLayout.addWidget(self.bp_select, 0, 2, 1, 2)
        self.bp_fusion = QtGui.QPushButton(panel_control_editor)
        self.bp_fusion.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_fusion.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_fusion.setObjectName(_fromUtf8("bp_fusion"))
        self.gridLayout.addWidget(self.bp_fusion, 0, 4, 1, 1)
        self.bp_move = QtGui.QPushButton(panel_control_editor)
        self.bp_move.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_move.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_move.setObjectName(_fromUtf8("bp_move"))
        self.gridLayout.addWidget(self.bp_move, 0, 0, 1, 2)
        self.sb_propagation = QtGui.QSpinBox(panel_control_editor)
        self.sb_propagation.setMinimumSize(QtCore.QSize(60, 0))
        self.sb_propagation.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sb_propagation.setObjectName(_fromUtf8("sb_propagation"))
        self.gridLayout.addWidget(self.sb_propagation, 0, 5, 1, 1)
        self.slider_cut_plane = QtGui.QSlider(panel_control_editor)
        self.slider_cut_plane.setMinimumSize(QtCore.QSize(90, 29))
        self.slider_cut_plane.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.slider_cut_plane.setOrientation(QtCore.Qt.Horizontal)
        self.slider_cut_plane.setObjectName(_fromUtf8("slider_cut_plane"))
        self.gridLayout.addWidget(self.slider_cut_plane, 1, 5, 1, 2)
        self.slider_propagation = QtGui.QSlider(panel_control_editor)
        self.slider_propagation.setMinimumSize(QtCore.QSize(60, 0))
        self.slider_propagation.setMaximumSize(QtCore.QSize(120, 16777215))
        self.slider_propagation.setOrientation(QtCore.Qt.Horizontal)
        self.slider_propagation.setObjectName(_fromUtf8("slider_propagation"))
        self.gridLayout.addWidget(self.slider_propagation, 0, 6, 1, 1)

        self.retranslateUi(panel_control_editor)
        QtCore.QMetaObject.connectSlotsByName(panel_control_editor)

    def retranslateUi(self, panel_control_editor):
        panel_control_editor.setWindowTitle(_translate("panel_control_editor", "Form", None))
        self.bp_moins.setText(_translate("panel_control_editor", "-", None))
        self.bp_save.setText(_translate("panel_control_editor", "Save", None))
        self.bp_plus.setText(_translate("panel_control_editor", "+", None))
        self.bp_z.setText(_translate("panel_control_editor", "Z", None))
        self.bp_y.setText(_translate("panel_control_editor", "Y", None))
        self.bp_x.setText(_translate("panel_control_editor", "X", None))
        self.bp_select.setToolTip(_translate("panel_control_editor", "this mode allow you to select a cell", None))
        self.bp_select.setText(_translate("panel_control_editor", "Select", None))
        self.bp_fusion.setToolTip(_translate("panel_control_editor", "click to fusion the considered cell with the selected one", None))
        self.bp_fusion.setText(_translate("panel_control_editor", "Fusion", None))
        self.bp_move.setToolTip(_translate("panel_control_editor", "this mode allow you to move the point in the considered cell", None))
        self.bp_move.setText(_translate("panel_control_editor", "move", None))
        self.sb_propagation.setToolTip(_translate("panel_control_editor", "choose the propagation of the deplacement you want", None))

