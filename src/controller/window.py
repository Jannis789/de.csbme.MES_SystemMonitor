
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk

from .Produktionslinie import ProduktionslinienController, ProduktionslinienModell


_COLUMN_VIEW_OVERRIDE = """
.ColumnView > header {
  font-size: 18px;
  font-weight: 900;
}"""


@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/window.ui')
class MesMonitorWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MesMonitorWindow'
    column_view: Gtk.ColumnView = Gtk.Template.Child()
    scrolled_window: Gtk.ScrolledWindow = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_button.add_controller(Gtk.GestureClick.new())
        self.add_button.connect('clicked', self.on_add_button_clicked)

        self.instanciate_column_view()
        self.load_css()
    
    def instanciate_column_view(self):
        self.produktionslinien_controller = ProduktionslinienController(self.column_view)    
    
        """create Dummy data for the column view"""
        data_model = Gio.ListStore(item_type=ProduktionslinienModell)
        for line in [
            ProduktionslinienModell(name="Produktionslinie 1"),
            ProduktionslinienModell(name="Produktionslinie 2"),
            ProduktionslinienModell(name="Produktionslinie 3"),
        ]:
            data_model.append(line)
            
        self.produktionslinien_controller.fill_column_view(data_model)

    def on_add_button_clicked(self, button):
        """Add a new Produktionslinie to the column view"""
        print("Add button clicked")
        
    def load_css(self):
        style = self.get_style_context()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        provider = Gtk.CssProvider()
        try:
            provider.load_from_data(_COLUMN_VIEW_OVERRIDE, -1)
        except Exception:
            provider.load_from_data(bytes(_COLUMN_VIEW_OVERRIDE.encode()))
        display = Gdk.Display.get_default()
        style.add_provider_for_display(display, provider, priority)
