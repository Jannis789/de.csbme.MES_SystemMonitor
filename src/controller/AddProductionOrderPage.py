from gi.repository import Adw, Gtk, GObject

from ..model.ProductionLines import ProductionLineModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/add-production-order-page.ui')
class AddProductionOrderPage(Adw.NavigationPage):
    __gtype_name__ = 'AddProductionOrderPage'
    __gsignals__ = {
        "add-production-order": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }
    
    page_tag: str = 'add-production-order-page'

    save_button: Gtk.Button = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
       super().__init__(**kwargs)