# -*- coding: utf-8 -*-
# -*- python -*-
#
#       TissueLab
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       TissueLab Website : http://virtualplants.github.io/
#
###############################################################################

__all__ = ['OmeroDbBrowser', 'OmeroModel', 'OmeroView']

from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.qt.QtCore import Signal


def image_to_items(image):
    item_type_image = QtGui.QStandardItem('image')
    item_image = QtGui.QStandardItem(image.getName())
    item_id = QtGui.QStandardItem(unicode(image.getId()))
    item_thumbnail = QtGui.QStandardItem()

    item_image.setData(image)

    img_data = image.getThumbnail()
    pixmap = QtGui.QPixmap()
    if pixmap.loadFromData(img_data, "JPEG"):
        item_thumbnail.setIcon(QtGui.QIcon(pixmap))
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
        self._connection = None
        self._data = []

        QtGui.QStandardItemModel.__init__(self)

    def setConnection(self, omero_connection):
        self._connection = omero_connection
        self.refresh()

    def refresh(self):
        # Here we should use a backend strategy to be able to change
        # db type easily
        self.clear()
        conn = self._connection
        if conn is None:
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
        if parent:
            item = parent.child
        else:
            item = self.item

        data_type = str(item(idx.row(), 1).text()).capitalize()
        data_id = int(item(idx.row(), 2).text())
        if data_type == 'Group':
            return None
        else:
            return self._connection.getObject(data_type, data_id)


class OmeroView(QtGui.QTreeView):
    objectSelected = Signal(object)
    imageSelected = Signal(object)

    def __init__(self):
        QtGui.QTreeView.__init__(self)

        self.setEditTriggers(QtGui.QTreeView.NoEditTriggers)

        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self.setIconSize(QtCore.QSize(50, 50))
        self.fineTune()

    def setClient(self, omeroClient):
        self.client = omeroClient

    def fineTune(self):
        self.expandAll()
        for icol in range(4):
            self.resizeColumnToContents(icol)
        titles = ['Category', 'Name', 'Id', 'Image']
        if self.model():
            self.model().setHorizontalHeaderLabels(titles)

    def currentChanged(self, current, previous):
        try:
            obj = self.model().omeroObject(current)
            self.objectSelected.emit(obj)
            if obj.__class__.__name__ == '_ImageWrapper':
                self.imageSelected.emit(obj)
        except:
            print "connection problem ?, reconnect"
            self.client.reconnect()

    # Drag and drop

    def startDrag(self, supportedActions):
        from openalea.core.service.mimetype import encode
        index = self.selectedIndexes()
        obj = self.model().omeroObject(index[0])
        conn = self.model()._connection

        uri = '%(NAME)s = omero://%(USER)s@%(HOST)s:%(PORT)s/id=%(ID)s' % dict(
            USER=conn._ic_props['omero.user'],
            PORT=conn.port,
            HOST=conn.host,
            NAME=obj.getName(),
            ID=obj.getId(),
        )

        mimetype, mimedata = encode(uri, mimetype='openalealab/omero')
        qmime_data = QtCore.QMimeData()
        qmime_data.setData(mimetype, mimedata)
        qmime_data.setText(obj.getName())
        drag = QtGui.QDrag(self)
        drag.setMimeData(qmime_data)
        drag.start()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalealab/omero"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("openalealab/omero"):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        event.ignore()


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

    def setConnection(self, omero_connection):
        self.model.setConnection(omero_connection)
        self.view.fineTune()

    def setClient(self, omeroClient):
        self.client = omeroClient
        self.view.setClient(omeroClient)

if __name__ == '__main__':
    import sys
    import tissuelab.omero
    app = QtGui.QApplication.instance()
    if app:
        EMBEDED = True
    else:
        EMBEDED = False
        app = QtGui.QApplication(sys.argv)

    from omero.gateway import BlitzGateway
    conn = BlitzGateway('root', 'omero', host='localhost', port=4064)
    conn.connect()

    def f(obj):
        print 'image:', obj

    w = OmeroDbBrowser()
    w.imageSelected.connect(f)
    w.setConnection(conn)
    w.show()

    if not EMBEDED:
        app.exec_()

    conn._closeSession()
