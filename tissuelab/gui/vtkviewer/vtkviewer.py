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
    attribute_definition['matrix'][
        axis +
        "_plane_position"] = dict(
        value=0,
        interface=IInt,
        alias=u"Move " +
        axis +
        " plane")
attribute_definition['matrix']['cut_planes'] = dict(value=False, interface=IBool, alias=u"Display Cut planes")
attribute_definition['polydata'] = {}
attribute_definition['polydata']['polydata_colormap'] = dict(
    value=dict(name='grey', color_points=dict([(0, (0, 0, 0)), (1, (1, 1, 1))])), interface=IColormap, alias="Colormap")
attribute_definition['polydata']['polydata_alpha'] = dict(value=1.0, interface=IFloat, alias=u"Alpha (Polydata)")
attribute_definition['polydata']['position'] = dict(value=(0.0, 0.0, 0.0), interface=ITuple, alias=u"Position")
attribute_definition['polydata']['polydata'] = dict(value=True, interface=IBool, alias=u"Display Polydata")


def attribute_meta(dtype, attr_name):
    return dict(interface=attribute_definition[dtype][attr_name]['interface'],
                alias=attribute_definition[dtype][attr_name]['alias'])


def attribute_args(dtype, attr_name, value=None):
    attribute = copy.deepcopy(attribute_definition[dtype][attr_name])
    attribute['name'] = attr_name
    if value is not None:
        attribute['value'] = value
    return attribute


def default(dtype, attr_name, **kwargs):
    if attr_name in kwargs:
        return kwargs[attr_name]
    else:
        return attribute_definition[dtype][attr_name]['value']


class VtkViewer(QtGui.QWidget):

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

        self.colormaps = load_colormaps()

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
        cmap = kwargs.pop('colormap', 'grey')
        resolution = default(dtype, 'resolution', **kwargs)
        position = default(dtype, 'position', **kwargs)
        alpha = default(dtype, 'cut_planes_alpha', **kwargs)

        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)

        # bwLut = define_lookuptable(data_matrix, colormap=self.colormaps["grey"])
        # colorLut = define_lookuptable(data_matrix, colormap=self.colormaps["glasbey"])
        # lut = define_lookuptable(data_matrix, colormap=self.colormaps[cmap])

        lut = define_lookuptable(data_matrix, colormap_points=self.colormaps[cmap]._color_points, colormap_name=cmap)

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

    def set_cut_planes_alpha(self, name, alpha):
        alpha = default('matrix', 'cut_planes_alpha', cut_planes_alpha=alpha)
        for orientation in [1, 2, 3]:
            self.actor[name + "_cut_plane_" + str(orientation)].SetOpacity(alpha)

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

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)

    def setInteractor(self, interactor, **kwargs):
        self.iren.SetInteractorStyle(interactor)
        interactor.SetCurrentRenderer(self.ren)
