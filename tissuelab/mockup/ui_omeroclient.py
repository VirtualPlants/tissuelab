# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/gbaty/Documents/TissueLab/demo/maquette_omero_client.ui'
#
# Created: Tue Jun  3 13:51:49 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import QtCore, QtGui

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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(722, 355)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeWidget = QtGui.QTreeWidget(self.splitter)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        item_3 = QtGui.QTreeWidgetItem(item_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/img_20.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item_3.setIcon(0, icon)
        item_3 = QtGui.QTreeWidgetItem(item_2)
        item_3.setIcon(0, icon)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.treeWidget.headerItem().setText(0, _translate("Form", "Omero database", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "mars-alt", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "study-vp0144", None))
        self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, _translate("Form", "dataset-2013-12-16", None))
        self.treeWidget.topLevelItem(0).child(0).child(1).setText(0, _translate("Form", "dataset-2013-12-17", None))
        self.treeWidget.topLevelItem(0).child(0).child(1).child(0).setText(0, _translate("Form", "img0001.lsm", None))
        self.treeWidget.topLevelItem(0).child(0).child(1).child(1).setText(0, _translate("Form", "img0002.lsm", None))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Form", "study-vp0143", None))
        self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, _translate("Form", "dataset...", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)

import resources_rc
