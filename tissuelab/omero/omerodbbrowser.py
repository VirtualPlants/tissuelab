
__all__ = ['OmeroDbBrowser', 'OmeroModel', 'OmeroView']

from cStringIO import StringIO

from openalea.image.pil import Image
from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.QtCore import Signal

def image_to_items(image):
    item_type_image = QtGui.QStandardItem('image')
    item_image = QtGui.QStandardItem(image.getName())
    item_id = QtGui.QStandardItem(unicode(image.getId()))
    item_thumbnail = QtGui.QStandardItem()

    item_image.setData(image)

    img_data = image.getThumbnail()
    renderedThumb = Image.open(StringIO(img_data))
    # renderedThumb.show()           # shows a pop-up
    filename = "thumbnail_%d.jpg" % image.getId()
    renderedThumb.save(filename)
    item_thumbnail.setIcon(QtGui.QIcon(filename))
    return [item_image, item_type_image, item_id, item_thumbnail]

def dataset_to_items(dataset):
    item_type_dataset = QtGui.QStandardItem('dataset')
    item_dataset = QtGui.QStandardItem(dataset.getName())
    item_id = QtGui.QStandardItem(unicode(dataset.getId()))

    item_dataset.setData(dataset)

    return [item_dataset, item_type_dataset, item_id]

def project_to_items(project):
    item_type_project = QtGui.QStandardItem('project')
    item_project = QtGui.QStandardItem(project.getName())
    item_id = QtGui.QStandardItem(unicode(project.getId()))

    item_project.setData(project)

    return [item_project, item_type_project, item_id]

def group_to_items(group):
    item_type_group = QtGui.QStandardItem('group')
    item_group = QtGui.QStandardItem(group.getName())
    item_id = QtGui.QStandardItem(unicode(group.getId()))

    item_group.setData(group)

    return [item_group, item_type_group, item_id]


class OmeroModel(QtGui.QStandardItemModel):
    def __init__(self):
        self._connexion = None
        self._data = []

        QtGui.QStandardItemModel.__init__(self)

    def setConnection(self, omero_connexion):
        self._connexion = omero_connexion
        self.refresh()

    def refresh(self):
        # Here we should use a backend strategy to be able to change
        # db type easily
        self.clear()
        conn = self._connexion
        if conn is None :
            return

        for group in conn.getGroupsMemberOf():
            row_group = group_to_items(group)
            self.appendRow(row_group)

            conn.SERVICE_OPTS.setOmeroGroup(group.getId())

            for project in conn.listProjects():
                row_project = project_to_items(project)
                row_group[0].appendRow(row_project)
                for dataset in project.listChildren():
                    row_dataset = dataset_to_items(dataset)
                    row_project[0].appendRow(row_dataset)
                    for image in dataset.listChildren():
                        row_img = image_to_items(image)
                        row_dataset[0].appendRow(row_img)

            for dataset in conn.listOrphans('Dataset'):
                row_dataset = dataset_to_items(dataset)
                row_group[0].appendRow(row_dataset)
                for image in dataset.listChildren():
                    row_img = image_to_items(image)
                    row_dataset[0].appendRow(row_img)

            for image in conn.listOrphans('Image'):
                row_img = image_to_items(image)
                row_group[0].appendRow(row_img)

        self.setColumnCount(4)
        conn.SERVICE_OPTS.setOmeroGroup(-1)

    def omeroObject(self, idx):
        item = self.itemFromIndex(idx)
        parent = item.parent()
        if parent :
            item = parent.child
        else :
            item = self.item

        data_type = str(item(idx.row(), 1).text()).capitalize()
        data_id = int(item(idx.row(), 2).text())
        if data_type == 'Group' :
            return None
        else :
            return self._connexion.getObject(data_type, data_id)

class OmeroView(QtGui.QTreeView):
    objectSelected = Signal(object)
    imageSelected = Signal(object)

    def __init__(self):
        QtGui.QTreeView.__init__(self)

        self.setEditTriggers(QtGui.QTreeView.NoEditTriggers)
        self.setIconSize(QtCore.QSize(50, 50))
        self.fineTune()

    def fineTune(self):
        for icol in range(4):
            self.resizeColumnToContents(icol)
        self.expandAll()

    def currentChanged(self, current, previous):
        obj = self.model().omeroObject(current)
        self.objectSelected.emit(obj)
        if obj.__class__.__name__ == '_ImageWrapper' :
            self.imageSelected.emit(obj)


class OmeroDbBrowser(QtGui.QWidget):
    objectSelected = Signal(object)
    imageSelected = Signal(object)

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.view = OmeroView()
        self.model = OmeroModel()
        self.view.setModel(self.model)

        self.grid = QtGui.QGridLayout(self)
        self.grid.addWidget(self.view, 0, 0)

        self.resize(QtCore.QSize(800, 600))

        self.view.objectSelected.connect(self.objectSelected.emit)
        self.view.imageSelected.connect(self.imageSelected.emit)

    def setConnection(self, omero_connexion):
        self.model.setConnection(omero_connexion)
        titles = ['Category', 'Name', 'Id', 'Image']
        self.model.setHorizontalHeaderLabels(titles)


if __name__ == '__main__' :
    import sys
    app = QtGui.QApplication.instance()
    if app :
        EMBEDED = True
    else :
        EMBEDED = False
        app = QtGui.QApplication(sys.argv)

    from omero.gateway import BlitzGateway
    conn = BlitzGateway('gbaty', 'gbaty', host='localhost', port=4064)
    conn.connect()

    def f(obj):
        print 'image:', obj

    w = OmeroDbBrowser()
    w.imageSelected.connect(f)
    w.setConnection(conn)
    w.show()

    if not EMBEDED :
        app.exec_()

    conn._closeSession()
