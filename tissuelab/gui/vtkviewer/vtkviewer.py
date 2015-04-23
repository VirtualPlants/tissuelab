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

import copy
import numpy as np
import vtk


from openalea.vpltk.qt import QtGui
from openalea.core.interface import IBool, IInt, IFloat, ITuple, IEnumStr
from openalea.oalab.plugins.interface import IIntRange, IColormap
# Do not import world related module in this module, see vtkworldviewer instead!

from tissuelab.gui.vtkviewer.qvtkrenderwindowinteractor import QVTKRenderWindowInteractor
from tissuelab.gui.vtkviewer.colormap_def import load_colormaps
from tissuelab.gui.vtkviewer.vtk_utils import matrix_to_image_reader, define_lookuptable


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))

attribute_definition = {}
attribute_definition['matrix'] = {}
attribute_definition['matrix']['matrix_colormap'] = dict(
    value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), interface=IColormap, alias="Colormap")
attribute_definition['matrix']['volume_alpha'] = dict(value=1.0, interface=IFloat, alias=u"Alpha (Volume)")
attribute_definition['matrix']['alphamap'] = dict(value='linear', interface=IEnumStr, alias="Alpha Map")
attribute_definition['matrix']['bg_id'] = dict(value=1, interface=IInt, alias="Background Intensity")
attribute_definition['matrix']['intensity_range'] = dict(value=(0, 255), interface=IIntRange, alias="Intensity Range")
attribute_definition['matrix']['volume'] = dict(value=True, interface=IBool, alias="Display Volume")
attribute_definition['matrix']['cut_planes_alpha'] = dict(value=1.0, interface=IFloat, alias=u"Alpha (Cut planes)")
attribute_definition['matrix']['resolution'] = dict(value=(1.0, 1.0, 1.0), interface=ITuple, alias=u"Resolution")
attribute_definition['matrix']['position'] = dict(value=(0.0, 0.0, 0.0), interface=ITuple, alias=u"Position")
for axis in ['x', 'y', 'z']:
    alias = u"Move " + axis + " plane"
    attribute_definition['matrix'][axis + "_plane_position"] = dict(value=0, interface=IInt, alias=alias)
attribute_definition['matrix']['cut_planes'] = dict(value=False, interface=IBool, alias=u"Display Cut planes")
attribute_definition['polydata'] = {}
attribute_definition['polydata']['polydata_colormap'] = dict(
    value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), interface=IColormap, alias="Colormap")
attribute_definition['polydata']['polydata_alpha'] = dict(value=1.0, interface=IFloat, alias=u"Alpha (Polydata)")
attribute_definition['polydata']['position'] = dict(value=(0.0, 0.0, 0.0), interface=ITuple, alias=u"Position")
attribute_definition['polydata']['polydata'] = dict(value=True, interface=IBool, alias=u"Display Polydata")


colormaps = load_colormaps()


def attribute_meta(dtype, attr_name):
    return dict(interface=attribute_definition[dtype][attr_name]['interface'],
                alias=attribute_definition[dtype][attr_name]['alias'])


def attribute_args(dtype, attr_name, value=None):
    attribute = copy.deepcopy(attribute_definition[dtype][attr_name])
    attribute['name'] = attr_name
    if value is not None:
        attribute['value'] = value
    return attribute


def default_value(dtype, attr_name, **kwargs):
    """
    Returns attribute in kwargs if defined else viewer's default
    """
    if isinstance(attr_name, basestring):
        attr_names = [attr_name]
    else:
        attr_names = attr_name

    for attr_name in attr_names:
        if attr_name in kwargs:
            return kwargs[attr_name]

    for attr_name in attr_names:
        if attr_name in attribute_definition[dtype]:
            return attribute_definition[dtype][attr_name]['value']

    raise NotImplementedError(attr_name)


class VtkViewer(QtGui.QWidget):

    """
    Class providing a VtkViewer and convenience methods
      - to add actors, matrices (3d images), polydata,
      - to define and set colormaps
      - generate cut planes

    .. warning::

        Though this class can be embedded directly in a QWidget,
        it doesn't contain Qt features like buttons, toolbars or QAction.
        This class use only pure vtk features.

        For end-user features, please have a look to TissueViewer class.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.frame = QtGui.QFrame()
        self.vl = QtGui.QVBoxLayout(self.frame)
        self.vl.setContentsMargins(0, 0, 0, 0)

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        expand(self)
        expand(self.frame)
        expand(self.vtkWidget)

        self.ren = vtk.vtkRenderer()  # vtk renderer
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        #rajout picker
        self.picker = vtk.vtkPointPicker()
        self.picker.SetTolerance(0.005)
        self.iren.SetPicker(self.picker)
        #fin rajout

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

        self.colormaps = colormaps

        # vtk objects (like vtk volumes, vtk actors...) sorted by name in a
        # dictionnary
        self.object_repr = {}
        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.property = {}
        self.vtkdata = {}

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    ################################################
    # PURE VTK METHODS, NO MORE Qt AFTER THIS LINE #
    ################################################

    def display_volume(self, name=None, disp=True):
        self.clear_scene()
        self._display_volume(name, disp)
        self.compute()

    def display_cut_planes(self, name=None, disp=True):
        self.clear_scene()
        self._display_cut_planes(name, disp)
        self.compute()

    def display_polydata(self, name=None, disp=True):
        self.clear_scene()
        self._display_polydata(name, disp)
        self.compute()

    def _display_volume(self, name, disp=True):
        if name is None:
            for name in self.volume:
                self.volume_property[name]['disp'] = disp
        else:
            self.volume_property[name]['disp'] = disp

    def _display_cut_planes(self, name, disp=True):
        if name is None:
            for actor_name in self.actor:
                if '_cut_plane_' in actor_name:
                    self.property[actor_name]['disp'] = disp
        else:
            for actor_name in self.actor:
                if actor_name.startswith('%s_cut_plane_' % name):
                    self.property[actor_name]['disp'] = disp

    def _display_polydata(self, name, disp=True):
        if name is None:
            for actor_name in self.actor:
                if '_polydata' in actor_name:
                    self.property[actor_name]['disp'] = disp
        else:
            for actor_name in self.actor:
                if actor_name.startswith('%s_polydata' % name):
                    self.property[actor_name]['disp'] = disp

    def initialize(self):
        pass

    def clear_scene(self):
        for volume in self.volume.values():
            self.ren.RemoveVolume(volume)
        for actor in self.actor.values():
            self.ren.RemoveActor(actor)

    def clear(self):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
            del self.volume[name]
        for name, actor in self.actor.items():
            self.ren.RemoveActor(actor)
            del self.actor[name]

        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.vtkdata = {}

    def save_screenshot(self, filename):
        screenshooter = vtk.vtkWindowToImageFilter()
        screenshooter.SetInput(self.vtkWidget.GetRenderWindow())
        screenshooter.Update()
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename)
        writer.SetInput(screenshooter.GetOutput())
        writer.Write()

    def refresh(self):
        self.compute()

    def compute(self):
        for name, volume in self.volume.items():
            if self.volume_property[name]['disp']:
                self.ren.AddVolume(volume)
        for name, actor in self.actor.items():
            if self.property[name]['disp']:
                self.ren.AddActor(actor)

        self.iren.Initialize()
        self.iren.Start()
        self.render()

    def auto_focus(self):
        self.ren.ResetCamera()

    def render(self):
        self.iren.Render()

    def add_actor(self, name, actor, **kwargs):
        if name in self.actor:
            old_actor = self.actor[name]
            self.ren.RemoveActor(old_actor)
            del old_actor
        self.actor[name] = actor
        self.property[name] = dict(disp=True)

    def add_outline(self, name, data_matrix, **kwargs):
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, np.uint16, 1)
        nx, ny, nz = data_matrix.shape
        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(reader.GetOutputPort())
        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline.GetOutputPort())
        outline_actor = vtk.vtkActor()
        outline_actor.SetOrigin(nx / 2., ny / 2., nz / 2.)
        outline_actor.SetPosition(- nx / 2., -ny / 2., -nz / 2.)
        outline_actor.SetMapper(outline_mapper)
        outline_actor.GetProperty().SetColor(1, 1, 1)
        self.add_actor('%s_outline' % (name), outline_actor)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        """
        """
        if name in self.matrix:
            data_matrix = self.matrix[name]
        else:
            self.matrix[name] = data_matrix
        dtype = 'matrix'
        cmap = default_value(dtype, ['matrix_colormap', 'colormap'], **kwargs)
        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        resolution = default_value(dtype, 'resolution', **kwargs)
        position = default_value(dtype, 'position', **kwargs)
        alpha = default_value(dtype, 'cut_planes_alpha', **kwargs)

        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)

        # bwLut = define_lookuptable(data_matrix, colormap=self.colormaps["grey"])
        # colorLut = define_lookuptable(data_matrix, colormap=self.colormaps["glasbey"])
        # lut = define_lookuptable(data_matrix, colormap=self.colormaps[cmap])

        lut = define_lookuptable(data_matrix, colormap_points=cmap['color_points'], colormap_name=cmap['name'])

        for orientation in [1, 2, 3]:
            nx, ny, nz = data_matrix.shape
            xMax = nx - 1
            yMax = ny - 1
            zMax = nz - 1

            colors = vtk.vtkImageMapToColors()
            colors.SetInputConnection(reader.GetOutputPort())
            colors.SetLookupTable(lut)

            imgactor = vtk.vtkImageActor()
            imgactor.SetInput(colors.GetOutput())
            if orientation == 1:
                imgactor.SetDisplayExtent(
                    np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
            elif orientation == 2:
                imgactor.SetDisplayExtent(
                    0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
            elif orientation == 3:
                imgactor.SetDisplayExtent(
                    0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

            imgactor.SetScale(resolution[0], resolution[1], resolution[2])
            # imgactor, blend = blend_funct(data_matrix, reader, lut, reader, lut, orientation)
            # self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend

            if position is not None:
                imgactor.SetOrigin(position[0], position[1], position[2])
                imgactor.SetPosition(-position[0], -position[1], -position[2])

            self.reader[name] = reader = matrix_to_image_reader(
                name, data_matrix, datatype, decimate)

            self.vtkdata['%s_cut_plane_colors_%d' %
                         (name, orientation)] = colors
            self.add_actor('%s_cut_plane_%d' % (name, orientation), imgactor)

        self.set_cut_planes_alpha(name, alpha=alpha)
        return imgactor

    def add_matrix_as_volume(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        dtype = 'matrix'
        position = tuple(default_value(dtype, 'position', **kwargs))
        resolution = tuple(default_value(dtype, 'resolution', **kwargs))
        alpha = default_value(dtype, ['volume_alpha', 'alpha'], **kwargs)
        alphamap = default_value(dtype, 'alphamap', **kwargs)
        cmap = default_value(dtype, ['matrix_colormap', 'colormap'], **kwargs)
        bg_id = default_value(dtype, 'bg_id', **kwargs)

        irange = default_value(dtype, 'intensity_range', **kwargs)
        if irange == attribute_definition[dtype]['intensity_range']:
            irange = (data_matrix.min(), data_matrix.max())

        if name in self.matrix:
            data_matrix = self.matrix[name]
        else:
            self.matrix[name] = data_matrix

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

        if position is not None:
            volume.SetOrigin(position[0], position[1], position[2])
            volume.SetPosition(-position[0], -position[1], -position[2])

        if isinstance(cmap, str):
            cmap = dict(name=cmap, color_points=self.colormaps[cmap]._color_points)

        volume.SetScale(resolution[0], resolution[1], resolution[2])

        if name in self.volume:
            old_volume = self.volume[name]
            self.ren.RemoveVolume(old_volume)
            del old_volume
        self.volume[name] = volume

        self.set_matrix_lookuptable(name, cmap, intensity_range=irange, cut_planes=False)
        self.set_volume_alpha(name, alpha, alphamap, intensity_range=irange, bg_id=bg_id)

    def set_cut_planes_alpha(self, name, alpha):
        alpha = default_value('matrix', 'cut_planes_alpha', cut_planes_alpha=alpha)
        for orientation in [1, 2, 3]:
            self.actor[name + "_cut_plane_" + str(orientation)].SetOpacity(alpha)

    def set_volume_alpha(self, name, alpha=1.0, alphamap="constant", **kwargs):
        alphaChannelFunc = self.volume_property[name][
            'vtkVolumeProperty'].GetScalarOpacity()
        alphaChannelFunc.RemoveAllPoints()

        bg_id = kwargs.get('bg_id', None)
        sh_id = kwargs.get('sh_id', None)
        irange = kwargs.get('intensity_range', (self.matrix[name].min(), self.matrix[name].max()))

        if alphamap == "constant":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(irange[0], alpha)
            alphaChannelFunc.AddPoint(irange[1], alpha)

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
            alphaChannelFunc.AddPoint(irange[0], 0.0)
            alphaChannelFunc.AddPoint(irange[1], alpha)

    def set_matrix_lookuptable(self, name, colormap, **kwargs):
        irange = kwargs.pop('intensity_range', None)

        cut_planes = kwargs.get('cut_planes', True)

        lut = define_lookuptable(self.matrix[name],
                                 colormap_points=colormap['color_points'],
                                 colormap_name=colormap['name'],
                                 i_min=irange[0], i_max=irange[1])
        if 'sh_id' in kwargs:
            lut.AddRGBPoint(kwargs['sh_id'], *kwargs.get('shade_color', (0., 0., 0.)))
        self.volume_property[name]['vtkVolumeProperty'].SetColor(lut)
        if cut_planes:
            for orientation in [1, 2, 3]:
                if name + "_cut_plane_colors_" + str(orientation) in self.vtkdata:
                    self.vtkdata[
                        name + "_cut_plane_colors_" + str(orientation)].SetLookupTable(lut)

    def move_cut_plane(self, name, position=0, orientation=1):
        actor = self.actor['%s_cut_plane_%d' % (name, orientation)]
        data_matrix = self.matrix[name]
        nx, ny, nz = data_matrix.shape

        xMax = nx - 1
        yMax = ny - 1
        zMax = nz - 1
        bounds = [xMax, yMax, zMax]

        if position > bounds[orientation - 1]:
            position = bounds[orientation - 1]
        elif position < 0:
            position = 0

        if orientation == 1:
            actor.SetDisplayExtent(position, position, 0, yMax, 0, zMax)

        elif orientation == 2:
            actor.SetDisplayExtent(0, xMax, position, position, 0, zMax)

        elif orientation == 3:
            actor.SetDisplayExtent(0, xMax, 0, yMax, position, position)

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

    def setInteractor(self, interactor, **kwargs):
        self.iren.SetInteractorStyle(interactor)
        interactor.SetCurrentRenderer(self.ren)
