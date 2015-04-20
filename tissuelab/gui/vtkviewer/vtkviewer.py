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
from openalea.vpltk.qt import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from tissuelab.gui.vtkviewer.colormap_def import load_colormaps


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


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
