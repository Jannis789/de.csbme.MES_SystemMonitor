from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk

from .Produktionslinie import ProduktionslinienController, ProduktionslinienModell


_COLUMN_VIEW_OVERRIDE = """
.ColumnView > header {
  font-size: 18px;
  font-weight: 400;
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
        # @TODO: fetch from db
        for line in []:
            data_model.append(line)
            
        self.produktionslinien_controller.fill_column_view(data_model)

    def on_add_button_clicked(self, _button):
        """Add a new Produktionslinie to the column view"""
        dialog = NewProduktionslinieDialog()
        dialog.present(self)
        
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

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/new-produktionslinie.ui')
class NewProduktionslinieDialog(Adw.Dialog):
    __gtype_name__ = 'DialogPopUp'

    entry: Gtk.Entry = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_button.connect('clicked', self.on_add_button_clicked)

    def on_add_button_clicked(self, _button):
        text = self.entry.get_text()
        plm = ProduktionslinienModell(name=text)
        ProduktionslinienController().add_column(plm)
        self.close()