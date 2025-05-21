from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/production-lines-overlay.ui')
class ProductionLinesOverlay(Adw.NavigationPage):
    __gtype_name__ = 'ProductionLinesOverlay'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
