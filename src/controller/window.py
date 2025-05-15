from gi.repository import Adw, Gtk, Gio, Gdk

from .Produktionslinie import ProduktionslinienController, ProduktionslinienModell

# @TODO: move to css file
_CSS = """
.ColumnView > header {
  font-size: 18px;
  font-weight: 400;
}
* {
    font-family: "Adwaita Mono Nerd Font";
}
"""

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'
    column_view: Gtk.ColumnView = Gtk.Template.Child()
    scrolled_window: Gtk.ScrolledWindow = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()
    root_page: Adw.NavigationPage = Gtk.Template.Child()
    detail_page: Adw.NavigationPage = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.produktionslinien_controller = ProduktionslinienController()
        self.add_button.connect('clicked', self._on_add_button_clicked)

        self._initialize_column_view()
        self._load_css()
    
    def _initialize_column_view(self):
        """Set up the column view and populate it with dummy data."""
        self.produktionslinien_controller.initialize(self.column_view) 

        # Create dummy data for the column view
        data_model = Gio.ListStore(item_type=ProduktionslinienModell)
        # @TODO: fetch from db
        for line in []:
            data_model.append(line)
            
        self.produktionslinien_controller.fill_column_view(data_model)

    def _on_add_button_clicked(self, _button):
        """Open a dialog to add a new Produktionslinie"""
        dialog = NewProduktionslinieDialog(self.produktionslinien_controller)
        dialog.present(self)
        
    def _load_css(self):
        style = self.get_style_context()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        provider = Gtk.CssProvider()
        try:
            provider.load_from_data(_CSS.encode())
        except Exception as e:
            raise RuntimeError(f"Failed to load CSS: {e}")
        display = Gdk.Display.get_default()
        style.add_provider_for_display(display, provider, priority)

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/new-produktionslinie.ui')
class NewProduktionslinieDialog(Adw.Dialog):
    __gtype_name__ = 'DialogPopUp'

    entry: Gtk.Entry = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, controller: ProduktionslinienController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.add_button.connect('clicked', self._on_add_button_clicked)

        # Ensure the "switch-page" signal is connected only once
        if not hasattr(self.controller, "_switch_page_connected"):
            self.controller.connect("switch-page", self._on_switch_page)
            self.controller._switch_page_connected = True

    def _on_add_button_clicked(self, _button):
        """Add a new Produktionslinie and close the dialog."""
        text = self.entry.get_text()
        plm = ProduktionslinienModell(name=text)
        self.controller.add_column(plm)
        self.close()

    def _on_switch_page(self, _sender, selected_item):
        """Handle switching to the detail view."""
        if isinstance(selected_item, ProduktionslinienModell):
            print(f"Switching to detail view for: {selected_item.name}")