from gi.repository import Adw, Gtk, GObject

from ..model.ProductionLines import ProductionLineModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/production-line-details.ui')
class ProductionLineDetails(Adw.NavigationPage):
    __gtype_name__ = 'ProductionLineDetails'
    __gsignals__ = {
        "open-production-order": (GObject.SIGNAL_RUN_FIRST, None, (ProductionLineModel, bool)),
    }
    
    page_tag: str = 'production-line-details'
    
    column_view: Gtk.ColumnView = Gtk.Template.Child()
    headerbar_title_label: Gtk.Label = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.current_item: ProductionLineModel = None
        
        # The title is not appended but replaced this way
        self.headerbar_title_default = self.headerbar_title_label.get_label()
        
        self.add_button.connect("clicked", self._on_add_button_clicked)
        
        
    def set_page_title(self, title: str):
        self.headerbar_title_label.set_label(self.headerbar_title_default + f"{title}")
        
    def open_with(self, item: ProductionLineModel):
        """Opens the content of the production line, which are at the time only ProductionOrders."""
        pass # TODO: Implement this method
        # self.emit("open-production-order", self.current_item, create_new=False)
    
    def _on_add_button_clicked(self, button):
        """Open the new product line popup."""
        self.emit("open-production-order", self.current_item, True)