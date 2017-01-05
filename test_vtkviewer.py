from Qt import QtWidgets

from openalea.oalab.shell import get_shell_class
from openalea.core.interpreter import get_interpreter_class
from tissuelab.gui.vtkviewer import VtkViewerWidget

instance = QtWidgets.QApplication.instance()
if instance is None :
    app = QtWidgets.QApplication([])
else :
    app = instance


# Set interpreter
interpreter = get_interpreter_class()()
# Set Shell Widget

widget = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout(widget)

shellwdgt = get_shell_class()(interpreter)
viewer = VtkViewerWidget()

layout.addWidget(viewer)
layout.addWidget(shellwdgt)

layout.setSpacing(0)
layout.setContentsMargins(0, 0, 0, 0)

interpreter.locals['interp'] = interpreter
interpreter.locals.update(locals())

p = QtWidgets.QSizePolicy
shellwdgt.setSizePolicy(p(p.Maximum, p.MinimumExpanding))

widget.show()
widget.raise_()


if instance is None :
    app.exec_()
