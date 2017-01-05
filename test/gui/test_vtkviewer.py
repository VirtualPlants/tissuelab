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

from Qt import QtCore, QtGui, QtWidgets
from tissuelab.gui.vtkviewer.vtkviewer import VtkViewer
from tissuelab.gui.vtkviewer.testing import VtkQtTestCase
from tissuelab.gui.vtkviewer.testing import demo_actor, demo_matrix_range, demo_matrix_xyz, demo_polydata_cube

########################################################################################################################
# WARNING: image references are also used in test_vtkworldviewer
########################################################################################################################


class TestCase(VtkQtTestCase):
    WIDGET_CLASS = VtkViewer
    SAVE_AS_REFERENCE = False
    PAUSE_FACTOR = 1000

    def tear_down(self):
        self.widget.compute()

    def save_screenshot(self, filepath):
        self.widget.save_screenshot(filepath)

    def test_actor(self):
        actor = demo_actor()
        self.widget.add_actor("actor", actor)
        self.pause(0.5)

    def test_polydata(self):
        cube = demo_polydata_cube()
        self.widget.add_polydata("cube", cube, colormap='glasbey', alpha=0.5)
        self.pause(0.5)

    def test_outline(self):
        matrix = demo_matrix_xyz()
        self.widget.add_outline("matrix", matrix)
        self.pause(0.5)

    def test_matrix_cut_planes(self):
        matrix = demo_matrix_xyz()
        n = "matrix"
        self.widget.add_matrix_cut_planes(n, matrix, colormap='glasbey')
        self.widget.move_cut_plane(n, 1000, 1)
        self.widget.move_cut_plane(n, -1000, 2)
        self.widget.render()

        extent = self.widget.view_prop['matrix_cut_plane_1'].GetDisplayExtent()
        self.assertListEqual(list(extent), [99, 99, 0, 99, 0, 99])
        extent = self.widget.view_prop['matrix_cut_plane_2'].GetDisplayExtent()
        self.assertListEqual(list(extent), [0, 99, 0, 0, 0, 99])

    def test_matrix_cut_planes2(self):
        matrix = demo_matrix_xyz()
        n = "matrix"
        self.widget.add_matrix_cut_planes(n, matrix, colormap='glasbey')
        self.widget.move_cut_plane(n, 95, 1)
        self.widget.move_cut_plane(n, 95, 2)
        self.widget.move_cut_plane(n, 95, 3)
        self.widget.set_cut_planes_alpha(n, 0.5)
        self.widget.render()
        self.pause(1)

    def test_volume(self):
        matrix = demo_matrix_xyz()
        self.widget.add_matrix_as_volume("matrix", matrix, colormap='glasbey', alphamap='constant',
                                         alpha=1, bg_id=0)
        self.pause(0.5)

    def test_intensity_range(self):
        self.widget.add_matrix_as_volume("matrix_ref", demo_matrix_range(delta=0), colormap='curvature',
                                         alphamap='constant', alpha=1, bg_id=0)
        self.widget.add_matrix_as_volume("matrix_2", demo_matrix_range(delta=10), colormap='curvature',
                                         alphamap='constant', alpha=1, bg_id=0,
                                         intensity_range=(105, 135))
        self.pause(2)
