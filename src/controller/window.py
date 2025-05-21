
from gi.repository import Adw, Gtk

from .ProductionLinesOverlay import ProductionLinesOverlay
from .AddProductionLineDialog import AddProductionLineDialog
from ..model.ProductionLines import ProductionLineModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'

    navigation_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.production_lines_overlay = ProductionLinesOverlay()
        self.navigation_view.add(self.production_lines_overlay)
        self.add_new_product_line_dialog = AddProductionLineDialog()
        
        # ================= Connect Signals ================= #
        
        self.production_lines_overlay.connect("open-new-product-line-dialog", self._open_new_product_line_dialog)
        self.production_lines_overlay.connect("open-production-line", self._on_open_production_line)
        self.add_new_product_line_dialog.connect("add-product-line", self._on_add_product_line)
        
    def _open_new_product_line_dialog(self, *args):
        """Open the new product line popup."""
        self.add_new_product_line_dialog.present(self.get_root())
        
    def _on_add_product_line(self, widget, name):
        """Add a new product line to the list."""
        entry = ProductionLineModel(name=name)
        self.production_lines_overlay.store.append(entry)
        widget.close()
        
    def _on_open_production_line(self, widget, index, item):
        pass
