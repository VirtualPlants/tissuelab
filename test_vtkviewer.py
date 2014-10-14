
from openalea.vpltk.qt import QtCore, QtGui
from openalea.oalab.shell import get_shell_class
from openalea.core.interpreter import get_interpreter_class
from tissuelab.gui.vtkviewer import VtkViewerWidget

instance = QtGui.QApplication.instance()
if instance is None :
    app = QtGui.QApplication([])
else :
    app = instance


# Set interpreter
interpreter = get_interpreter_class()()
# Set Shell Widget

widget = QtGui.QWidget()
layout = QtGui.QHBoxLayout(widget)

shellwdgt = get_shell_class()(interpreter)
viewer = VtkViewerWidget()

layout.addWidget(viewer)
layout.addWidget(shellwdgt)

layout.setSpacing(0)
layout.setContentsMargins(0, 0, 0, 0)

interpreter.locals['interp'] = interpreter
interpreter.locals.update(locals())

p = QtGui.QSizePolicy
shellwdgt.setSizePolicy(p(p.Maximum, p.MinimumExpanding))

widget.show()
widget.raise_()


if instance is None :
    app.exec_()


