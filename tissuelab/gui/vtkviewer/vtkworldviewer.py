# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Bâty <guillaume.baty@inria.fr>
#       File contributor(s): Guillaume Bâty <guillaume.baty@inria.fr>
#                            Alizon König <alizon.konig@inria.fr>
#                            Guillaume Cerutti <guillaume.cerutti@inria.fr>
#                            Pierre Fernique <pierre.fernique@inria.fr>
#                            Sophie Ribes <sophie.ribes@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

import vtk
import numpy as np
from scipy import ndimage as nd

from openalea.core.observer import AbstractListener
from openalea.core.world import World
from openalea.vpltk.qt import QtGui


from tissuelab.gui.vtkviewer.vtk_utils import define_lookuptable
from tissuelab.gui.vtkviewer.vtkviewer import VtkViewer, attribute_args, attribute_definition, colormaps


class ImageBlending(object):

    def __init__(self, world_objects):
        self.world_objects = world_objects
        self.data_matrices = [world_object.data for world_object in world_objects]

        self.shape = world_objects[0].data.shape
        self.resolution = world_objects[0].data.resolution


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


def attribute_value(world_object, dtype, attr_name, **kwargs):
    """
    Return a value for attr_name. Try to get value in this order:
        1. kwargs
        2. world object
        3. viewer's default
    """
    if isinstance(attr_name, basestring):
        attr_names = [attr_name]
    else:
        attr_names = attr_name
    for attr_name in attr_names:
        if attr_name in kwargs:
            return kwargs[attr_name]
    else:
        return world_object.get(attr_name, attribute_definition[dtype][attr_name]['value'])


def setdefault(world_object, dtype, attr_name, obj_attr_name=None, conv=None, **kwargs):
    if obj_attr_name is None:
        obj_attr_name = attr_name
    if isinstance(attr_name, basestring):
        attr_names = [attr_name]
    else:
        attr_names = attr_name
    if obj_attr_name != attr_name:
        attr_names.insert(0, obj_attr_name)

    #Try to get value in this order:
    #    1. kwargs
    value = None
    for attr_name in attr_names:
        if attr_name in kwargs:
            value = kwargs[attr_name]
            break

    #    2. world object
    if value is None:
        value = world_object.get(attr_name, None)

    # If a conversion has been defined, apply it
    attribute = None
    if conv:
        attribute = conv(world_object, obj_attr_name, value, **kwargs)

    if attribute is None:
        attribute = dict(value=value)

    value = attribute['value']

    # If value is still None after conversion, use viewer's default
    if value is None:
        for attr_name in attr_names:
            if attr_name in attribute_definition[dtype]:
                value = attribute_definition[dtype][attr_name]['value']
                attribute['value'] = value
                break

    # Set as attribute
    world_object.set_attribute(**attribute_args(dtype, obj_attr_name, **attribute))

    # And clear from kwargs
    world_object.kwargs.pop(obj_attr_name, None)
    return value


def world_kwargs(world_object):
    kwargs = {}
    for attribute in world_object.attributes:
        kwargs[attribute['name']] = attribute['value']
    return kwargs


def _tuple(world_object, attr_name, value, **kwargs):
    if value is not None:
        return dict(value=tuple(value))


def _colormap(world_object, attr_name, cmap, **kwargs):
    if isinstance(cmap, str):
        cmap = dict(name=cmap, color_points=colormaps[cmap]._color_points)

    return dict(value=cmap)


def _irange(world_object, attr_name, irange, **kwargs):
    try:
        object_min = world_object.data.min()
        object_max = world_object.data.max()
    except AttributeError:
        if irange is None:
            i_min = kwargs.get('i_min', None)
            i_max = kwargs.get('i_max', None)
            irange = (i_min, i_max) if (i_min is not None) and (i_max is not None) else None
        constraints = None
    else:
        if irange is None:
            i_min = kwargs.get('i_min', object_min)
            i_max = kwargs.get('i_max', object_max)
            irange = (i_min, i_max)
        constraints = dict(min=object_min, max=object_max)

    return dict(value=irange, constraints=constraints)


def _plane_position(world_object, attr_name, plane_position, **kwargs):
    lst = list('xyz')
    i = lst.index(attr_name[0])
    if plane_position is None:
        plane_position = (world_object.data.shape[i] - 1) / 2

    constraints = dict(min=0, max=world_object.data.shape[i] - 1)

    return dict(value=plane_position, constraints=constraints)


def _bg_id(world_object, attr_name, value, **kwargs):
    attribute = _irange(world_object, attr_name, value)
    if value is None:
        value = 1
    attribute['value'] = value
    return attribute


class VtkWorldViewer(VtkViewer, AbstractListener):

    """
    Class able to listen events of world and world objects and update scene depending on it.
    Ths class is based on VtkViewer that provide pure vtk methods.
    """

    def __init__(self):
        VtkViewer.__init__(self)
        AbstractListener.__init__(self)

        self.world = World()
        self.world.register_listener(self)
        self.setAcceptDrops(True)

        self._first_object = True

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.set_world(data)
        elif signal == 'world_object_removed':
            world, old = data
            self.remove_world_object(world, old)
        elif signal == 'world_object_changed':
            world, old, new = data
            self.set_world_object(world, new)
        elif signal == 'world_object_item_changed':
            world, obj, item, old, new = data
            if item == 'attribute':
                self.update_world_object(world, obj, new)

    def set_world(self, world):
        self.clear()
        self._first_object = True
        for obj_name, world_object in world.items():
            self.set_world_object(world, world_object, compute=False)
            # if hasattr(world_object, "transform"):
            #     object_data = world_object.transform()
            # elif hasattr(world_object, "_repr_vtk_"):
            #     object_data = world_object._repr_vtk_()
            # elif hasattr(world_object.data, "_repr_vtk_"):
            #     object_data = world_object.data._repr_vtk_()
            # else:
            #     object_data = world_object.data

            # if isinstance(object_data, np.ndarray):
            #     self.add_matrix(world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
            # elif isinstance(object_data, vtk.vtkPolyData):
            #     self.add_polydata(world_object, object_data, **world_object.kwargs)
            # elif isinstance(object_data, vtk.vtkActor):
            #     self.add_actor(obj_name, object_data, **world_object.kwargs)
        self.compute(autofocus=True)

    def set_world_object(self, world, world_object, compute=True):
        """
        Add a world object in the viewer's scene
        """

        # Convert the world object data into its VTK representation
        object_name = world_object.name
        if hasattr(world_object, "transform"):
            object_data = world_object.transform()
        elif hasattr(world_object, "_repr_vtk_"):
            object_data = world_object._repr_vtk_()
        elif hasattr(world_object.data, "_repr_vtk_"):
            object_data = world_object.data._repr_vtk_()
        else:
            object_data = world_object.data
        self.object_repr[object_name] = object_data

        if isinstance(object_data, np.ndarray):
            if hasattr(object_data, 'resolution') and 'resolution' not in world_object.kwargs:
                world_object.kwargs['resolution'] = object_data.resolution
            self.add_matrix(world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
        elif isinstance(object_data, vtk.vtkPolyData):
            self.add_polydata(world_object, object_data, **world_object.kwargs)
        elif isinstance(object_data, ImageBlending):
            self.add_blending(world_object, object_data, **world_object.kwargs)
        elif isinstance(object_data, vtk.vtkActor):
            self.add_actor(object_name, object_data, **world_object.kwargs)
        if compute is True:
            self.compute(autofocus=self._first_object)
            self._first_object = False

    def remove_world_object(self, world, world_object):
        """
        Remove a world object from the viewer's scene
        """
        object_name = world_object.name
        if object_name in self.object_repr:
            object_data = self.object_repr[object_name]
        if isinstance(object_data, np.ndarray):
            self.remove_matrix(object_name)
        elif isinstance(object_data, vtk.vtkPolyData):
            self.remove_polydata(object_name)
        elif isinstance(object_data, ImageBlending):
            self.remove_blending(object_name)
        elif isinstance(object_data, vtk.vtkActor):
            self.remove_actor(object_name)
        self.compute()
        if len(world) == 0:
            self._first_object = True

    def update_world_object(self, world, world_object, attribute):
        object_name = world_object.name
        if object_name in self.object_repr:
            object_data = self.object_repr[object_name]
            if isinstance(object_data, np.ndarray):
                dtype = 'matrix'
                colormap = attribute_value(world_object, dtype, 'matrix_colormap')
                alpha = attribute_value(world_object, dtype, 'volume_alpha')
                alphamap = attribute_value(world_object, dtype, 'alphamap')
                bg_id = attribute_value(world_object, dtype, 'bg_id')
                irange = attribute_value(world_object, dtype, 'intensity_range')
                if attribute['name'] == 'volume':
                    self.display_volume(name=world_object.name, disp=attribute['value'])
                elif attribute['name'] == 'matrix_colormap':
                    self.set_matrix_lookuptable(
                        world_object.name,
                        colormap=attribute['value'],
                        intensity_range=irange
                    )
                elif attribute['name'] == 'alphamap':
                    self.set_volume_alpha(
                        world_object.name,
                        alpha=alpha,
                        alphamap=attribute['value'],
                        intensity_range=irange,
                        bg_id=bg_id)
                elif attribute['name'] == 'volume_alpha':
                    self.set_volume_alpha(
                        world_object.name,
                        alpha=attribute['value'],
                        alphamap=alphamap,
                        intensity_range=irange,
                        bg_id=bg_id)
                elif attribute['name'] == 'intensity_range':
                    self.set_matrix_lookuptable(
                        world_object.name,
                        colormap=colormap,
                        intensity_range=attribute['value']
                    )
                    self.set_volume_alpha(
                        world_object.name,
                        alpha=alpha,
                        alphamap=alphamap,
                        intensity_range=attribute['value'],
                        bg_id=bg_id)
                elif attribute['name'] == 'cut_planes':
                    self.display_cut_planes(name=world_object.name, disp=attribute['value'])
                elif attribute['name'] == 'cut_planes_alpha':
                    self.set_cut_planes_alpha(world_object.name, alpha=attribute['value'])
                elif attribute['name'] == 'bg_id':
                    self.set_volume_alpha(
                        world_object.name,
                        alpha=alpha,
                        alphamap=alphamap,
                        intensity_range=irange,
                        bg_id=bg_id)
                    self.set_cut_planes_alpha(world_object.name, alpha=attribute['value'])
                else:
                    for i, axis in enumerate(['x', 'y', 'z']):
                        if attribute['name'] == axis + '_plane_position':
                            self.move_cut_plane(name=world_object.name, position=attribute['value'], orientation=i + 1)
            elif isinstance(object_data, vtk.vtkPolyData):
                dtype = 'polydata'
                alpha = attribute_value(world_object, dtype, 'polydata_alpha')
                colormap = attribute_value(world_object, dtype, 'polydata_colormap')
                irange = attribute_value(world_object, dtype, 'intensity_range')
                linewidth = attribute_value(world_object, dtype, 'linewidth')
                point_radius = attribute_value(world_object, dtype, 'point_radius')
                preserve_faces = attribute_value(world_object, dtype, 'preserve_faces')
                x_slice = attribute_value(world_object, dtype, 'x_slice')
                y_slice = attribute_value(world_object, dtype, 'y_slice')
                z_slice = attribute_value(world_object, dtype, 'z_slice')
                if attribute['name'] == 'display_polydata':
                    self.display_polydata(name=world_object.name, disp=attribute['value'])
                elif attribute['name'] == 'linewidth':
                    self.set_polydata_linewidth(world_object.name, linewidth=attribute['value'])
                elif attribute['name'] == 'point_radius':
                    self.set_polydata_point_radius(world_object.name, point_radius=attribute['value'])
                elif attribute['name'] == 'polydata_colormap':
                    self.set_polydata_lookuptable(world_object.name, colormap=attribute['value'], alpha=alpha,
                                                  intensity_range=irange)
                elif attribute['name'] == 'polydata_alpha':
                    self.set_polydata_alpha(world_object.name, alpha=attribute['value'])
                elif attribute['name'] == 'intensity_range':
                    self.set_polydata_lookuptable(world_object.name, colormap=colormap, alpha=alpha,
                                                  intensity_range=attribute['value'])
                elif attribute['name'] == 'x_slice':
                    self.slice_polydata(
                        name=world_object.name,
                        x_slice=attribute['value'],
                        y_slice=y_slice,
                        z_slice=z_slice,
                        preserve_faces=preserve_faces,
                        point_radius=point_radius)
                elif attribute['name'] == 'y_slice':
                    self.slice_polydata(
                        name=world_object.name,
                        x_slice=x_slice,
                        y_slice=attribute['value'],
                        z_slice=z_slice,
                        preserve_faces=preserve_faces,
                        point_radius=point_radius)
                elif attribute['name'] == 'z_slice':
                    self.slice_polydata(
                        name=world_object.name,
                        x_slice=x_slice,
                        y_slice=y_slice,
                        z_slice=attribute['value'],
                        preserve_faces=preserve_faces,
                        point_radius=point_radius)
                elif attribute['name'] == 'preserve_faces':
                    self.slice_polydata(
                        name=world_object.name,
                        x_slice=x_slice,
                        y_slice=y_slice,
                        z_slice=z_slice,
                        preserve_faces=attribute['value'],
                        point_radius=point_radius)

            elif isinstance(object_data, ImageBlending):
                if attribute['name'] == 'blending_factor':
                    self.set_blending_factor(world_object.name, blending_factor=attribute['value'])
                elif attribute['name'] == 'cut_planes_alpha':
                    self.set_cut_planes_alpha(world_object.name, alpha=attribute['value'])
                elif attribute['name'] == 'cut_planes':
                    self.display_cut_planes(name=world_object.name, disp=attribute['value'])
                else:
                    for i, axis in enumerate(['x', 'y', 'z']):
                        if attribute['name'] == axis + '_plane_position':
                            self.move_cut_plane(name=world_object.name, position=attribute['value'], orientation=i + 1)
        self.render()

    def add_polydata(self, world_object, polydata, **kwargs):
        world_object.silent = True

        dtype = 'polydata'

        setdefault(world_object, dtype, 'colormap', 'polydata_colormap', conv=_colormap, **kwargs)
        setdefault(world_object, dtype, 'alpha', 'polydata_alpha', **kwargs)
        setdefault(world_object, dtype, 'intensity_range', conv=_irange, **kwargs)
        setdefault(world_object, dtype, 'position', conv=_tuple, **kwargs)
        setdefault(world_object, dtype, 'resolution', conv=_tuple, **kwargs)
        setdefault(world_object, dtype, 'linewidth', **kwargs)
        setdefault(world_object, dtype, 'point_radius', **kwargs)

        obj_kwargs = world_kwargs(world_object)
        super(VtkWorldViewer, self).add_polydata(world_object.name, polydata, **obj_kwargs)

        world_object.silent = False
        setdefault(world_object, dtype, 'display_polydata', **kwargs)

        world_object.silent = True
        for axis in ['x', 'y', 'z']:
            attr_name = axis + '_slice'
            setdefault(world_object, dtype, attr_name, **kwargs)
        world_object.silent = False

        setdefault(world_object, dtype, 'preserve_faces', **kwargs)

    def set_polydata_property(self, name, property=None, **kwargs):
        cmap = kwargs.get('colormap', 'grey')
        i_min = kwargs.get('i_min', None)
        i_max = kwargs.get('i_max', None)

        n_triangles = self.actor[name + '_polydata'].GetMapper().GetInput().GetPolys().GetNumberOfCells()

        vtk_property = vtk.vtkLongArray()
        if property is None:
            for t in xrange(n_triangles):
                vtk_property.InsertValue(t, t)
            # lut = define_lookuptable(np.arange(n_triangles), colormap=self.colormaps[cmap])
            lut = define_lookuptable(
                np.arange(n_triangles),
                colormap_points=self.colormaps[cmap]._color_points,
                colormap_name=cmap)
        else:
            assert len(property.keys()) == n_triangles
            for (fid, t) in zip(property.keys(), xrange(n_triangles)):
                vtk_property.InsertValue(t, property[fid])

            # lut = define_lookuptable(np.array(property.values()),
            # colormap=self.colormaps[cmap], i_min=i_min, i_max=i_max)
            lut = define_lookuptable(np.array(property.values()),
                                     colormap_points=self.colormaps[cmap]._color_points,
                                     colormap_name=cmap,
                                     i_min=i_min, i_max=i_max)

        self.actor[name + '_polydata'].GetMapper().GetInput().GetCellData().SetScalars(vtk_property)
        self.actor[name + '_polydata'].GetMapper().SetLookupTable(lut)
        alpha = kwargs.get('alpha', self.actor[name + '_polydata'].GetProperty().GetOpacity())
        self.actor[name + '_polydata'].GetProperty().SetOpacity(alpha)

    def add_matrix(self, world_object, data_matrix, datatype=np.uint8, decimate=1, **kwargs):
        world_object.silent = True

        name = world_object.name
        dtype = 'matrix'
        data_matrix = world_object.data
        shade = kwargs.get('shade')
        erosion = kwargs.get('erosion')

        if shade and not erosion:
            data_matrix = np.copy(data_matrix)
            sh_id = kwargs.get('sh_id', 0)
            bg_id = kwargs.get('bg_id', attribute_value(world_object, dtype, 'bg_id'))
            structure = kwargs.get('structure', np.ones((3, 3, 3)))
            tmp = data_matrix != bg_id
            mask = nd.binary_dilation(tmp, structure=structure)
            data_matrix[tmp ^ mask] = sh_id
        if erosion:
            data_matrix = np.copy(data_matrix)
            if not shade:
                sh_id = None
            else:
                sh_id = kwargs.get('sh_id', 0)
            bg_id = kwargs.get('bg_id', attribute_value(world_object, dtype, 'bg_id'))
            if sh_id is None:
                er_id = bg_id
            else:
                er_id = sh_id
            boundary_boxes = nd.find_objects(data_matrix)
            structure = kwargs.get('structure', np.ones((3, 3, 3)))
            for i in np.unique(data_matrix):
                if not i in [sh_id, bg_id]:
                    tmp = data_matrix[boundary_boxes[i - 1]] == i
                    mask = nd.binary_erosion(tmp, structure=structure)
                    data_matrix[boundary_boxes[i - 1]][tmp ^ mask] = er_id
        self.matrix[name] = data_matrix

        self.add_matrix_as_volume(
            world_object, data_matrix, datatype, decimate, **kwargs)
        world_object.silent = False

        setdefault(world_object, dtype, 'volume', **kwargs)

        world_object.silent = True
        self.add_matrix_cut_planes(
            world_object, data_matrix, datatype, decimate, **kwargs)
        world_object.silent = False

        setdefault(world_object, dtype, 'cut_planes', **kwargs)

        # self._display_volume(name, display_volume)
        # self._display_cut_planes(name, display_cut_planes)

    def add_matrix_cut_planes(self, world_object, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        name = world_object.name
        dtype = "matrix"

        setdefault(world_object, dtype, 'alpha', 'cut_planes_alpha', **kwargs)

        for axis in ['x', 'y', 'z']:
            attr_name = axis + '_plane_position'
            setdefault(world_object, dtype, attr_name, conv=_plane_position, **kwargs)

        kwargs = world_kwargs(world_object)
        super(VtkWorldViewer, self).add_matrix_cut_planes(name, data_matrix, datatype=datatype, **kwargs)

    def add_matrix_as_volume(self, world_object, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        dtype = 'matrix'

        setdefault(world_object, dtype, 'colormap', 'matrix_colormap', conv=_colormap, **kwargs)
        setdefault(world_object, dtype, 'alpha', 'volume_alpha', **kwargs)
        setdefault(world_object, dtype, 'alphamap', **kwargs)
        setdefault(world_object, dtype, 'intensity_range', conv=_irange, **kwargs)
        setdefault(world_object, dtype, 'position', conv=_tuple, **kwargs)
        setdefault(world_object, dtype, 'resolution', conv=_tuple, **kwargs)
        setdefault(world_object, dtype, 'bg_id', conv=_bg_id, **kwargs)
        kwargs = world_kwargs(world_object)
        super(VtkWorldViewer, self).add_matrix_as_volume(world_object.name, data_matrix,
                                                         datatype=datatype, decimate=1,
                                                         **kwargs)

    def add_blending(self, world_object, image_blending, **kwargs):
        from .vtk_utils import blend_funct

        # dtype = 'blending'
        dtype = 'matrix'

        blended_objects = image_blending.world_objects
        data_matrices = image_blending.data_matrices

        names = [obj.name for obj in blended_objects]

        world_object.silent = True

        setdefault(world_object, dtype, 'blending_factor', **kwargs)
        setdefault(world_object, dtype, 'alpha', 'cut_planes_alpha', **kwargs)

        obj_kwargs = world_kwargs(blended_objects[0])
        setdefault(world_object, dtype, 'position', conv=_tuple, **obj_kwargs)
        setdefault(world_object, dtype, 'resolution', conv=_tuple, **obj_kwargs)

        for axis in ['x', 'y', 'z']:
            attr_name = axis + '_plane_position'
            setdefault(world_object, dtype, attr_name, conv=_plane_position, **obj_kwargs)

        obj_kwargs = world_kwargs(world_object)
        super(VtkWorldViewer, self).add_blending(world_object.name, names, data_matrices, **obj_kwargs)
        world_object.silent = False

        setdefault(world_object, dtype, 'cut_planes', **kwargs)

    def dragEnterEvent(self, event):
        for fmt in ['text/uri-list', 'openalealab/data']:
            if event.mimeData().hasFormat(fmt):
                event.acceptProposedAction()
                return

        return QtGui.QWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        for fmt in ['text/uri-list', 'openalealab/data']:
            if event.mimeData().hasFormat(fmt):
                event.acceptProposedAction()
                return

        event.ignore()

    def dropEvent(self, event):
        source = event.mimeData()
        if source.hasFormat('text/uri-list'):
            from openalea.image.serial.basics import imread
            from openalea.core.path import path
            for url in source.urls():
                local_file = url.toLocalFile()
                local_file = path(local_file)
                if local_file.exists():
                    data = imread(local_file)
                    self.world.add(data, name=local_file.namebase)
                    event.acceptProposedAction()
                    self.auto_focus()
                else:
                    return QtGui.QWidget.dropEvent(self, event)

        elif source.hasFormat('openalealab/data'):
            from openalea.core.service.mimetype import decode
            data = decode('openalealab/data', source.data('openalealab/data'))
            from openalea.image.serial.basics import imread
            matrix = imread(data.path)
            self.world.add(matrix, name=data.path.namebase)
            self.auto_focus()
            event.acceptProposedAction()

        else:
            return QtGui.QWidget.dropEvent(self, event)
