from gi.repository import Adw, Gtk, GObject, Gio
from typing import Optional

from ..model.ProductionLines import ProductionLineModel
from ..model.ProductionOrder import ProductionOrderModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/production-line-details.ui')
class ProductionLineDetails(Adw.NavigationPage):
    __gtype_name__ = 'ProductionLineDetails'
    __gsignals__ = {
        "open-production-order": (GObject.SIGNAL_RUN_FIRST, None, (object, bool)),
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
        self.column_view.connect("activate", self._on_column_activate)
        
        
    def set_page_title(self, title: str):
        self.headerbar_title_label.set_label(self.headerbar_title_default + f"{title}")
    
    def _on_add_button_clicked(self, button):
        """Open the new product line popup."""
        self.emit("open-production-order", self.current_item, True)
        
    def open_with(self, item: ProductionLineModel):
        """Opens the content of the production line, which are at the time only ProductionOrders."""
        self.current_item = item
        self._construct_factory()
        
    def _construct_factory(self):
        # Entferne alle bestehenden Spalten, um Duplikate zu vermeiden
        for column in list(self.column_view.get_columns()):
            self.column_view.remove_column(column)
        self.column_view.set_model(Gtk.SingleSelection(model=self.current_item.production_orders))

        def make_factory(attr):
            def setup(factory, list_item):
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                label = Gtk.Label()
                box.append(label)
                list_item.set_child(box)
            def bind(factory, list_item):
                item: ProductionOrderModel = list_item.get_item()
                box = list_item.get_child()
                label = box.get_first_child()
                label.set_text(str(getattr(item, attr)))
            factory = Gtk.SignalListItemFactory()
            factory.connect("setup", setup)
            factory.connect("bind", bind)
            return factory

        columns = [
            ("Auftragsname", "name", True),
            ("Auftragsnummer", "order_number", False),
            ("Einheiten", "units", False),
        ]
        for title, attr, expand in columns:
            factory = make_factory(attr)
            column = Gtk.ColumnViewColumn(
                title=title, factory=factory, expand=expand, resizable=True
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
        item: ProductionOrderModel = list_item.get_item()
        box = list_item.get_child()
        label = box.get_first_child()
        label.set_text(item.name)

    def _on_column_activate(self, view, index):
        selection = view.get_model()
        item = selection.get_selected_item()
        self.emit("open-production-order", item, False)