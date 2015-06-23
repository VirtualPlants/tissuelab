class IPolyDataEditor(object):

    """
    Qt applet to edit a mesh.
    Features:
        - allow to edit meshes: remove, add, move points, edges, ...
        - support 3d background image
    """

    def load_bg_image(self):
        """
        Display a file selector to choose a bg image to use.
        """

    def set_mesh(self, mesh):
        pass

    def mesh(self):
        pass


class IVtkPolyDataEditor(object):

    """
    Class to edit a vtkPolyData:
        - move points
        - delete points
        - add points
        - add edges

    This Editor works on copy of polydata, you can get modified version with "polydata" method.
    """

    def set_bg_image(self, spatial_image=None):
        """
        :param spatial_image: a :class:`~openalea.image.spatial_image.SpatialImage`
        """

    def set_polydata(self, polydata, **kwargs):
        """
        :param polydata: A :obj:`~vtk.vtkPolyData` or list of vtkPolyData
        """

    def polydata(self):
        """
        :return: list of polydata
        """
