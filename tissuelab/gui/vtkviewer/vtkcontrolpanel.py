# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

from openalea.oalab.control.manager import ControlManagerWidget
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.service.ipython import interpreter as get_interpreter


class VtkControlPanel(QtGui.QWidget):

    StyleTableView = 0
    StylePanel = 1
    DEFAULT_STYLE = StylePanel

    attributeChanged = QtCore.Signal(str, dict)

    def __init__(self, parent=None, style=None):
        QtGui.QWidget.__init__(self, parent=parent)
        if style is None:
            style = self.DEFAULT_STYLE
        self.style = style

        self._manager = {}

        self._cb_matrix_name = QtGui.QComboBox()
        p = QtGui.QSizePolicy
        self._cb_matrix_name.setSizePolicy(p(p.Expanding, p.Maximum))
        self._cb_matrix_name.currentIndexChanged.connect(
            self._matrix_name_changed)

        self._viewer = None
        self._current = None
        self._old_color = None
        self._default_manager = self._create_manager()

        self.interpreter = get_interpreter()
        self.interpreter.locals['viewer_control'] = self

        if self.style == self.StylePanel:
            from openalea.oalab.service.qt_control import edit
            self._view = edit(self._default_manager)
            self._qt_control = {}
            for control, editor in self._view.editor.items():
                self._qt_control[control.name] = editor
        else:
            self._view = ControlManagerWidget(manager=self._default_manager)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self._cb_matrix_name)
        self._layout.addWidget(self._view)

    def __getitem__(self, key):
        return self._manager[self._current].control(name=key)

    def _create_manager(self, viewer=None, matrix_name=None):
        from openalea.core.control.manager import ControlContainer
        manager = ControlContainer()
        for i, data in enumerate([
            ('x', self._x_slider_changed),
            ('y', self._y_slider_changed),
            ('z', self._z_slider_changed),
        ]):
            name, func = data
            c = manager.add(
                name, interface='IInt', value=1, alias='Move %s plane' % name)
            c.interface.min = 0
            c.interface.max = 100

        cut_planes = manager.add(
            'cut_planes', interface='IBool', value=True, alias='Display cut plane')
        volume = manager.add(
            'volume', interface='IBool', value=True, alias='Display volume')

        alpha = manager.add(
            'cut_planes_alpha', interface='IFloat', value=1, alias=u'Cut planes α')
        alpha.interface.step = 0.1
        alpha.interface.min = 0
        alpha.interface.max = 1

        alpha = manager.add(
            'volume_alpha', interface='IFloat', value=1, alias=u'Volume α')
        alpha.interface.step = 0.1
        alpha.interface.min = 0
        alpha.interface.max = 1

        alphamap = manager.add('volume_alphamap_type', interface='IEnumStr', value='constant',
                               alias=u'Volume α map')
        alphamap.interface.enum = ['constant', 'linear']

        # lut = manager.add(
        #     'lookuptable', interface='IEnumStr', value='grey', alias=u'Lookup table')
        # if viewer is not None:
        #     colormap_names = viewer.vtk.colormaps.keys()
        #     colormap_names.sort()
        #     lut.interface.enum = colormap_names
        # else:
        #     from openalea.oalab.colormap.colormap_def import colormap_names
        #     lut.interface.enum = colormap_names

        cmap = manager.add('colormap', interface='IColormap', value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), alias=u'Colormap')

        intensity_range = manager.add(
            'intensity_range', interface='IIntRange', value=(0, 255), alias=u'Intensity range')
        intensity_range.interface.min = 0
        intensity_range.interface.max = 255

        bg_id = manager.add(
            'bg_id', interface='IInt', value=1, alias=u'Background Id')
        #selected_id = manager.add('selected_id', interface='IInt', value=2, alias=u'Color cell')

        if viewer and matrix_name:
            disp = True
            for actor_name in viewer.vtk.actor:
                if actor_name.startswith('%s_cut_plane_' % matrix_name):
                    disp = viewer.vtk.property[actor_name]['disp']
                    break

            volume.value = viewer.vtk.volume_property[matrix_name]['disp']
            cut_planes.value = disp

            data_matrix = viewer.vtk.matrix[matrix_name]

            for orientation in (0, 1, 2):
                c_id = list('xyz')[orientation]
                c = manager.control(name=c_id)
                c.interface.min = 0
                c.interface.max = data_matrix.shape[orientation]
                c.value = c.interface.max / 2

            for c in [bg_id]:
                c.interface.min = data_matrix.min()
                c.interface.max = data_matrix.max()

            for c in [intensity_range]:
                c.value = (data_matrix.min(), data_matrix.max())
                c.interface.min = data_matrix.min()
                c.interface.max = data_matrix.max()

        return manager

    def _connect_manager(self, manager):
        manager.register_follower('volume', self._display_volume_changed)
        manager.register_follower(
            'cut_planes', self._display_cut_planes_changed)
        manager.register_follower(
            'cut_planes_alpha', self._cut_planes_alpha_changed)
        manager.register_follower('volume_alpha', self._volume_alpha_changed)
        manager.register_follower(
            'volume_alphamap_type', self._volume_alphamap_changed)
        # manager.register_follower('lookuptable', self._lookuptable_changed)
        manager.register_follower('colormap', self._colormap_changed)
        manager.register_follower('bg_id', self._bg_id_changed)
        #manager.register_follower('selected_id', self._selected_id_changed)
        manager.register_follower('intensity_range', self._intensity_range_changed)

        for data in [
            ('x', self._x_slider_changed),
            ('y', self._y_slider_changed),
            ('z', self._z_slider_changed),
        ]:
            name, func = data
            manager.register_follower(name, func)

    def set_viewer(self, viewer):
        self._viewer = viewer

    def clear(self):
        self._cb_matrix_name.clear()
        self._manager.clear()

    def set_matrix(self, name):
        viewer = self.sender()
        if viewer is None:
            return
        self.set_viewer(viewer.vtk)

        if not isinstance(name, basestring):
            raise NotImplementedError

        if name not in self._manager:
            manager = self._create_manager(viewer, name)
            self._manager[name] = manager
            self._connect_manager(manager)
            self._cb_matrix_name.addItem(name)

    def _matrix_name_changed(self, idx):
        if idx != -1:
            self.select_matrix(self._cb_matrix_name.itemText(idx))

    def _set_manager(self, manager):
        if self.style == self.StylePanel:
            for c_id, weakref in self._qt_control.items():
                control = manager.control(name=c_id)
                editor = weakref()
                if editor and control:
                    editor.set(control)
        else:
            self._view.model.set_manager(manager)

    def select_matrix(self, name):
        if name != self._current:
            # Update matrix name
            self._current = name
            manager = self._manager[name]
            manager.disable_followers()
            self._set_manager(manager)
            manager.enable_followers()

    def _selected_id_changed(self, old, new):
        # restore old cell original color
        if self._old_color:
            self._viewer.color_cell(self._current, old, self._old_color)
        # save current color and color in red
        self._old_color = self._viewer.cell_color(self._current, new)
        self._viewer.color_cell(self._current, new, (1., 0., 0.))

    def _bg_id_changed(self, old, new):
        self._volume_alpha_changed(None, self['volume_alpha'].value)

    def _intensity_range_changed(self, old, new):
        # lookuptable = self['lookuptable'].value
        colormap = self['colormap'].value
        alpha = self['volume_alpha'].value
        alphamap = self['volume_alphamap_type'].value
        bg_id = self['bg_id'].value
        self._viewer.set_matrix_lookuptable(self._current, colormap=colormap['name'], i_min=new[0], i_max=new[1])
        self._viewer.set_volume_alpha(
            self._current, alpha=alpha, alphamap=alphamap, bg_id=bg_id, i_min=new[0], i_max=new[1])

    def _cut_planes_alpha_changed(self, old, new):
        self._viewer.set_cut_planes_alpha(self._current, alpha=new)

    def _volume_alpha_changed(self, old, new):
        alphamap = self['volume_alphamap_type'].value
        i_range = self['intensity_range'].value
        bg_id = self['bg_id'].value
        self._viewer.set_volume_alpha(
            self._current, alpha=new, alphamap=alphamap, bg_id=bg_id, i_min=i_range[0], i_max=i_range[1])

    # def _lookuptable_changed(self, old, new):
    #     i_range = self['intensity_range'].value
    #     self._viewer.set_matrix_lookuptable(self._current, colormap=new, i_min=i_range [0], i_max=i_range[1])

    def _colormap_changed(self, old, new):
        i_range = self['intensity_range'].value
        self._viewer.set_matrix_lookuptable(self._current, colormap=new['name'], i_min=i_range[0], i_max=i_range[1])

    def _volume_alphamap_changed(self, old, new):
        self._volume_alpha_changed(None, self['volume_alpha'].value)

    def _display_cut_planes_changed(self, old, new):
        self._viewer.display_cut_planes(name=self._current, disp=new)

    def _display_volume_changed(self, old, new):
        self._viewer.display_volume(name=self._current, disp=new)

    def _x_slider_changed(self, old, new):
        self._viewer.move_cut_plane(
            name=self._current, position=new, orientation=1)

    def _y_slider_changed(self, old, new):
        self._viewer.move_cut_plane(
            name=self._current, position=new, orientation=2)

    def _z_slider_changed(self, old, new):
        self._viewer.move_cut_plane(
            name=self._current, position=new, orientation=3)
