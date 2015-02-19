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
from openalea.core.service.ipython import interpreter as get_interpreter


class VtkControlPanel(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        from openalea.core.control.manager import ControlContainer

        self._manager = ControlContainer()
        self._view = ControlManagerWidget(manager=self._manager)

        self._params = {}

        self._cb_matrix_name = QtGui.QComboBox()
        p = QtGui.QSizePolicy
        self._cb_matrix_name.setSizePolicy(p(p.Expanding, p.Maximum))
        self._cb_matrix_name.currentIndexChanged.connect(self._matrix_name_changed)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self._cb_matrix_name)
        self._layout.addWidget(self._view)

        self._viewer = None

        self._view.model.set_manager(self._manager)

        for i, data in enumerate([
            ('x', self._x_slider_changed),
            ('y', self._y_slider_changed),
            ('z', self._z_slider_changed),
        ]):
            name, func = data
            c = self._manager.add(name, interface='IInt', value=1, alias='Move %s plane' % name)
            c.interface.min = 0
            c.interface.max = 100
            self._manager.register_follower(name, func)

        self._manager.add('volume', interface='IBool', value=True, alias='Display volume')
        self._manager.add('cut_planes', interface='IBool', value=True, alias='Display cut plane')

        self._manager.register_follower('volume', self._display_volume_changed)
        self._manager.register_follower('cut_planes', self._display_cut_planes_changed)

        self._current = None

        self.interpreter = get_interpreter()
        self.interpreter.locals['viewer_control'] = self

    def __getitem__(self, key):
        return self._manager.control(name=key)

    def set_viewer(self, viewer):
        self._viewer = viewer

    def clear(self):
        print '---------->'
        self._cb_matrix_name.clear()
        self._params.clear()

    def set_matrix(self, name):
        viewer = self.sender()
        if viewer is None:
            return

        self.set_viewer(viewer.vtk)

        if not isinstance(name, basestring):
            raise NotImplementedError

        if name not in self._params:
            self._cb_matrix_name.addItem(name)
            self._params[name] = {}

        for actor_name in viewer.vtk.actor:
            if actor_name.startswith('%s_cut_plane_' % name):
                disp = viewer.vtk.property[actor_name]['disp']
                break

        self._params[name]['volume'] = viewer.vtk.volume_property[name]['disp']
        self._params[name]['cut_planes'] = disp

        data_matrix = self._viewer.matrix[name]

        for orientation in (0, 1, 2):
            c_id = list('xyz')[orientation]
            c = self._manager.control(name=c_id)
            c.interface.min = 0
            c.interface.max = data_matrix.shape[orientation]
            c.value = c.interface.max / 2
            self._params[name][c_id] = c.interface.max / 2

    def _matrix_name_changed(self, idx):
        if idx == -1:
            return
        name = self._cb_matrix_name.itemText(idx)
        self.select_matrix(name)

    def select_matrix(self, name):
        if name != self._current:
            # Store old matrix values
            if self._current in self._params:
                for c_id in self._params[self._current].keys():
                    control = self._manager.control(name=c_id)
                    self._params[self._current][c_id] = control.value

            # Update matrix name
            self._current = name

            # Update parameters with new matrix values
            if name in self._params:
                for c_id, value in self._params[name].items():
                    control = self._manager.control(name=c_id)
                    control.value = value

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
