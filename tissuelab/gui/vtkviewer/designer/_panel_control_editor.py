# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panel_control_editor.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_panel_control_editor(object):
    def setupUi(self, panel_control_editor):
        panel_control_editor.setObjectName("panel_control_editor")
        panel_control_editor.resize(536, 82)
        self.gridLayout = QtWidgets.QGridLayout(panel_control_editor)
        self.gridLayout.setObjectName("gridLayout")
        self.bp_moins = QtWidgets.QPushButton(panel_control_editor)
        self.bp_moins.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_moins.setMaximumSize(QtCore.QSize(60, 27))
        self.bp_moins.setObjectName("bp_moins")
        self.gridLayout.addWidget(self.bp_moins, 2, 3, 1, 1)
        self.sb_cut_plane = QtWidgets.QSpinBox(panel_control_editor)
        self.sb_cut_plane.setMinimumSize(QtCore.QSize(60, 0))
        self.sb_cut_plane.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sb_cut_plane.setObjectName("sb_cut_plane")
        self.gridLayout.addWidget(self.sb_cut_plane, 2, 4, 1, 1)
        self.bp_y = QtWidgets.QPushButton(panel_control_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_y.sizePolicy().hasHeightForWidth())
        self.bp_y.setSizePolicy(sizePolicy)
        self.bp_y.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_y.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_y.setObjectName("bp_y")
        self.gridLayout.addWidget(self.bp_y, 2, 1, 1, 1)
        self.bp_x = QtWidgets.QPushButton(panel_control_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_x.sizePolicy().hasHeightForWidth())
        self.bp_x.setSizePolicy(sizePolicy)
        self.bp_x.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_x.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_x.setObjectName("bp_x")
        self.gridLayout.addWidget(self.bp_x, 2, 0, 1, 1)
        self.bp_fusion = QtWidgets.QPushButton(panel_control_editor)
        self.bp_fusion.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_fusion.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_fusion.setObjectName("bp_fusion")
        self.gridLayout.addWidget(self.bp_fusion, 0, 4, 1, 1)
        self.bp_move = QtWidgets.QPushButton(panel_control_editor)
        self.bp_move.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_move.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_move.setObjectName("bp_move")
        self.gridLayout.addWidget(self.bp_move, 0, 0, 1, 2)
        self.bp_new_edit = QtWidgets.QPushButton(panel_control_editor)
        self.bp_new_edit.setMinimumSize(QtCore.QSize(80, 0))
        self.bp_new_edit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_new_edit.setObjectName("bp_new_edit")
        self.gridLayout.addWidget(self.bp_new_edit, 0, 7, 1, 1)
        self.bp_select = QtWidgets.QPushButton(panel_control_editor)
        self.bp_select.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_select.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_select.setObjectName("bp_select")
        self.gridLayout.addWidget(self.bp_select, 0, 2, 1, 2)
        self.slider_cut_plane = QtWidgets.QSlider(panel_control_editor)
        self.slider_cut_plane.setMinimumSize(QtCore.QSize(90, 29))
        self.slider_cut_plane.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.slider_cut_plane.setOrientation(QtCore.Qt.Horizontal)
        self.slider_cut_plane.setObjectName("slider_cut_plane")
        self.gridLayout.addWidget(self.slider_cut_plane, 2, 5, 1, 1)
        self.slider_propagation = QtWidgets.QSlider(panel_control_editor)
        self.slider_propagation.setMinimumSize(QtCore.QSize(60, 0))
        self.slider_propagation.setMaximumSize(QtCore.QSize(120, 16777215))
        self.slider_propagation.setOrientation(QtCore.Qt.Horizontal)
        self.slider_propagation.setObjectName("slider_propagation")
        self.gridLayout.addWidget(self.slider_propagation, 0, 9, 1, 1)
        self.sb_propagation = QtWidgets.QSpinBox(panel_control_editor)
        self.sb_propagation.setMinimumSize(QtCore.QSize(60, 0))
        self.sb_propagation.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sb_propagation.setObjectName("sb_propagation")
        self.gridLayout.addWidget(self.sb_propagation, 0, 8, 1, 1)
        self.bp_z = QtWidgets.QPushButton(panel_control_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_z.sizePolicy().hasHeightForWidth())
        self.bp_z.setSizePolicy(sizePolicy)
        self.bp_z.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_z.setMaximumSize(QtCore.QSize(50, 27))
        self.bp_z.setObjectName("bp_z")
        self.gridLayout.addWidget(self.bp_z, 2, 2, 1, 1)
        self.bp_split = QtWidgets.QPushButton(panel_control_editor)
        self.bp_split.setMinimumSize(QtCore.QSize(60, 0))
        self.bp_split.setMaximumSize(QtCore.QSize(120, 16777215))
        self.bp_split.setObjectName("bp_split")
        self.gridLayout.addWidget(self.bp_split, 0, 5, 1, 1)
        self.bp_plus = QtWidgets.QPushButton(panel_control_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_plus.sizePolicy().hasHeightForWidth())
        self.bp_plus.setSizePolicy(sizePolicy)
        self.bp_plus.setMinimumSize(QtCore.QSize(30, 27))
        self.bp_plus.setMaximumSize(QtCore.QSize(60, 27))
        self.bp_plus.setObjectName("bp_plus")
        self.gridLayout.addWidget(self.bp_plus, 2, 7, 1, 1)
        self.bp_save = QtWidgets.QPushButton(panel_control_editor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bp_save.sizePolicy().hasHeightForWidth())
        self.bp_save.setSizePolicy(sizePolicy)
        self.bp_save.setMinimumSize(QtCore.QSize(110, 27))
        self.bp_save.setMaximumSize(QtCore.QSize(240, 27))
        self.bp_save.setObjectName("bp_save")
        self.gridLayout.addWidget(self.bp_save, 2, 8, 1, 2)

        self.retranslateUi(panel_control_editor)
        QtCore.QMetaObject.connectSlotsByName(panel_control_editor)

    def retranslateUi(self, panel_control_editor):
        _translate = QtCore.QCoreApplication.translate
        panel_control_editor.setWindowTitle(_translate("panel_control_editor", "Form"))
        self.bp_moins.setToolTip(_translate("panel_control_editor", "change the origine of the plane view"))
        self.bp_moins.setText(_translate("panel_control_editor", "-"))
        self.sb_cut_plane.setToolTip(_translate("panel_control_editor", "change the origine of the plane view"))
        self.bp_y.setToolTip(_translate("panel_control_editor", "change the normal of the plane view to the axis y"))
        self.bp_y.setText(_translate("panel_control_editor", "Y"))
        self.bp_x.setToolTip(_translate("panel_control_editor", "change the normal of the plane view to the axis x"))
        self.bp_x.setText(_translate("panel_control_editor", "X"))
        self.bp_fusion.setToolTip(_translate("panel_control_editor", "click to fusion the considered cell with the selected one"))
        self.bp_fusion.setText(_translate("panel_control_editor", "Fusion"))
        self.bp_move.setToolTip(_translate("panel_control_editor", "this mode allow you to move the point in the considered cell"))
        self.bp_move.setText(_translate("panel_control_editor", "move"))
        self.bp_new_edit.setToolTip(_translate("panel_control_editor", "Switch from the considered cell to the selected one in the editor"))
        self.bp_new_edit.setText(_translate("panel_control_editor", "Edit select"))
        self.bp_select.setToolTip(_translate("panel_control_editor", "this mode allow you to select a cell"))
        self.bp_select.setText(_translate("panel_control_editor", "Select"))
        self.slider_cut_plane.setToolTip(_translate("panel_control_editor", "change the origine of the plane view"))
        self.slider_propagation.setToolTip(_translate("panel_control_editor", "choose the propagation of the deplacement you want"))
        self.sb_propagation.setToolTip(_translate("panel_control_editor", "choose the propagation of the deplacement you want"))
        self.bp_z.setToolTip(_translate("panel_control_editor", "change the normal of the plane view to the axis z"))
        self.bp_z.setText(_translate("panel_control_editor", "Z"))
        self.bp_split.setToolTip(_translate("panel_control_editor", "Split the considered cell in two, along the plane view"))
        self.bp_split.setText(_translate("panel_control_editor", "Split cell"))
        self.bp_plus.setToolTip(_translate("panel_control_editor", "change the origine of the plane view"))
        self.bp_plus.setText(_translate("panel_control_editor", "+"))
        self.bp_save.setToolTip(_translate("panel_control_editor", "Apply changes to the segmented matrix"))
        self.bp_save.setText(_translate("panel_control_editor", "Apply changes"))

