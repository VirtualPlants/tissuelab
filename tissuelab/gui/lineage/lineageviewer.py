
from openalea.vpltk.qt import QtGui

from openalea.grapheditor import qt
from custom_graph_model import Graph

class SimpleView(qt.View):
    def __init__(self, *args, **kwargs):
        qt.View.__init__(self, *args, **kwargs)
        self.set_default_drop_handler(self.dropHandler)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        self.scene().new_vertex(position=position)


    def clear(self):
        self.__observableGraph.unregister_listener(self)
        self.__graph = None
        self.__graphAdapter = None
        self.__observableGraph = None
        self.__widgetmap.clear()

    mouseDoubleClickEvent = dropHandler

class SimpleVertex(qt.DefaultGraphicalVertex):
    def __init__(self, *args, **kwargs):
        qt.DefaultGraphicalVertex.__init__(self, *args, **kwargs)
        self.initialise(self.get_observed().get_ad_hoc_dict())
        self.link_value = 0

    def get_view_data(self, key):
        return self.get_observed().get_ad_hoc_dict().get_metadata(key)

SimpleGraph = qt.QtGraphStrategyMaker(graphView=SimpleView,
                                       vertexWidgetMap={"vertex":SimpleVertex},
                                       edgeWidgetMap={"default":qt.DefaultGraphicalEdge,
                                                               "floating-default":qt.DefaultGraphicalFloatingEdge},
                                       graphViewInitialiser=None,
                                       adapterType=None)


class LineageViewer(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.graph = Graph()
        self.view = SimpleGraph.create_view(self.graph)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)

    def new_graph(self):
        return self.graph.__class__()

    def set_graph(self, graph):
        scene = self.view.scene()
        scene.clear()
        self.view.set_graph(graph)
        self.graph = graph

    def demo_fill_graph(self, graph):
        import random
        for i in range(50):
            graph.new_vertex(i, (i * 40, random.randint(0, 4) * 10))

