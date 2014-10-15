
class TissueLab(object):
    name = 'tissue'

    applets = [
        'ProjectManager',
        'ControlManager',
        'PkgManagerWidget',
        'EditorManager',
        'VtkViewer',
        'Viewer3D',
        'OmeroClient',
        'HelpWidget',
        'Logger',
        'HistoryWidget',
        'World',
        'LineageViewer',
    ]

    def __call__(self, mainwin):
        # Load, create and place applets in mainwindow
        for name in self.applets:
            mainwin.add_plugin(name=name)
        # Initialize all applets
        mainwin.initialize()
