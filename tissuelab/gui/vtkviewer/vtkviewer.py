
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


# class JetMap (ColorRange) :
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.,0.,0.3),blue,green,
#                              yellow,red,Color(0.3,0.,0.)],
#                             (0.,0.15,0.3,0.7,0.85,1.),
#                             **keys)

# class TerrainMap (ColorRange) :
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.,0.651,0.),Color(0.902,0.902,0.),
#                              Color(0.925,0.694,0.463),Color(0.949,0.949,0.949)],
#                             (0.,0.4,0.8,1.),
#                             **keys)

# class HeatMap (ColorRange) :
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.2,0.,0.),red,
#                              yellow,white,Color(0.3,0.3,1.)],
#                             (0.,0.3,0.6,0.9,1.),
#                             **keys)

# class JetMapWithoutRed (ColorRange) :
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.,0.,0.3),blue,green,
#                              yellow,magenta],
#                             (0.,0.2,0.5,0.8,1.),
#                             **keys)

# class GreenMap (ColorRange) :
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.,0.,0.),Color(0.,0.1,0.),green],
#                             (0.,.5,1.),
#                             **keys)


# class BlueMap (ColorRange) :
#     """Created by Michael Walker 16/05/2011. If Jerome has a problem he can sue me.
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(.7,.7,1.),Color(0.5,0.5,.9),Color(.1,.1,.7)],
#                             (0.,.5,1.),
#                             **keys)

# class CurvMap (ColorRange) :
#     """Created by Guillaume Cerutti 06/07/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.125,0.9,1.0),Color(0.125,0.3,1.0),Color(0.125,0.125,0.3),Color(0.3,0.125,0.125),Color(1.0,0.3,0.125),Color(1.,0.9,0.125)],
#                             (0.,.2,.45,0.55,.8,1.),
#                             **keys)

# class PurpleMap (ColorRange) :
#     """Created by Guillaume Cerutti 18/12/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0.0,0.0,0.0),Color(0.133,0.0,0.32),Color(0.55,0.0,0.65),Color(0.88,0.08,0.52),Color(1.,0.66,0.86),Color(1.,0.92,0.88)],
#                             (0.,.1,.4,0.65,.9,1.),
#                             **keys)

# class HotMap (ColorRange) :
#     """Created by Guillaume Cerutti 18/12/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [black,red,yellow,white],
#                             (0.,.33,.66,1.),
#                             **keys)

# class ColdMap (ColorRange) :
#     """Created by Guillaume Cerutti 18/12/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(8/255.,104/255.,172/255.),Color(67/255.,162/255.,202/255.),Color(123/255.,204/255.,196/255.),Color(186/255.,228/255.,188/255.),Color(240/255.,249/255.,232/255.)],
#                             (0.,.25,.5,.75,1.),
#                             **keys)

# class PureGreenMap (ColorRange) :
#     """Created by Guillaume Cerutti 18/12/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(0/255.,86/255.,5/255.),Color(40/255.,134/255.,0/255.),Color(46/255.,255/255.,0/255.),Color(189/255.,255/255.,82/255.),Color(212/255.,255/255.,69/255.)],
#                             (0.,.25,.5,.75,1.),
#                             **keys)

# class AtmosphereMap (ColorRange) :
#     """Created by Guillaume Cerutti 18/12/2014
#     """
#     def __init__ (self, val_min=0., val_max=1., **keys) :
#         ColorRange.__init__(self,
#                             (val_min,val_max),
#                             [Color(237/255.,234/255.,206/255.),Color(127/255.,212/255.,183/255.),Color(86/255.,149/255.,200/255.),Color(149/255.,37/255.,130/255.),],
#                             (0.,.33,.66,1.),
#                             **keys)


def define_LUT(image, colormap, i_min=None, i_max=None):
    if i_min is None:
        # i_min = image.min()
        i_min = np.percentile(image, 5)
    if i_max is None:
        # i_max = image.max()
        i_max = np.percentile(image, 95)
    # lut = vtk.vtkLookupTable()
    lut = vtk.vtkDiscretizableColorTransferFunction()
    # lut.DiscretizeOn()
    if colormap == "grey":
        # lut.SetTableRange(image.min(), image.max())
        # lut.SetSaturationRange(0, 0)
        # lut.SetHueRange(0, 0)
        # lut.SetValueRange(0, 1)
        lut.AddRGBPoint(i_min, 0.0, 0.0, 0.0)
        lut.AddRGBPoint(i_max, 1.0, 1.0, 1.0)

    elif colormap == "invert_grey":
        lut.AddRGBPoint(i_min, 1.0, 1.0, 1.0)
        lut.AddRGBPoint(0.5 * i_min + 0.5 * i_max, 0.5, 0.5, 0.55)
        lut.AddRGBPoint(i_max, 0.0, 0.0, 0.0)

    elif colormap == "vegetation":
        lut.AddRGBPoint(1.0 * i_min + 0.0 * i_max, 255 / 255., 246 / 255., 229 / 255.)
        lut.AddRGBPoint(0.8 * i_min + 0.2 * i_max, 219 / 255., 219 / 255., 162 / 255.)
        lut.AddRGBPoint(0.6 * i_min + 0.4 * i_max, 158 / 255., 184 / 255., 106 / 255.)
        lut.AddRGBPoint(0.4 * i_min + 0.6 * i_max, 91 / 255., 148 / 255., 62 / 255.)
        lut.AddRGBPoint(0.2 * i_min + 0.8 * i_max, 29 / 255., 112 / 255., 29 / 255.)
        lut.AddRGBPoint(0.0 * i_min + 1.0 * i_max, 8 / 255., 77 / 255., 31 / 255.)

    elif colormap == "color":
        # lut.SetNumberOfTableValues(image.max() + 1)
        # lut.SetNumberOfColors(i_max() + 1)
        # lut.SetRange(i_min(), i_max())
        lut.AddHSVPoint(i_min, 0.0, 1.0, 0.8)
        lut.AddHSVPoint(0.67 * i_min + 0.33 * i_max, 0.33, 1.0, 0.8)
        lut.AddHSVPoint(0.33 * i_min + 0.67 * i_max, 0.67, 1.0, 0.8)
        lut.AddHSVPoint(i_max, 1.0, 1.0, 0.8)

    elif colormap == "glasbey":
        from glasbey import glasbey
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


def blend_funct(data_matrix, data1, LUT1, data2, LUT2, orientation):
    nx, ny, nz = data_matrix.shape
    xMax = nx - 1
    yMax = ny - 1
    zMax = nz - 1

    p1Colors = vtk.vtkImageMapToColors()
    p1Colors.SetInputConnection(data1.GetOutputPort())
    p1Colors.SetLookupTable(LUT1)
    p2Colors = vtk.vtkImageMapToColors()
    p2Colors.SetInputConnection(data2.GetOutputPort())
    p2Colors.SetLookupTable(LUT2)
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

    def display_volume(self, disp=True):
        self.clear_scene()
        self._display_volume(disp)
        self.compute()

    def display_cut_planes(self, disp=True):
        self.clear_scene()
        self._display_cut_planes(disp)
        self.compute()

    def _display_volume(self, disp=True):
        for name in self.volume:
            self.volume_property[name]['disp'] = disp

    def _display_cut_planes(self, disp=True):
        for actor_name in self.actor:
            if '_cut_plane_' in actor_name:
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

        self.matrixAdded.emit(name)

    def add_matrix_cut_planes(self, name, data_matrix, datatype=np.uint16, decimate=1, **kwargs):
        self.reader[name] = reader = matrix_to_image_reader(name, data_matrix, datatype, decimate)
        cmap = kwargs.get('colormap', 'grey')
        # bwLut = define_LUT(data_matrix, "grey")
        # colorLut = define_LUT(data_matrix, "glasbey")
        lut = define_LUT(data_matrix, cmap)
        for orientation in [1, 2, 3]:
            actor, blend = blend_funct(data_matrix, reader, lut, reader, lut, orientation)
            self.vtkdata['%s_blend_cut_plane_%d' % (name, orientation)] = blend
            self.add_actor('%s_cut_plane_%d' % (name, orientation), actor)

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
        alpha = kwargs.get('alpha', None)
        self.color_cell(name, alpha=alpha, colormap=cmap)

    def color_cell(self, name, cell_id=None, color=None, alpha=None, bg_id=1, colormap='glasbey'):

        alphaChannelFunc = self.volume_property[name]['vtkVolumeProperty'].GetScalarOpacity()

        # if alpha is None:
        #     alpha = 1.

        # colorFunc.AddRGBPoint(bg_id, 1.0, 1.0, 1.0)

        for matrix in self.matrix.values():

            if cell_id is None:
                # colorFunc.RemoveAllPoints()

                self.volume_property[name]['vtkVolumeProperty'].SetColor(define_LUT(matrix, colormap))

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
                if alpha is None:

                    if colormap not in ['glasbey']:
                        alphaChannelFunc.RemoveAllPoints()
                        alphaChannelFunc.AddPoint(matrix.min(), 0.0)
                        alphaChannelFunc.AddPoint(matrix.max(), 1.0)
                    else:
                        # alphaChannelFunc.AddPoint(1, 0.0)
                        alphaChannelFunc.AddPoint(bg_id + 1, 1.0)
                        alphaChannelFunc.AddPoint(matrix.max(), 1.0)

                # else:
                #     m = np.max(matrix)
                #     for i in np.unique(matrix):
                #         if i != 0:
                #             colorFunc.AddRGBPoint(i, i / np.float(m), 1 - i / np.float(m), 0.0)
                else:
                    for i in np.unique(matrix):
                        if i > bg_id:
                            alphaChannelFunc.AddPoint(i, alpha)

            else:
                if color is None:
                    color = (1., 1., 1.)
                colorFunc = self.volume_property[name]['vtkVolumeProperty'].GetRGBTransferFunction()
                colorFunc.AddRGBPoint(cell_id, *color)
                if alpha is None:
                    alpha = 1.
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
