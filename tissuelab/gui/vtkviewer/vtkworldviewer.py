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


from tissuelab.gui.vtkviewer.vtk_utils import define_lookuptable, matrix_to_image_reader
from tissuelab.gui.vtkviewer.vtkviewer import VtkViewer, attribute_args, attribute_definition, attribute_meta


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


def attribute_value(world_object, dtype, attr_name):
    return world_object.get(attr_name, attribute_definition[dtype][attr_name]['value'])


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
                self.add_matrix(
                    world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
                world_object.kwargs.pop('colormap', None)
                world_object.kwargs.pop('alpha', None)
                world_object.kwargs.pop('alphamap', None)
                world_object.kwargs.pop('resolution', None)
                world_object.kwargs.pop('volume', None)
                world_object.kwargs.pop('cut_planes', None)
            elif isinstance(object_data, vtk.vtkPolyData):
                self.add_polydata(world_object, object_data, **world_object.kwargs)
                world_object.kwargs.pop('position', None)
                world_object.kwargs.pop('colormap', None)
                world_object.kwargs.pop('alpha', None)
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
            self.add_matrix(
                world_object, object_data, datatype=object_data.dtype, **world_object.kwargs)
            world_object.kwargs.pop('colormap', None)
            world_object.kwargs.pop('alpha', None)
            world_object.kwargs.pop('alphamap', None)
            world_object.kwargs.pop('bg_id', None)
            world_object.kwargs.pop('resolution', None)
            world_object.kwargs.pop('volume', None)
            world_object.kwargs.pop('cut_planes', None)
        elif isinstance(object_data, vtk.vtkPolyData):
            self.add_polydata(world_object, object_data, **world_object.kwargs)
            world_object.kwargs.pop('position', None)
            world_object.kwargs.pop('colormap', None)
            world_object.kwargs.pop('alpha', None)
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
            i_range = attribute_value(world_object, dtype, 'intensity_range')
            if attribute['name'] == 'volume':
                self.display_volume(name=world_object.name, disp=attribute['value'])
            elif attribute['name'] == 'matrix_colormap':
                self.set_matrix_lookuptable(
                    world_object.name,
                    colormap=attribute['value'],
                    i_min=i_range[0],
                    i_max=i_range[1])
            elif attribute['name'] == 'alphamap':
                self.set_volume_alpha(
                    world_object.name,
                    alpha=alpha,
                    alphamap=attribute['value'],
                    i_min=i_range[0],
                    i_max=i_range[1],
                    bg_id=bg_id)
            elif attribute['name'] == 'volume_alpha':
                self.set_volume_alpha(
                    world_object.name,
                    alpha=attribute['value'],
                    alphamap=alphamap,
                    i_min=i_range[0],
                    i_max=i_range[1],
                    bg_id=bg_id)
            elif attribute['name'] == 'intensity_range':
                self.set_matrix_lookuptable(
                    world_object.name,
                    colormap=colormap,
                    i_min=attribute['value'][0],
                    i_max=attribute['value'][1])
                self.set_volume_alpha(
                    world_object.name,
                    alpha=alpha,
                    alphamap=alphamap,
                    i_min=attribute['value'][0],
                    i_max=attribute['value'][1],
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

        display_volume = kwargs.pop('volume', attribute_value(world_object, dtype, 'volume'))
        world_object.set_attribute(**attribute_args(dtype, 'volume', display_volume))

        world_object.silent = True

        self.add_matrix_cut_planes(
            world_object, data_matrix, datatype, decimate, **kwargs)

        world_object.silent = False

        display_cut_planes = kwargs.pop('cut_planes', attribute_value(world_object, dtype, 'cut_planes'))
        world_object.set_attribute(**attribute_args(dtype, 'cut_planes', display_cut_planes))

        # self._display_volume(name, display_volume)
        # self._display_cut_planes(name, display_cut_planes)

        print world_object.kwargs

    def add_matrix_cut_planes(self, world_object, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        name = world_object.name
        dtype = "matrix"
        alpha = kwargs.pop('alpha', attribute_value(world_object, dtype, 'cut_planes_alpha'))

        super(VtkWorldViewer, self).add_matrix_cut_planes(name, data_matrix, datatype=datatype, **kwargs)

        world_object.set_attribute(**attribute_args(dtype, 'cut_planes_alpha', alpha))
        for i, axis in enumerate(['x', 'y', 'z']):
            world_object.set_attribute(
                **attribute_args(dtype, axis + '_plane_position', (data_matrix.shape[i] - 1) / 2))

        world_object.set_attribute(**attribute_args(dtype, 'cut_planes_alpha', alpha))
        for i, axis in enumerate(['x', 'y', 'z']):
            world_object.set_attribute(
                **attribute_args(dtype, axis + '_plane_position', (data_matrix.shape[i] - 1) / 2))

    def add_matrix_as_volume(self, world_object, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        name = world_object.name
        dtype = 'matrix'
        self.reader[name] = reader = matrix_to_image_reader(
            name, data_matrix, datatype, decimate)

        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        volumeMapper = vtk.vtkVolumeRayCastMapper()
        volumeMapper.SetVolumeRayCastFunction(compositeFunction)
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        # colorFunc = vtk.vtkColorTransferFunction()
        colorFunc = vtk.vtkDiscretizableColorTransferFunction()
        alphaChannelFunc = vtk.vtkPiecewiseFunction()

        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(colorFunc)
        volume_property.SetScalarOpacity(alphaChannelFunc)
        self.volume_property[name] = dict(
            vtkVolumeProperty=volume_property, disp=True)

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volume_property)

        position = tuple(kwargs.pop('position', attribute_value(world_object, dtype, 'position')))

        if position is not None:
            volume.SetOrigin(position[0], position[1], position[2])
            volume.SetPosition(-position[0], -position[1], -position[2])

        resolution = tuple(kwargs.get('resolution', attribute_value(world_object, dtype, 'resolution')))
        volume.SetScale(resolution[0], resolution[1], resolution[2])

        if name in self.volume:
            old_volume = self.volume[name]
            self.ren.RemoveVolume(old_volume)
            del old_volume
        self.volume[name] = volume

        cmap = kwargs.pop('colormap', attribute_value(world_object, dtype, 'matrix_colormap'))
        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        alpha = kwargs.pop('alpha', attribute_value(world_object, dtype, 'volume_alpha'))
        alphamap = kwargs.pop('alphamap', attribute_value(world_object, dtype, 'alphamap'))
        bg_id = kwargs.pop('bg_id', attribute_value(world_object, dtype, 'bg_id'))

        i_min = kwargs.pop('i_min', world_object.get('intensity_range', (data_matrix.min(), 0))[0])
        i_max = kwargs.pop('i_max', world_object.get('intensity_range', (0, data_matrix.max()))[1])
        self.set_matrix_lookuptable(name, cmap, i_min=i_min, i_max=i_max, cut_planes=False)
        self.set_volume_alpha(name, alpha, alphamap, i_min=i_min, i_max=i_max, bg_id=bg_id)

        world_object.set_attribute(**attribute_args(dtype, 'matrix_colormap', cmap))
        world_object.set_attribute(**attribute_args(dtype, 'volume_alpha', alpha))
        world_object.set_attribute(**attribute_args(dtype, 'alphamap', alphamap))
        world_object.set_attribute(**attribute_args(dtype, 'intensity_range', (i_min, i_max)))
        world_object.set_attribute(**attribute_args(dtype, 'position', position))
        world_object.set_attribute(**attribute_args(dtype, 'resolution', resolution))
        world_object.set_attribute(**attribute_args(dtype, 'bg_id', bg_id))

    def set_volume_alpha(self, name, alpha=1.0, alphamap="constant", **kwargs):
        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()
        alphaChannelFunc.RemoveAllPoints()

        bg_id = kwargs.get('bg_id', None)
        sh_id = kwargs.get('sh_id', None)
        i_min = kwargs.get('i_min', self.matrix[name].min())
        i_max = kwargs.get('i_max', self.matrix[name].max())

        if alphamap == "constant":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, alpha)
            alphaChannelFunc.AddPoint(i_max, alpha)

            if bg_id is not None:
                if not bg_id - 1 == sh_id:
                    alphaChannelFunc.AddPoint(bg_id - 1, alpha)
                alphaChannelFunc.AddPoint(bg_id, 0.0)
                if not bg_id + 1 == sh_id:
                    alphaChannelFunc.AddPoint(bg_id + 1, alpha)

            if sh_id is not None:
                if not sh_id - 1 == bg_id:
                    alphaChannelFunc.AddPoint(sh_id - 1, alpha)
                alphaChannelFunc.AddPoint(sh_id, kwargs.get('shade_alpha', 0.1))
                if not sh_id + 1 == bg_id:
                    alphaChannelFunc.AddPoint(sh_id + 1, alpha)

        elif alphamap == "linear":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, 0.0)
            alphaChannelFunc.AddPoint(i_max, alpha)

    def set_matrix_lookuptable(self, name, colormap, **kwargs):
        i_min = kwargs.get('i_min', None)
        i_max = kwargs.get('i_max', None)
        cut_planes = kwargs.get('cut_planes', True)

        lut = define_lookuptable(self.matrix[name],
                                 colormap_points=colormap['color_points'],
                                 colormap_name=colormap['name'],
                                 i_min=i_min, i_max=i_max)
        if 'sh_id' in kwargs:
            lut.AddRGBPoint(kwargs['sh_id'], *kwargs.get('shade_color', (0., 0., 0.)))
        self.volume_property[name]['vtkVolumeProperty'].SetColor(lut)
        if cut_planes:
            for orientation in [1, 2, 3]:
                if name + "_cut_plane_colors_" + str(orientation) in self.vtkdata:
                    self.vtkdata[
                        name + "_cut_plane_colors_" + str(orientation)].SetLookupTable(lut)

    def cell_color(self, name, cell_id):
        colorFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetRGBTransferFunction()
        return colorFunc.GetColor(cell_id)

    def color_cell(self, name, cell_id=None, color=None, alpha=None):
        if color is None:
            color = (1., 1., 1.)
        if cell_id is None:
            cell_id = 1
        colorFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetRGBTransferFunction()
        colorFunc.RemoveAllPoints()
        colorFunc.AddRGBPoint(cell_id - 1, 1., 1., 1.)
        colorFunc.AddRGBPoint(cell_id, *color)
        colorFunc.AddRGBPoint(cell_id + 1, 1., 1., 1.)

    def old_color_cell(self, name, cell_id=None, color=None, alpha=None, bg_id=1, colormap='glasbey'):
        """
        TODO: replace with method that allows user to identify a cell
        """

        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()

        if alpha is None:
            alpha = 1.

        # colorFunc.AddRGBPoint(bg_id, 1.0, 1.0, 1.0)

        for matrix in self.matrix.values():

            if cell_id is None:
                # colorFunc.RemoveAllPoints()

                # self.volume_property[name]['vtkVolumeProperty'].SetColor(
                    # define_lookuptable(matrix, colormap=self.colormaps[colormap]))

                self.volume_property[name]['vtkVolumeProperty'].SetColor(
                    define_lookuptable(matrix, colormap_points=self.colormaps[colormap]._color_points, colormap_name=colormap))

                alphaChannelFunc.RemoveAllPoints()

                alphaChannelFunc.AddPoint(bg_id, 0.0)

                if colormap not in ['glasbey']:
                    alphaChannelFunc.RemoveAllPoints()
                    alphaChannelFunc.AddPoint(matrix.min(), 0.0)
                    alphaChannelFunc.AddPoint(matrix.max(), alpha)
                else:
                    # alphaChannelFunc.AddPoint(1, 0.0)
                    alphaChannelFunc.AddPoint(bg_id + 1, alpha)
                    alphaChannelFunc.AddPoint(matrix.max(), alpha)

            else:
                if color is None:
                    color = (1., 1., 1.)
                colorFunc = self.volume_property[name][
                    'vtkVolumeProperty'].GetRGBTransferFunction()
                colorFunc.AddRGBPoint(cell_id, *color)

                alphaChannelFunc.AddPoint(cell_id, alpha)
