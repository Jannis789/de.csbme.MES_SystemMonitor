from gi.repository import Adw, Gtk, GObject

from ..model.ProductionOrder import ProductionOrderModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/add-production-order-page.ui')
class AddProductionOrderPage(Adw.NavigationPage):
    __gtype_name__ = 'AddProductionOrderPage'
    __gsignals__ = {
        "add-production-order": (GObject.SIGNAL_RUN_FIRST, None, (ProductionOrderModel,)),
        "remove-production-order": (GObject.SIGNAL_RUN_FIRST, None, (ProductionOrderModel,)),
    }
    
    page_tag: str = 'add-production-order-page'

    save_button: Gtk.Button = Gtk.Template.Child()
    
    unavailable_names = set()
    unavailable_order_numbers = set()
    
    # relevant if creating a new production order
    order_number_entry: Adw.EntryRow = Gtk.Template.Child()
    name_entry: Adw.EntryRow = Gtk.Template.Child()
    unit_entry: Adw.EntryRow = Gtk.Template.Child()
    
    # need real time updates
    status_row: Adw.ActionRow = Gtk.Template.Child()
    produced_units_row: Adw.ActionRow = Gtk.Template.Child()
    efficiency_row: Adw.ActionRow = Gtk.Template.Child()

    delete_button: Gtk.Button = Gtk.Template.Child()
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
       
        self.save_button.connect("clicked", self._on_save_button_clicked)
        self.delete_button.connect("clicked", self._on_delete_button_clicked)  # <-- hinzugefügt
        self.editable = False # only initially
        self._current_item_name = None
        self._current_item_order_number = None
        self._current_order = None
       
    def _on_save_button_clicked(self, button):
        """Open the new product line popup."""
        
        order_number = self.order_number_entry.get_text()
        name = self.name_entry.get_text()
        units = self.unit_entry.get_text()
        
        unavailable_names = self.unavailable_names.copy()
        unavailable_order_numbers = self.unavailable_order_numbers.copy()

        error_message = None
        
        if not name:
            error_message = "Bitte geben Sie einen Namen ein."
        elif name in unavailable_names and not self.editable:
            error_message = "Der Name ist bereits vergeben."
        elif not order_number:
            error_message = "Bitte geben Sie eine Auftragsnummer ein."
        elif not order_number.isdigit() or int(order_number) <= 0:
            error_message = "Die Auftragsnummer muss eine positive Zahl sein."
        elif int(order_number) in {int(x) for x in unavailable_order_numbers} and not self.editable:
            error_message = "Die Auftragsnummer ist bereits vergeben."
        elif not units:
            error_message = "Bitte geben Sie die Stückzahl ein."
        elif not units.isdigit() or int(units) <= 0:
            error_message = "Die Stückzahl muss eine positive Zahl sein."

        if error_message:
            dialog = Adw.AlertDialog.new(
                heading="Ungültige Eingabe",
                body=error_message
            )
            dialog.add_response("close", "Schließen")
            dialog.set_close_response("close")
            dialog.set_default_response("close")
            dialog.present(self.get_root())
            return
        if not self.editable:
            order = ProductionOrderModel(
                name=name,
                order_number=int(order_number),
                units=int(units) 
            )
            self._current_order = order
        else:
            self._current_order.name = name
            self._current_order.order_number = int(order_number)
            self._current_order.units = int(units)
        
        self.unavailable_names.add(name)
        self.unavailable_order_numbers.add(str(order_number))
        
        self.emit("add-production-order", self._current_order)

    def fill_content(self, order: ProductionOrderModel):
        """Fills the input fields with the data of an existing production order, or with empty values if a new Order should be created."""
        if order is None:
            # Felder leeren, falls kein Auftrag übergeben wurde
            self.order_number_entry.set_text("")
            self.name_entry.set_text("")
            self.unit_entry.set_text("")
            self.status_row.set_subtitle("Initial")
            self.produced_units_row.set_subtitle("0 / 0")
            self.efficiency_row.set_subtitle("0 %")
            self.editable = False
            self._current_item_name = None
            self._current_item_order_number = None
            self._current_order = None
            self.delete_button.set_visible(False)
            return
        
        self.delete_button.set_visible(True)
        
        self.order_number_entry.set_text(str(order.order_number))
        self.name_entry.set_text(str(order.name))
        self.unit_entry.set_text(str(order.units))
        self.status_row.set_subtitle(str(order.status))
        self.produced_units_row.set_subtitle(f"{order.units_string}")
        self.efficiency_row.set_subtitle(f"{order.efficiency:.0f} %")
        self.unavailable_names.add(order.name)
        self.unavailable_order_numbers.add(str(order.order_number))
        self._current_item_name = order.name
        self._current_item_order_number = order.order_number
        self._current_order = order

        order.bind_property("name", self.name_entry, "text", GObject.BindingFlags.SYNC_CREATE)
        order.bind_property(
            "order_number",
            self.order_number_entry,
            "text",
            GObject.BindingFlags.SYNC_CREATE,
        )
        order.bind_property(
            "units",
            self.unit_entry,
            "text",
            GObject.BindingFlags.SYNC_CREATE,
        )
        order.bind_property("status", self.status_row, "subtitle", GObject.BindingFlags.SYNC_CREATE)
        order.bind_property("units_string", self.produced_units_row, "subtitle", GObject.BindingFlags.SYNC_CREATE)
        order.bind_property(
            "efficiency",
            self.efficiency_row,
            "subtitle",
            GObject.BindingFlags.SYNC_CREATE,
            transform_to=lambda obj, value, *args: f"{value:.0f} %"
        )
        self.editable = True

    def _on_delete_button_clicked(self, button):
        """Löscht den aktuellen Auftrag aus den Eingabefeldern und entfernt ihn aus den unavailable Sets."""
        if self._current_item_name:
            self.unavailable_names.discard(self._current_item_name)
        if self._current_item_order_number:
            self.unavailable_order_numbers.discard(str(self._current_item_order_number))
        self.emit("remove-production-order", self._current_order)
        self.fill_content(None)