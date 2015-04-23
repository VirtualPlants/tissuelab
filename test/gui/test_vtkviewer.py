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

def demo_polydata_cube():
    
    def mkVtkIdList(it):
        vil = vtk.vtkIdList()
        for i in it:
            vil.InsertNextId(int(i))
        return vil
 
    x = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
         (0.0, 0.0, 1.0), (1.0, 0.0 ,1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0)]
 
    pts = [(0,1,2,3), (4,5,6,7), (0,1,5,4),
           (1,2,6,5), (2,3,7,6), (3,0,4,7)]
 
    # We'll create the building blocks of polydata including data attributes.
    cube    = vtk.vtkPolyData()
    points  = vtk.vtkPoints()
    polys   = vtk.vtkCellArray()
    scalars = vtk.vtkFloatArray()
 
    # Load the point, cell, and data attributes.
    for i in range(8):
        points.InsertPoint(i, x[i])
    for i in range(6):
        polys.InsertNextCell( mkVtkIdList(pts[i]) )
    for i in range(8):
        scalars.InsertTuple1(i,i)
 
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

    def test_polydata(self):
        cube = demo_polydata_cube()
        self.widget.add_polydata("cube", cube, colormap='glasbey', alpha=0.5)

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
        self.widget.add_matrix_as_volume("matrix", matrix, colormap='glasbey', alphamap='constant',
                                         alpha=1, bg_id=0)

    def test_intensity_range(self):
        self.widget.add_matrix_as_volume("matrix_ref", demo_matrix_range(delta=0), colormap='curvature',
                                         alphamap='constant', alpha=1, bg_id=0)
        self.widget.add_matrix_as_volume("matrix_2", demo_matrix_range(delta=10), colormap='curvature',
                                         alphamap='constant', alpha=1, bg_id=0,
                                         intensity_range=(105, 135))

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
