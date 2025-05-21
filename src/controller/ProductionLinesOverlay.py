from gi.repository import Adw, Gtk, Gio, GObject

from ..model.ProductionLines import ProductionLineModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/production-lines-overlay.ui')
class ProductionLinesOverlay(Adw.NavigationPage):
    __gtype_name__ = 'ProductionLinesOverlay'
    
    __gsignals__ = {
        "open-new-product-line-dialog": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "open-production-line": (GObject.SIGNAL_RUN_FIRST, None, (Gtk.ColumnView, int, ProductionLineModel)),
    }
    
    page_tag: str = 'production-lines-overlay'
    
    column_view: Gtk.ColumnView = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._construct_factory()
        self.column_view.connect("activate", self._on_column_activate)
        self.add_button.connect("clicked", lambda button: self.emit("open-new-product-line-dialog"))
        
    def _construct_factory(self):
        """Initializes the data model and sets up the column view with its columns and cell factories."""
        self.store = Gio.ListStore(item_type=ProductionLineModel)
        self.column_view.set_model(Gtk.SingleSelection(model=self.store))
        
        # Actions to when you append the column view
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)
        
        # Sets the head column's for the ColumnView
        column = Gtk.ColumnViewColumn(
            title="Name", factory=factory, expand=True, resizable=True
        )
        
        self.column_view.append_column(column)
        

    def _on_factory_setup(self, factory, list_item: Gtk.ColumnViewCell):
        """Set up the list item for the column view. Initial call"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label()
        box.append(label)
        list_item.set_child(box)  

    def _on_factory_bind(self, factory, list_item: Gtk.ColumnViewCell):
        """Bind data to the list item, when created or changed."""
        item: ProductionLineModel = list_item.get_item()
        box = list_item.get_child()
        label = box.get_first_child()
        label.set_text(item.name)

    def _on_column_activate(self, view, index):
        item = self.controller.model.get_item(index)
        self.emit("open-production-line", view, index, item)