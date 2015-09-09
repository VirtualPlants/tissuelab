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
from openalea.core.service.plugin import plugin_instance
from openalea.core.world import World
from openalea.image.serial.basics import imread
from openalea.oalab.cli.parser import CommandLineParser
from openalea.oalab.main import launch_lab
from openalea.oalab.plugin.builtin.lab.minilab import MiniLab


class PymageCommandLineParser(CommandLineParser):

    def __init__(self, session=None):
        CommandLineParser.__init__(self, session=session)
        self.parser.add_argument('images', metavar='images', nargs='*',
                                 help='Image to display in lab')
        self.parser.add_argument('--blend', action="store_true",
                                 help='Blend images two by two')

    def post_launch(self):
        if self.session.gui:
            world = World()

            lst = []
            for path in self.args.images:
                path = Path(path)
                image = imread(path)
                lst.append(path.namebase)
                world.add(image, name=path.namebase)

            if self.args.blend:
                from tissuelab.gui.vtkviewer.vtkworldviewer import ImageBlending
                for i in range(len(lst) / 2):
                    image1 = world[lst[i]]
                    image2 = world[lst[i + 1]]
                    blending = ImageBlending([image1, image2])
                    world.add(blending)


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
    label = 'PyMage'
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
