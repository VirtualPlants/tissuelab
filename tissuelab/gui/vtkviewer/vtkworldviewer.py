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
from openalea.oalab.world import World
from openalea.vpltk.qt import QtGui


from tissuelab.gui.vtkviewer.vtk_utils import define_lookuptable
from tissuelab.gui.vtkviewer.vtkviewer import VtkViewer, attribute_args, attribute_definition, colormaps


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
    if conv:
        value = conv(world_object, obj_attr_name, value, **kwargs)

    # If value is still None after conversion, use viewer's default
    if value is None:
        for attr_name in attr_names:
            if attr_name in attribute_definition[dtype]:
                value = attribute_definition[dtype][attr_name]['value']
                break

    # Set as attribute
    world_object.set_attribute(**attribute_args(dtype, obj_attr_name, value))

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
        return tuple(value)


def _colormap(world_object, attr_name, cmap, **kwargs):
    if isinstance(cmap, str):
        return dict(name=cmap, color_points=colormaps[cmap]._color_points)
    else:
        return cmap


def _irange(world_object, attr_name, irange, **kwargs):
    if irange is None:
        imin = kwargs.get('i_min', world_object.data.min())
        imax = kwargs.get('i_max', world_object.data.max())
        world_object.kwargs.pop('i_min', None)
        world_object.kwargs.pop('i_max', None)
        return (imin, imax)
    else:
        return irange


def _plane_position(world_object, attr_name, position, **kwargs):
    if position is None:
        lst = list('xyz')
        i = attr_name[0]
        return (world_object.data.shape[lst.index(i)] - 1) / 2
    else:
        return position


class VtkWorldViewer(VtkViewer, AbstractListener):

    def __init__(self):
        VtkViewer.__init__(self)
        AbstractListener.__init__(self)

        self.world = World()
        self.world.register_listener(self)

    def notify(self, sender, event=None):
        signal, data = event
        print "VtkViewer < ", signal, "!"
        if signal == 'world_sync':
            self.set_world(data)
        elif signal == 'world_object_changed':
            world, old, new = data
            self.set_world_object(world, new)
        elif signal == 'world_object_item_changed':
            world, obj, item, old, new = data
            if item == 'attribute':
                self.update_world_object(world, obj, new)

    def set_world(self, world):
        self.clear()
        for obj_name, world_object in world.items():
            if hasattr(world_object, "transform"):
                object_data = world_object.transform()
            elif hasattr(world_object, "_repr_vtk_"):
                object_data = world_object._repr_vtk_()
            else:
                object_data = world_object.data

            if isinstance(object_data, np.ndarray):
                self.add_matrix(world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
            elif isinstance(object_data, vtk.vtkPolyData):
                self.add_polydata(world_object, object_data, **world_object.kwargs)
            elif isinstance(object_data, vtk.vtkActor):
                self.add_actor(obj_name, object_data, **world_object.kwargs)
        self.compute()

    def set_world_object(self, world, world_object):
        """
        Add a world object in the viewer's scene
        """

        # Convert the world object data into its VTK representation
        object_name = world_object.name
        if hasattr(world_object, "transform"):
            object_data = world_object.transform()
        elif hasattr(world_object, "_repr_vtk_"):
            object_data = world_object._repr_vtk_()
        else:
            object_data = world_object.data
        self.object_repr[object_name] = object_data

        if isinstance(object_data, np.ndarray):
            self.add_matrix(world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
        elif isinstance(object_data, vtk.vtkPolyData):
            self.add_polydata(world_object, object_data, **world_object.kwargs)
        elif isinstance(object_data, vtk.vtkActor):
            self.add_actor(object_name, object_data, **world_object.kwargs)
        self.compute()

    def update_world_object(self, world, world_object, attribute):
        object_name = world_object.name
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
            else:
                for i, axis in enumerate(['x', 'y', 'z']):
                    if attribute['name'] == axis + '_plane_position':
                        self.move_cut_plane(name=world_object.name, position=attribute['value'], orientation=i + 1)
        elif isinstance(object_data, vtk.vtkPolyData):
            dtype = 'polydata'
            alpha = attribute_value(world_object, dtype, 'polydata_alpha')
            colormap = attribute_value(world_object, dtype, 'polydata_colormap')
            if attribute['name'] == 'polydata':
                self.display_polydata(name=world_object.name, disp=attribute['value'])
            elif attribute['name'] == 'polydata_colormap':
                self.set_polydata_lookuptable(world_object.name, colormap=attribute['value'], alpha=alpha)
            elif attribute['name'] == 'polydata_alpha':
                self.set_polydata_lookuptable(world_object.name, colormap=colormap, alpha=attribute['value'])

    def add_polydata(self, world_object, polydata, **kwargs):
        name = world_object.name
        dtype = 'polydata'
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polydata)
        else:
            mapper.SetInputData(polydata)

        polydata_actor = vtk.vtkActor()
        polydata_actor.SetMapper(mapper)
        polydata_actor.GetProperty().SetPointSize(1)

        position = tuple(kwargs.pop('position', attribute_value(world_object, dtype, 'position')))
        if position is not None:
            polydata_actor.SetOrigin(position[0], position[1], position[2])
            # imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)
            polydata_actor.SetPosition(-position[0], -position[1], -position[2])

        self.add_actor('%s_polydata' % (name), polydata_actor)

        # if (polydata.GetCellData().GetNumberOfComponents() > 0) or (polydata.GetPointData().GetNumberOfComponents() > 0):
        #     cmap = kwargs.get('colormap', 'glasbey')
        # else:
        cmap = kwargs.pop('colormap', attribute_value(world_object, dtype, 'polydata_colormap'))
        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)
        alpha = kwargs.pop('alpha', attribute_value(world_object, dtype, 'polydata_alpha'))

        self.set_polydata_lookuptable(name, colormap=cmap, alpha=alpha)

        world_object.set_attribute(**attribute_args(dtype, 'polydata_colormap', cmap))
        world_object.set_attribute(**attribute_args(dtype, 'polydata_alpha', alpha))
        world_object.set_attribute(**attribute_args(dtype, 'position', position))

        display_polydata = kwargs.pop('polydata', attribute_value(world_object, dtype, 'polydata'))
        world_object.set_attribute(**attribute_args(dtype, 'polydata', display_polydata))

    def set_polydata_lookuptable(self, name, colormap, **kwargs):

        if self.actor[name + '_polydata'].GetMapper().GetInput().GetCellData().GetNumberOfComponents() > 0:
            if isinstance(
                    self.actor[name + '_polydata'].GetMapper().GetInput().GetCellData().GetArray(0), vtk.vtkLongArray):
                cell_data = np.frombuffer(
                    self.actor[
                        name +
                        '_polydata'].GetMapper().GetInput().GetCellData().GetArray(0),
                    np.uint32)
            elif isinstance(self.actor[name + '_polydata'].GetMapper().GetInput().GetCellData().GetArray(0), vtk.vtkDoubleArray):
                cell_data = np.frombuffer(
                    self.actor[
                        name +
                        '_polydata'].GetMapper().GetInput().GetCellData().GetArray(0),
                    np.float64)
            lut = define_lookuptable(
                cell_data,
                colormap_points=colormap['color_points'],
                colormap_name=colormap['name'])
        elif self.actor[name + '_polydata'].GetMapper().GetInput().GetPointData().GetNumberOfComponents() > 0:
            if isinstance(
                    self.actor[name + '_polydata'].GetMapper().GetInput().GetPointData().GetArray(0), vtk.vtkLongArray):
                cell_data = np.frombuffer(
                    self.actor[
                        name +
                        '_polydata'].GetMapper().GetInput().GetPointData().GetArray(0),
                    np.uint32)
            if isinstance(
                    self.actor[name + '_polydata'].GetMapper().GetInput().GetPointData().GetArray(0), vtk.vtkDoubleArray):
                cell_data = np.frombuffer(
                    self.actor[
                        name +
                        '_polydata'].GetMapper().GetInput().GetPointData().GetArray(0),
                    np.float64)
            lut = define_lookuptable(
                cell_data,
                colormap_points=colormap['color_points'],
                colormap_name=colormap['name'])
        else:
            lut = define_lookuptable(
                np.arange(1),
                colormap_points=colormap['color_points'],
                colormap_name=colormap['name'],
                i_min=0,
                i_max=1)
        self.actor[name + '_polydata'].GetMapper().SetLookupTable(lut)

        alpha = kwargs.get('alpha', self.actor[name + '_polydata'].GetProperty().GetOpacity())
        self.actor[name + '_polydata'].GetProperty().SetOpacity(alpha)

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

            # lut = define_lookuptable(np.array(property.values()), colormap=self.colormaps[cmap], i_min=i_min, i_max=i_max)
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
        setdefault(world_object, dtype, 'bg_id', **kwargs)

        kwargs = world_kwargs(world_object)
        super(VtkWorldViewer, self).add_matrix_as_volume(world_object.name, data_matrix,
                                                         datatype=np.uint16, decimate=1,
                                                         **kwargs)
