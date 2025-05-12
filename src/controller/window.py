
from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
