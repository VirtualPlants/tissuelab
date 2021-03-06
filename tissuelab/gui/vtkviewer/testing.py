# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
import vtk
import numpy as np
import unittest
from openalea.vpltk.qt import QtGui, QtCore
from PyQt4 import QtTest


def demo_actor():
    source = vtk.vtkSphereSource()
    source.SetCenter(0, 0, 0)
    source.SetRadius(5.0)

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(source.GetOutput())
    else:
        mapper.SetInputConnection(source.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def demo_polydata_cube():

    def mkVtkIdList(it):
        vil = vtk.vtkIdList()
        for i in it:
            vil.InsertNextId(int(i))
        return vil

    x = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
         (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0)]

    pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

    # We'll create the building blocks of polydata including data attributes.
    cube = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()

    # Load the point, cell, and data attributes.
    for i in range(8):
        points.InsertPoint(i, x[i])
    for i in range(6):
        polys.InsertNextCell(mkVtkIdList(pts[i]))
    for i in range(8):
        scalars.InsertTuple1(i, i)

    # We now assign the pieces to the vtkPolyData.
    cube.SetPoints(points)
    cube.SetPolys(polys)
    cube.GetPointData().SetScalars(scalars)

    return cube


def demo_matrix_xyz():
    dtype = np.uint16
    matrix = np.zeros([100, 100, 100], dtype=dtype)
    matrix[90:100, 0:10, 0:10] = 1
    matrix[0:10, 90:100, 0:10] = 2
    matrix[0:10, 0:10, 90:100] = 3
    return matrix


def demo_matrix_range(delta=0):
    dtype = np.uint16
    matrix = np.zeros([255, 255, 255], dtype=dtype)
    for i in range(0, 255, 10):
        matrix[i:i + 5, delta + 0:delta + 5, 0:5] = i
    return matrix

from openalea.oalab.testing.qtunittest import QtTestCase


class VtkQtTestCase(QtTestCase):

    def tear_down(self):
        pass

    def set_up(self):
        pass

    def _refpath(self):
        from openalea.core.path import path
        if self._ref is None:
            filename = self.id().replace('TestCase.', '') + '.png'
        else:
            filename = self._ref
        return path('ref') / filename

    def ref(self, filename):
        self._ref = filename

    def setUp(self):
        self._ref = None
        self.widget = None
        self.init()
        self.widget = self.WIDGET_CLASS()
        self.widget.ren.SetBackground(0, 0, 0)

        self.widget.resize(300, 300)

        self.l_ref = QtGui.QLabel()
        self.cmp_widget = QtGui.QWidget()
        layout = QtGui.QGridLayout(self.cmp_widget)
        name = self.id().split('.')[-1]
        layout.addWidget(QtGui.QLabel(name), 0, 0)
        layout.addWidget(self.widget, 1, 0)
        layout.addWidget(QtGui.QLabel("Reference"), 0, 1)
        layout.addWidget(self.l_ref, 1, 1)

        self.set_up()

    def tearDown(self):
        self.tear_down()

        self.l_ref.resize(300, 300)
        self.l_ref.setPixmap(QtGui.QPixmap(self._refpath()))
        self._ref = None

        self.cmp_widget.show()
        self.cmp_widget.raise_()

        if self._pause:
            if self.SAVE_AS_REFERENCE:
                filepath = self._refpath()
                self.widget.setFocus(True)
                QtTest.QTest.qWait(1)
                self.save_screenshot(filepath)
            else:
                QtTest.QTest.qWait(self._duration)

        if self.widget:
            self.widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.widget.close()
            del self.widget
        self.app.quit()
        del self.app
        del self.instance
