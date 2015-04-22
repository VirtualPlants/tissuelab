# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       TissueLab
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
#
###############################################################################

import vtk
import numpy as np
import unittest
from openalea.vpltk.qt import QtGui, QtTest, QtCore
from tissuelab.gui.vtkviewer.vtkviewer import VtkViewer


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


def demo_matrix_xyz():
    dtype = np.uint16
    matrix = np.zeros([100, 100, 100], dtype=dtype)
    matrix[90:100, 0:10, 0:10] = 1
    matrix[0:10, 90:100, 0:10] = 2
    matrix[0:10, 0:10, 90:100] = 3
    return matrix


class QtTestCase(object):

    def init(self):
        self.instance = QtGui.QApplication.instance()
        if self.instance is None:
            self.app = QtGui.QApplication([])
        else:
            self.app = self.instance

    def exec_(self):
        if self.instance is None:
            self.app.exec_()


class TestCase(QtTestCase, unittest.TestCase):

    def setUp(self):
        self.widget = None
        self.init()
        self.widget = VtkViewer()

    def test_actor(self):
        actor = demo_actor()
        self.widget.add_actor("actor", actor)

    def test_outline(self):
        matrix = demo_matrix_xyz()
        self.widget.add_outline("matrix", matrix)

    def test_matrix_cut_planes(self):
        matrix = demo_matrix_xyz()
        n = "matrix"
        self.widget.add_matrix_cut_planes(n, matrix, colormap='glasbey')
        self.widget.move_cut_plane(n, 100, 1)
        self.widget.move_cut_plane(n, 100, 2)
        self.widget.move_cut_plane(n, 100, 3)
        self.widget.set_cut_planes_alpha(n, 0.5)
        self.widget.render()

    def test_volume(self):
        matrix = demo_matrix_xyz()
        self.widget.add_matrix_as_volume("matrix", matrix)

    def tearDown(self):
        self.widget.compute()
        self.widget.show()
        self.widget.raise_()
        QtTest.QTest.qWait(1000)
        if self.widget:
            self.widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.widget.close()
            del self.widget
        self.app.quit()
        del self.app
        del self.instance

if __name__ == '__main__':

    tc = QtTestCase()
    tc.init()

    widget = VtkViewer()
    widget.show()
    widget.raise_()
    widget.compute()

    tc.exec_()
