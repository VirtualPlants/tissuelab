# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
import sys
from openalea.vpltk.qt import QtGui

from openalea.core.path import path as Path
from openalea.oalab.cli.parser import CommandLineParser
from openalea.oalab.plugins.labs.minilab import MiniLab
from openalea.oalab.main2 import launch_lab
from openalea.oalab.world import World

from openalea.core.service.plugin import plugin_instance

from openalea.image.serial.basics import imread


class PymageCommandLineParser(CommandLineParser):

    def __init__(self, session=None):
        CommandLineParser.__init__(self, session=session)
        self.parser.add_argument('images', metavar='images', nargs='+',
                                 help='Image to display in lab')

    def post_launch(self):
        if self.session.gui:
            world = World()
            viewer = plugin_instance('oalab.applet', 'TissueViewer')
            #viewer.vtk.set_world(world)
            #viewer.vtk.refresh()
            #viewer.show()

            for path in self.args.images:
                path = Path(path)
                image = imread(path)
                world.add(image, name=path.namebase)


class Pymage(MiniLab):

    layout = {
        "children": {"0": [9, 10]},
        "interface": "ISplittableUi",
        "parents": {"0": None, "9": 0, "10": 0},
        "properties": {"0": {"amount": 0.4, "splitDirection": 1},
                       "9": {"widget": {"applets": [{"name": "WorldControl", }], }},
                       "10": {"widget": {"applets": [{"name": "TissueViewer", "properties": {"toolbar": True}}], }},
                       }
    }

    name = 'pymage'
    alias = 'PyMage'
    icon = 'icon_tissuelab.png'


def main():
    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication(sys.argv)
    else:
        app = instance

    class Session(object):
        pass

    session = Session()
    cli = PymageCommandLineParser(session=session)
    cli.parse()

    if session.gui is True:

        win = launch_lab(Pymage)

        if instance is None and win:
            cli.post_launch()
            app.exec_()

if(__name__ == "__main__"):
    main()
