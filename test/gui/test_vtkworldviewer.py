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

from openalea.vpltk.qt import QtGui, QtCore
from tissuelab.gui.vtkviewer.vtkworldviewer import VtkWorldViewer
from tissuelab.gui.vtkviewer.testing import VtkQtTestCase
from tissuelab.gui.vtkviewer.testing import demo_actor, demo_matrix_range, demo_matrix_xyz, demo_polydata_cube

from openalea.oalab.world import World


class TestCase(VtkQtTestCase):
    WIDGET_CLASS = VtkWorldViewer
    SAVE_AS_REFERENCE = False
    PAUSE_FACTOR = 1000

    def set_up(self):
        self.world = World()
        self.world.clear()

    def tear_down(self):
        self.widget.compute()
        self.widget.ren.ResetCamera()

    def save_screenshot(self, filepath):
        self.widget.save_screenshot(filepath)

    def test_volume(self):
        matrix = demo_matrix_xyz()
        self.widget.set_world(self.world)
        self.world.add(matrix, name="matrix", colormap='glasbey', alphamap='constant', alpha=1, bg_id=0)
        self.pause(1)
        self.ref("test_vtkviewer.test_volume.png")

    def atest_actor_added_after_set_world(self):
        actor = demo_actor()
        self.widget.set_world(self.world)
        self.world.add(actor)
        self.widget.compute()
        self.pause(1)

    def atest_actor_added_before_set_world(self):
        actor = demo_actor()
        self.world.add(actor)
        self.widget.set_world(self.world)
        self.widget.compute()
        self.pause(1)
