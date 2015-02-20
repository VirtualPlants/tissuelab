
import vtk
import numpy as np

from openalea.core.observer import AbstractListener
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.world import World
from openalea.core.service.ipython import interpreter as get_interpreter
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


def expand(widget):
    p = QtGui.QSizePolicy
    widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))


def define_lookuptable(image, colormap, i_min=None, i_max=None):
    if i_min is None:
        # i_min = image.min()
        i_min = np.percentile(image, 5)
    if i_max is None:
        # i_max = image.max()
        i_max = np.percentile(image, 95)
    # lut = vtk.vtkLookupTable()
    lut = vtk.vtkColorTransferFunction()
    # lut.DiscretizeOn()

    from colormap_utils import colormap_names
    assert colormap in colormap_names

    if colormap == "grey":
        # lut.SetTableRange(image.min(), image.max())
        # lut.SetSaturationRange(0, 0)
        # lut.SetHueRange(0, 0)
        # lut.SetValueRange(0, 1)
        lut.AddRGBPoint(i_min, 0.0, 0.0, 0.0)
        lut.AddRGBPoint(i_max, 1.0, 1.0, 1.0)

    elif colormap == "invert_grey":
        lut.AddRGBPoint(i_min, 1.0, 1.0, 1.0)
        lut.AddRGBPoint(0.5 * i_min + 0.5 * i_max, 0.4, 0.4, 0.5)
        lut.AddRGBPoint(i_max, 0.2, 0.2, 0.2)

    elif colormap == "jet":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0.0, 0.0, 0.3)
        lut.AddRGBPoint(0.85 * i_min + 0.15 * i_max, 0.0, 0.0, 1.0)
        lut.AddRGBPoint(0.7 * i_min + 0.3 * i_max, 0.0, 1.0, 0.0)
        lut.AddRGBPoint(0.3 * i_min + 0.7 * i_max, 1.0, 1.0, 0.0)
        lut.AddRGBPoint(0.15 * i_min + 0.85 * i_max, 1.0, 0.0, 0.0)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 0.3, 0.0, 0.0)

    elif colormap == "hot":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0.0, 0.0, 0.0)
        lut.AddRGBPoint(0.67 * i_min + 0.33 * i_max, 1.0, 0.0, 0.0)
        lut.AddRGBPoint(0.33 * i_min + 0.67 * i_max, 1.0, 1.0, 0.0)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 1.0, 1.0, 1.0)

    elif colormap == "blue":
        lut.AddRGBPoint(i_min, 0.7, 0.7, 1.0)
        lut.AddRGBPoint(0.5 * i_min + 0.5 * i_max, 0.5, 0.5, 0.9)
        lut.AddRGBPoint(i_max, 1.0, 1.0, 0.7)

    elif colormap == "terrain":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0., 0.651, 0.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 0.902, 0.902, 0.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 0.925, 0.694, 0.463)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 0.949, 0.949, 0.949)

    # custom lookup tables ;)

    elif colormap == "cold":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 8 / 255., 104 / 255., 172 / 255.)
        lut.AddRGBPoint(0.75 * i_min + 0.25 * i_max, 67 / 255., 162 / 255., 202 / 255.)
        lut.AddRGBPoint(0.5 * i_min + 0.5 * i_max, 123 / 255., 204 / 255., 196 / 255.)
        lut.AddRGBPoint(0.25 * i_min + 0.75 * i_max, 186 / 255., 228 / 255., 188 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 240 / 255., 249 / 255., 232 / 255.)

    elif colormap == "temperature":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 19 / 255., 70 / 255., 135 / 255.)
        lut.AddRGBPoint(0.9 * i_min + 0.1 * i_max, 0 / 255., 56 / 255., 216 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 150 / 255., 196 / 255., 222 / 255.)
        lut.AddRGBPoint(0.65 * i_min + 0.35 * i_max, 230 / 255., 225 / 255., 193 / 255.)
        lut.AddRGBPoint(0.35 * i_min + 0.65 * i_max, 225 / 255., 194 / 255., 63 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 241 / 255., 89 / 255., 33 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 115 / 255., 4 / 255., 5 / 255.)

    elif colormap == "atmosphere":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 237 / 255., 234 / 255., 206 / 255.)
        lut.AddRGBPoint(0.67 * i_min + 0.33 * i_max, 127 / 255., 212 / 255., 183 / 255.)
        lut.AddRGBPoint(0.33 * i_min + 0.67 * i_max, 86 / 255., 149 / 255., 200 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 149 / 255., 37 / 255., 130 / 255.)

    elif colormap == "vegetation":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 255 / 255., 246 / 255., 229 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 219 / 255., 219 / 255., 162 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 158 / 255., 184 / 255., 106 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 91 / 255., 148 / 255., 62 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 29 / 255., 112 / 255., 29 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 8 / 255., 77 / 255., 31 / 255.)

    elif colormap == "ocean":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 46 / 255., 43 / 255., 77 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 8 / 255., 70 / 255., 117 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 5 / 255., 112 / 255., 166 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 56 / 255., 168 / 255., 208 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 113 / 255., 212 / 255., 217 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 204 / 255., 219 / 255., 218 / 255.)

    elif colormap == "density":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 240 / 255., 240 / 255., 224 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 240 / 255., 240 / 255., 176 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 240 / 255., 224 / 255., 144 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 240 / 255., 176 / 255., 172 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 208 / 255., 112 / 255., 80 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 176 / 255., 48 / 255., 48 / 255.)

    elif colormap == "curvature":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0.125, 0.9, 1.0)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 0.125, 0.3, 1.0)
        lut.AddRGBPoint(0.55 * i_min + 0.45 * i_max, 0.125, 0.125, 0.3)
        lut.AddRGBPoint(0.45 * i_min + 0.55 * i_max, 0.3, 0.125, 0.125)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 1.0, 0.3, 0.125)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 1., 0.9, 0.125)

    elif colormap == "green":
        # lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0 / 255., 86 / 255., 5 / 255.)
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0 / 255., 0 / 255., 0 / 255.)
        lut.AddRGBPoint(0.75 * i_min + 0.25 * i_max, 40 / 255., 134 / 255., 0 / 255.)
        lut.AddRGBPoint(0.5 * i_min + 0.5 * i_max, 46 / 255., 255 / 255., 0 / 255.)
        lut.AddRGBPoint(0.25 * i_min + 0.75 * i_max, 189 / 255., 255 / 255., 82 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 212 / 255., 255 / 255., 69 / 255.)

    elif colormap == "purple":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 0.0, 0.0, 0.0)
        lut.AddRGBPoint(0.9 * i_min + 0.1 * i_max, 0.133, 0.0, 0.32)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 0.55, 0.0, 0.65)
        lut.AddRGBPoint(0.35 * i_min + 0.65 * i_max, 0.88, 0.08, 0.52)
        lut.AddRGBPoint(0.1 * i_min + 0.9 * i_max, 1., 0.66, 0.86)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 1., 0.92, 0.88)

    elif colormap == "red":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 73 / 255., 16 / 255., 18 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 94 / 255., 15 / 255., 2 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 139 / 255., 31 / 255., 19 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 154 / 255., 51 / 255., 52 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 203 / 255., 97 / 255., 71 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 239 / 255., 238 / 255., 239 / 255.)

    elif colormap == "marocco":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 62 / 255., 23 / 255., 78 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 98 / 255., 26 / 255., 74 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 155 / 255., 1 / 255., 59 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 216 / 255., 71 / 255., 40 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 255 / 255., 134 / 255., 3 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 255 / 255., 197 / 255., 2 / 255.)

    elif colormap == "sepia":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 245 / 255., 236 / 255., 233 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 232 / 255., 213 / 255., 204 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 158 / 255., 130 / 255., 109 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 125 / 255., 97 / 255., 77 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 95 / 255., 66 / 255., 36 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 72 / 255., 43 / 255., 13 / 255.)

    elif colormap == "color":
        # lut.SetNumberOfTableValues(image.max() + 1)
        # lut.SetNumberOfColors(i_max() + 1)
        # lut.SetRange(i_min(), i_max())
        lut.AddHSVPoint(i_min, 0.0, 1.0, 0.8)
        lut.AddHSVPoint(0.67 * i_min + 0.33 * i_max, 0.33, 1.0, 0.8)
        lut.AddHSVPoint(0.33 * i_min + 0.67 * i_max, 0.67, 1.0, 0.8)
        lut.AddHSVPoint(i_max, 1.0, 1.0, 0.8)

    elif colormap == "glasbey":
        from colormap_utils import glasbey
        if i_max < 255:
            for i in xrange(256):
                #   lut.AddRGBPoint((1.-i/255.)*i_min + (i/255.)*i_max,glasbey[i][0],glasbey[i][1],glasbey[i][2])
                lut.AddRGBPoint(i, glasbey[i][0], glasbey[i][1], glasbey[i][2])
        else:
            for i in np.unique(image):
                # for i in xrange(65536):
                lut.AddRGBPoint(i, glasbey[i % 256][0], glasbey[i % 256][1], glasbey[i % 256][2])

    # lut.Build()
    return lut


def matrix_to_image_reader(name, data_matrix, datatype=np.uint16, decimate=1):
    nx, ny, nz = data_matrix.shape
    data_string = data_matrix.tostring('F')

    reader = vtk.vtkImageImport()
    reader.CopyImportVoidPointer(data_string, len(data_string))
    if datatype == np.uint8:
        reader.SetDataScalarTypeToUnsignedChar()
    else:
        reader.SetDataScalarTypeToUnsignedShort()
    reader.SetNumberOfScalarComponents(1)
    reader.SetDataExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
    reader.SetWholeExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)

    return reader


def blend_funct(data_matrix, data1, lookuptable1, data2, lookuptable2, orientation):
    nx, ny, nz = data_matrix.shape
    xMax = nx - 1
    yMax = ny - 1
    zMax = nz - 1

    p1Colors = vtk.vtkImageMapToColors()
    p1Colors.SetInputConnection(data1.GetOutputPort())
    p1Colors.SetLookupTable(lookuptable1)
    p2Colors = vtk.vtkImageMapToColors()
    p2Colors.SetInputConnection(data2.GetOutputPort())
    p2Colors.SetLookupTable(lookuptable2)
    blend = vtk.vtkImageBlend()
    blend.AddInput(p1Colors.GetOutput())
    blend.AddInput(p2Colors.GetOutput())
    blend.SetOpacity(0, 0.5)
    blend.SetOpacity(1, 0.5)
    imgactor = vtk.vtkImageActor()
    imgactor.SetInput(blend.GetOutput())
    if orientation == 1:
        imgactor.SetDisplayExtent(np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
    elif orientation == 2:
        imgactor.SetDisplayExtent(0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
    elif orientation == 3:
        imgactor.SetDisplayExtent(0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

    imgactor.SetOrigin(nx / 2., ny / 2., nz / 2.)
    imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)

    return imgactor, blend


class VtkViewerWidget(QtGui.QWidget, AbstractListener):
    matrixAdded = QtCore.Signal(str)
    worldChanged = QtCore.Signal()

    def __init__(self):
        QtGui.QWidget.__init__(self)
        AbstractListener.__init__(self)

        layout = QtGui.QVBoxLayout(self)
        self.vtk = VtkViewer()
        self.vtk.matrixAdded.connect(self.matrixAdded.emit)
        layout.addWidget(self.vtk)

        self.world = World()
        self.world.register_listener(self)

        self.interpreter = get_interpreter()
        self.interpreter.locals['world_viewer'] = self
        self.interpreter.locals['viewer'] = self.vtk

        self._create_actions()
        self._create_connections()

    def show_control_panel(self):
        from tissuelab.gui.vtkviewer.vtkcontrolpanel import VtkControlPanel
        self.panel = VtkControlPanel()
        self.matrixAdded.connect(self.panel.set_matrix)
        self.panel.set_viewer(self.vtk)
        self.panel.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.panel.show()

    def _create_actions(self):
        self.action_control_panel = QtGui.QAction('Control Panel', self)

    def _create_connections(self):
        self.action_control_panel.triggered.connect(self.show_control_panel)

    def toolbar_actions(self):
        return [
            self.action_control_panel
        ]

    def notify(self, sender, event=None):
        signal, data = event
        if signal == 'world_sync':
            self.worldChanged.emit()
            self.set_world(data)

    def set_world(self, world):
        self.vtk.clear()
        for obj_name, world_object in world.items():
            obj = world_object.obj
            if isinstance(obj, np.ndarray):
                self.vtk.add_matrix(obj_name, obj, datatype=obj.dtype, **world_object.kwargs)
            if isinstance(obj, vtk.vtkActor):
                self.vtk.add_actor(obj_name, obj)
        self.vtk.compute()


class VtkViewer(QtGui.QWidget):
    matrixAdded = QtCore.Signal(str)

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

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        layout.addWidget(self.frame)
        self.ren.ResetCamera()

        self.matrix = {}
        self.reader = {}
        self.volume_property = {}
        self.volume = {}
        self.actor = {}
        self.property = {}

    def display_volume(self, name=None, disp=True):
        self.clear_scene()
        self._display_volume(name, disp)
        self.compute()

    def display_cut_planes(self, name=None, disp=True):
        self.clear_scene()
        self._display_cut_planes(name, disp)
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

    def initialize(self):
        pass
#         self.ren.ResetCamera()
#         self.iren.AddObserver("MouseMoveEvent", self.on_cursor_moved)


#     def on_cursor_moved(self, iren, event):
#         if self.picker is None:
#             return
#         x, y = iren.GetEventPosition()
#         self.picker.Pick(x, y, 0, self.ren)
#         print self.picker.GetSubId()

    def clear_scene(self):
        for name, volume in self.volume.items():
            self.ren.RemoveVolume(volume)
        for name, actor in self.actor.items():
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

        self.render()

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
        self.ren.ResetCamera()
        self.render()

    def render(self):
        self.iren.Render()

    def add_actor(self, name, actor):
        self.actor[name] = actor
        self.property[name] = dict(disp=True)

    def add_matrix(self, name, data_matrix, datatype=np.uint8, decimate=1, **kwargs):
        self.matrix[name] = data_matrix

        self.add_matrix_as_volume(name, data_matrix, datatype, decimate, **kwargs)
        self.add_matrix_cut_planes(name, data_matrix, datatype, decimate, **kwargs)

        self._display_cut_planes(name, kwargs.get('cut_planes', True))
        self._display_volume(name, kwargs.get('volume', True))

        self.matrixAdded.emit(name)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)
        cmap = kwargs.get('colormap', 'grey')
        alpha = kwargs.get('alpha', 1.0)
        # bwLut = define_lookuptable(data_matrix, "grey")
        # colorLut = define_lookuptable(data_matrix, "glasbey")
        lut = define_lookuptable(data_matrix, colormap=cmap)
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
                imgactor.SetDisplayExtent(np.round(xMax / 2), np.round(xMax / 2), 0, yMax, 0, zMax)
            elif orientation == 2:
                imgactor.SetDisplayExtent(0, xMax, np.round(yMax / 2), np.round(yMax / 2), 0, zMax)
            elif orientation == 3:
                imgactor.SetDisplayExtent(0, xMax, 0, yMax, np.round(zMax / 2), np.round(zMax / 2))

            imgactor.SetOrigin(nx / 2., ny / 2., nz / 2.)
            imgactor.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)
            # imgactor, blend = blend_funct(data_matrix, reader, lut, reader, lut, orientation)
            # self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend
            self.vtkdata['%s_cut_plane_colors_%d' % (name, orientation)] = colors
            self.add_actor('%s_cut_plane_%d' % (name, orientation), imgactor)
        self.set_cut_planes_alpha(name, alpha)

    def add_matrix_as_volume(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        nx, ny, nz = data_matrix.shape
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)

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

        self.volume_property[name] = dict(vtkVolumeProperty=volume_property, disp=True)

        volume = self.volume[name] = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volume_property)
        volume.SetOrigin(nx / 2., ny / 2., nz / 2.)
        volume.SetPosition(-(nx - 1) / 2., -(ny - 1) / 2., -(nz - 1) / 2.)

        cmap = kwargs.get('colormap', 'grey')
        alpha = kwargs.get('alpha', 1.0)
        alphamap = kwargs.get('alphamap', 'linear')
        # self.color_cell(name, alpha=alpha, colormap=cmap)
        self.set_lookuptable(name, cmap, cut_planes=False)
        self.set_volume_alpha(name, alpha, alphamap)

    def set_volume_alpha(self, name, alpha=1.0, alphamap="constant", **kwargs):
        alphaChannelFunc = self.volume_property[name]['vtkVolumeProperty'].GetScalarOpacity()
        alphaChannelFunc.RemoveAllPoints()

        bg_id = kwargs.get('bg_id', None)
        i_min = kwargs.get('i_min', self.matrix[name].min())
        i_max = kwargs.get('i_max', self.matrix[name].max())

        if alphamap == "constant":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, alpha)
            alphaChannelFunc.AddPoint(i_max, alpha)

            if bg_id is not None:
                alphaChannelFunc.AddPoint(bg_id - 1, alpha)
                alphaChannelFunc.AddPoint(bg_id, 0.0)
                alphaChannelFunc.AddPoint(bg_id + 1, alpha)

        elif alphamap == "linear":
            alphaChannelFunc.ClampingOn()
            alphaChannelFunc.AddPoint(i_min, 0.0)
            alphaChannelFunc.AddPoint(i_max, alpha)

    def set_cut_planes_alpha(self, name, alpha=1.0, **kwargs):
        for orientation in [1, 2, 3]:
            self.actor[name + "_cut_plane_" + str(orientation)].SetOpacity(alpha)

    def set_lookuptable(self, name, colormap='grey', **kwargs):
        i_min = kwargs.get('i_min', None)
        i_max = kwargs.get('i_max', None)
        cut_planes = kwargs.get('cut_planes', True)
        lut = define_lookuptable(self.matrix[name], colormap, i_min, i_max)
        self.volume_property[name]['vtkVolumeProperty'].SetColor(lut)
        if cut_planes:
            for orientation in [1, 2, 3]:
                self.vtkdata[name + "_cut_plane_colors_" + str(orientation)].SetLookupTable(lut)

    def color_cell(self, name, cell_id=None, color=None, alpha=None, bg_id=1, colormap='glasbey'):

        alphaChannelFunc = self.volume_property[name]['vtkVolumeProperty'].GetScalarOpacity()

        if alpha is None:
            alpha = 1.

        # colorFunc.AddRGBPoint(bg_id, 1.0, 1.0, 1.0)

        for matrix in self.matrix.values():

            if cell_id is None:
                # colorFunc.RemoveAllPoints()

                self.volume_property[name]['vtkVolumeProperty'].SetColor(define_lookuptable(matrix, colormap))

                alphaChannelFunc.RemoveAllPoints()

                alphaChannelFunc.AddPoint(bg_id, 0.0)

                # if colormap == 'random':
                #     from random import random as r
                #     for i in np.unique(matrix):
                #         colorFunc.AddRGBPoint(i, r(), r(), r())
                # elif colormap == 'monocolor':
                #     for i in np.unique(matrix):
                #         colorFunc.AddRGBPoint(i, *color)

                # elif colormap == 'grey':
                # colorFunc.AddRGBPoint(matrix.min(),0.0,0.0,0.0)
                # colorFunc.AddRGBPoint(matrix.max(),1.0,1.0,1.0)
                # colorFunc.AddHSVPoint(matrix.min(),0.0,1.0,0.5)
                # colorFunc.AddHSVPoint(matrix.max(),0.5,1.0,0.5)

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
                colorFunc = self.volume_property[name]['vtkVolumeProperty'].GetRGBTransferFunction()
                colorFunc.AddRGBPoint(cell_id, *color)

                alphaChannelFunc.AddPoint(cell_id, alpha)

    # def color_intensity(self, name, intensity_min=0, intensity_max=255, colormap='grey'):

    #     colorFunc = self.volume_property[name]['vtkVolumeProperty'].GetRGBTransferFunction()
    #     alphaChannelFunc = self.volume_property[name]['vtkVolumeProperty'].GetScalarOpacity()

    def demo_matrix_xyz(self):
        dtype = np.uint16
        matrix = np.zeros([100, 100, 100], dtype=dtype)
        matrix[90:100, 0:10, 0:10] = 1
        matrix[0:10, 90:100, 0:10] = 2
        matrix[0:10, 0:10, 90:100] = 3
        return matrix

    def demo_matrix1(self):
        dtype = np.uint16
        matrix = np.zeros([75, 75, 75], dtype=dtype)
        matrix[25:55, 25:55, 25:55] = 1
        matrix[45:74, 45:74, 45:74] = 10
        return matrix

    def demo_matrix2(self):
        dtype = np.uint16
        matrix = np.zeros([75, 75, 75], dtype=dtype)
        matrix[0:10, 0:10, 0:10] = 1

        return matrix

    def demo_actor(self):
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(5.0)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        return actor

    def demo(self):

        self.clear()

        matrix1 = self.demo_matrix1()
        matrix2 = self.demo_matrix2()
        sphere = self.demo_actor()

        self.add_matrix('matrix1', matrix1)
        self.color_cell('matrix1')

        self.add_matrix('matrix2', matrix2)
        self.color_cell('matrix2', colormap='monocolor')

        self.add_actor('sphere', sphere)

        self.compute()

    def resizeEvent(self, *args, **kwargs):
        self.render()
        return QtGui.QWidget.resizeEvent(self, *args, **kwargs)
