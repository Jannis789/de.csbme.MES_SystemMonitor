from gi.repository import Adw, Gtk

from .ProductionLinesOverlay import ProductionLinesOverlay
from .ProductionLineDetails import ProductionLineDetails
from .AddProductionLineDialog import AddProductionLineDialog
from .AddProductionOrderPage import AddProductionOrderPage
from ..model.ProductionLines import ProductionLineModel
from ..model.ProductionOrder import ProductionOrderModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'

    navigation_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ================= Initialize Views ================= #
        
        # Create ProductionLinesOverlay 
        self.production_lines_overlay = ProductionLinesOverlay()
        self.navigation_view.add(self.production_lines_overlay)
        
        # Create AddProductionLineDialog (Dialog to define a new production line)
        self.add_new_product_line_dialog = AddProductionLineDialog()
        
        # Create ProductionLineDetails
        self.production_lines_details = ProductionLineDetails()
        self.navigation_view.add(self.production_lines_details)
        
        # Create AddProductionOrderPage
        self.add_production_order_page = AddProductionOrderPage()
        self.navigation_view.add(self.add_production_order_page)
        
        # ================= Connect Signals ================= #
        
        self.production_lines_overlay.connect("open-new-production-line-dialog", self._open_new_product_line_dialog)
        self.production_lines_overlay.connect("open-production-line", self._on_open_production_line)
        self.add_new_product_line_dialog.connect("add-production-line", self._on_add_production_line)
        self.production_lines_details.connect("open-production-order", self._on_open_production_order)
        self.add_production_order_page.connect("add-production-order", self._on_add_production_order)
        
    def _open_new_product_line_dialog(self, _widget: ProductionLinesOverlay):
        """Open the new product line popup."""
        self.add_new_product_line_dialog.present(self.get_root())
        
    def _on_add_production_line(self, widget, name):
        """Add a new product line to the list."""
        entry = ProductionLineModel(name=name)
        self.production_lines_overlay.store.append(entry)
        widget.close()

    def _on_open_production_line(self, _widget: ProductionLinesOverlay, _view: Gtk.ColumnView, _index: int, item: ProductionLineModel):
        print(f"Open production line: {item.name}")
        self.navigation_view.push_by_tag(self.production_lines_details.page_tag)
        self.production_lines_details.set_page_title(item.name)
        self.production_lines_details.open_with(item)
        
    def _on_open_production_order(self, _widget: ProductionLineDetails, item: ProductionLineModel, create_new: bool):
        self.navigation_view.push_by_tag(self.add_production_order_page.page_tag)
        
    def _on_add_production_order(self, _widget: AddProductionOrderPage, item: ProductionOrderModel):
        self.production_lines_details.current_item.production_orders.insert(0, item)