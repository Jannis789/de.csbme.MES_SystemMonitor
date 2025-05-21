
from gi.repository import Adw, Gtk

from .ProductionLinesOverlay import ProductionLinesOverlay

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'

    navigation_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.production_lines_overlay = ProductionLinesOverlay()
        self.navigation_view.add(self.production_lines_overlay)
