# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
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

from openalea.oalab.gui.control.manager import ControlManagerWidget
from openalea.vpltk.qt import QtGui, QtCore


class VtkControlPanel(ControlManagerWidget):

    def __init__(self, parent=None):
        ControlManagerWidget.__init__(self)
        self._layout = QtGui.QVBoxLayout(self)

        self._viewer = None

        from openalea.core.control.manager import ControlContainer
        self.controls = ControlContainer()
        self.model.set_manager(self.controls)

        self.controls.add('matrix_name', interface='IStr', value='', alias='Matrix name')

        for i, data in enumerate([
            ('x', self._x_slider_changed),
            ('y', self._y_slider_changed),
            ('z', self._z_slider_changed),
        ]):
            name, func = data
            c = self.controls.add(name, interface='IInt', value=1, alias='Move %s plane' % name)
            c.interface.min = 0
            c.interface.max = 100
            self.controls.register_follower(name, func)

        self.controls.add('volume', interface='IBool', value=True, alias='Display volume')
        self.controls.add('cut_planes', interface='IBool', value=True, alias='Display cut plane')

        self.controls.register_follower('volume', self._display_volume_changed)
        self.controls.register_follower('cut_planes', self._display_cut_planes_changed)
        self.controls.register_follower('matrix_name', self._matrix_name_changed)

        self._current = None

    def set_viewer(self, viewer):
        self._viewer = viewer

    def set_matrix(self, data_matrix):
        viewer = self.sender()
        if viewer is None:
            return

        self.set_viewer(viewer.vtk)

        if isinstance(data_matrix, basestring):
            self.controls.control(name='matrix_name').value = data_matrix
            data_matrix = self._viewer.matrix[data_matrix]

        for orientation in (0, 1, 2):
            c = self.controls.control(name=list('xyz')[orientation])
            c.interface.min = 0
            c.interface.max = data_matrix.shape[orientation]
            c.value = c.interface.max / 2

    def _matrix_name_changed(self, old, new):
        self._current = new

    def _display_cut_planes_changed(self, old, new):
        self._viewer.display_cut_planes(name=self._current, disp=new)

    def _display_volume_changed(self, old, new):
        self._viewer.display_volume(name=self._current, disp=new)

    def _x_slider_changed(self, old, new):
        name = self._current
        self._viewer.move_cut_plane(name, new, 1)

    def _y_slider_changed(self, old, new):
        name = self._current
        self._viewer.move_cut_plane(name, new, 2)

    def _z_slider_changed(self, old, new):
        name = self._current
        self._viewer.move_cut_plane(name, new, 3)
