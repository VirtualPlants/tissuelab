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

import numpy as np
import vtk

from openalea.vpltk.qt import QtGui
from openalea.core.service.plugin import plugin_instance


def demo_matrix_xyz():
    dtype = np.uint16
    matrix = np.zeros([100, 100, 100], dtype=dtype)
    matrix[90:100, 0:10, 0:10] = 1
    matrix[0:10, 90:100, 0:10] = 2
    matrix[0:10, 0:10, 90:100] = 3
    return matrix


def demo_matrix1():
    dtype = np.uint16
    matrix = np.zeros([75, 75, 75], dtype=dtype)
    matrix[25:55, 25:55, 25:55] = 1
    matrix[45:74, 45:74, 45:74] = 10
    return matrix


def demo_matrix2():
    dtype = np.uint16
    matrix = np.zeros([75, 75, 75], dtype=dtype)
    matrix[0:10, 0:10, 0:10] = 1

    return matrix


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


def get_viewer():
    return plugin_instance('oalab.applet', 'VtkViewer')


def demo():
    viewer = get_viewer()
    matrix1 = demo_matrix1()
    matrix2 = demo_matrix2()
    sphere = demo_actor()

    viewer.add_matrix('matrix1', matrix1)
    viewer.color_cell('matrix1')

    viewer.add_matrix('matrix2', matrix2)
    viewer.color_cell('matrix2', colormap='monocolor')

    viewer.add_actor('sphere', sphere)

    viewer.compute()


if __name__ == '__main__':

    from openalea.oalab.gui.splittablewindow import TestMainWin
    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    tests = [
        demo,
        demo_actor,
        demo_matrix1,
        demo_matrix2,
    ]

    layout = {'children': {'0': [3, 4], '3': [5, 6]},
              'interface': 'ISplittableUi',
              'parents': {'0': None, '3': 0, '4': 0, '5': 3, '6': 3},
              'properties': {'0': {'amount': 0.7046703296703297, 'splitDirection': 2},
                             '3': {'amount': 0.3250497017892644, 'splitDirection': 1},
                             '4': {'widget': {'applets': [{'name': 'ShellWidget'}], }},
                             '5': {'widget': {'applets': [{'name': 'WorldControl'}], }},
                             '6': {'widget': {'applets': [{'name': 'TissueViewer'}], }},
                             }
              }

    mw = TestMainWin(default_layout=layout, tests=tests, layout_file='.test_tissueviewer.oaui')

    mw.resize(1024, 768)
    mw.show()

    mw.initialize()

    if instance is None:
        app.exec_()
