from gi.repository import Adw, Gtk, GObject

from ..model.ProductionOrder import ProductionOrderModel

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/add-production-order-page.ui')
class AddProductionOrderPage(Adw.NavigationPage):
    __gtype_name__ = 'AddProductionOrderPage'
    __gsignals__ = {
        "add-production-order": (GObject.SIGNAL_RUN_FIRST, None, (ProductionOrderModel,)),
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
    
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       
       self.save_button.connect("clicked", self._on_save_button_clicked)
       
    def _on_save_button_clicked(self, button):
        """Open the new product line popup."""
        
        order_number = self.order_number_entry.get_text()
        name = self.name_entry.get_text()
        units = self.unit_entry.get_text()
        
        error_message = None
        
        if not name:
            error_message = "Bitte geben Sie einen Namen ein."
        elif name in self.unavailable_names:
            error_message = "Der Name ist bereits vergeben."
        elif not order_number:
            error_message = "Bitte geben Sie eine Auftragsnummer ein."
        elif not order_number.isdigit() or int(order_number) <= 0:
            error_message = "Die Auftragsnummer muss eine positive Zahl sein."
        elif order_number in self.unavailable_order_numbers:
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

        order = ProductionOrderModel(
            name=name,
            order_number=order_number,
            units=units
        )
        self.emit("add-production-order", order)

    def fill_content(self, order: ProductionOrderModel):
        """Füllt die Eingabefelder mit den Daten eines bestehenden Produktionsauftrags."""
        if order is None:
            # Felder leeren, falls kein Auftrag übergeben wurde
            self.order_number_entry.set_text("")
            self.name_entry.set_text("")
            self.unit_entry.set_text("")
            self.status_row.set_subtitle("Initial")
            self.produced_units_row.set_subtitle("0 / 0")
            self.efficiency_row.set_subtitle("0 %")
            return

        self.order_number_entry.set_text(str(order.order_number))
        self.name_entry.set_text(str(order.name))
        self.unit_entry.set_text(str(order.units))
        self.status_row.set_subtitle(str(order.status))
        self.produced_units_row.set_subtitle(f"{order.produced_units} / {order.units}")
        self.efficiency_row.set_subtitle(f"{order.efficiency:.0f} %")