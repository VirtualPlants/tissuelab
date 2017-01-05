import sys

from Qt import QtWidgets

from openalea.grapheditor import qt
from custom_graph_model import Graph

tmp=None
#CUSTOMISING THE GRAPH VIEW FOR THIS PARTICULAR DEMO:
class SimpleView( qt.View ):
    def __init__(self, *args, **kwargs):
        qt.View.__init__(self, *args, **kwargs)
        self.set_default_drop_handler(self.dropHandler)

    def dropHandler(self, event):
        position = self.mapToScene(event.pos())
        position = [position.x(), position.y()]
        self.scene().new_vertex(position=position)

    # def mousePressEvent(self, event):
    #     print event.globalX(), event.globalY()
    #     global tmp
    #     tmp=event
    #     print event.button()
    #     return qt.View.mousePressEvent(self, event)

    #mouseSimpleClickEvent = test
    mouseDoubleClickEvent = dropHandler

class SimpleVertex(qt.DefaultGraphicalVertex):
    def __init__(self, *args, **kwargs):
        qt.DefaultGraphicalVertex.__init__(self, *args, **kwargs)
        self.initialise(self.get_observed().get_ad_hoc_dict())
        self.link_value=0

    def get_view_data(self, key):
        # print z
        # z+=1
        return self.get_observed().get_ad_hoc_dict().get_metadata(key)

SimpleGraph = qt.QtGraphStrategyMaker( graphView            = SimpleView,
                                       vertexWidgetMap      = {"vertex":SimpleVertex},
                                       edgeWidgetMap        = {"default":qt.DefaultGraphicalEdge,
                                                               "floating-default":qt.DefaultGraphicalFloatingEdge},
                                       graphViewInitialiser = None,
                                       adapterType          = None )


def get_next(t, n):
    if t.get(n, '')=='':
        return [n]
    else:
        d=t[n]
        out=[]
        for i in d:
            out.extend(get_next(t, i))
        return out

#THE APPLICATION'S MAIN WINDOW
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """                """
        QtWidgets.QMainWindow.__init__(self, parent)
        self.__graph = Graph()
        self.__graphView = SimpleGraph.create_view(self.__graph, parent=self)
        self.setCentralWidget(self.__graphView)
        import pickle as pkl
        import numpy as np
        f=open("lin_tree_NOV_cor.pkl")
        t=pkl.load(f)
        f.close()
        t={ k: v for k, v in t.iteritems() if k/10**3<20 }
        t_back={ vi : k for k, v in t.iteritems() for vi in v }
        nodes=np.array(list(set(t.keys()).union(t_back.keys())))
        time_max=np.max(nodes)/10**3
        leaves=[]
        for n in nodes[nodes/10**3==1]:
            leaves.extend(get_next(t, n))
        placed=[]
        vertices={}
        positions={}
        for i, node in enumerate(leaves):
            vertices[node]=self.__graph.new_vertex(node, (i*40, 0))
            placed.append(node)
            positions[node]=i*40
        for time in range(time_max-2, 0, -2):
            for node in nodes[nodes/10**3==time]:
                if t.get(node, '')!='':
                    #print "node : ", node
                    tmp=[positions.get(v, '') for v in t[node] if positions.get(v, '')!='']
                    #print tmp
                    if tmp!=[]:
                        pos=np.mean([positions.get(v, '') for v in t[node] if positions.get(v, '')!=''])
                        vertices[node]=self.__graph.new_vertex(node, (pos, (time-time_max)*30))
                        [self.__graph.new_edge(vertices[node], vertices[c]) for c in t.get(node, '') if c!='' and vertices.get(c, '')!='']
                        positions[node]=pos

        #print self.__graph.get_vertex_inputs()
        # v1 = self.__graph.new_vertex((0, 0))
        # v2 = self.__graph.new_vertex((10, 10))
        # v3 = self.__graph.new_vertex((20, 20))
        # self.__graph.new_edge(v1, v2)
        # self.__graph.new_edge(v2, v3)



#THE ENTRY POINT
def main(args):
    app = QtWidgets.QApplication([])
    QtWidgets.QApplication.processEvents()
    win = MainWindow()
    win.show()

    from tissuelab.plugins.labs import TissueLab
    lab = TissueLab()

    from openalea.oalab.widget.mainwindow import MainWindow as MW
    from openalea.oalab.session.session import Session
    session = Session()
    session.extension = 'tissue'
    mainwindow2 = MW(session)
    lab(mainwindow2)
    mainwindow2.show()
    mainwindow2.raise_()

    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)
