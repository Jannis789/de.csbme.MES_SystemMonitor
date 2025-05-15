from gi.repository import Gtk, Gio, GObject

class ProduktionslinienController(GObject.Object): 
    __gsignals__ = {
        "switch-page": (GObject.SIGNAL_RUN_FIRST, None, (object,))
    }

    def __init__(self, column_view: Gtk.ColumnView = None):
        super().__init__()
        self.column_view = column_view
        self.model = None
        self._initialized = False

    def initialize(self, column_view: Gtk.ColumnView):
        print(self._initialized)
        """Initialize the controller with a Gtk.ColumnView."""
        if not self._initialized:
            self.column_view = column_view
            column_view.connect("activate", self._on_column_click)
            self._initialized = True

    def fill_column_view(self, produktionslinien: Gio.ListStore):
        """Populate the column view with data from a Gio.ListStore."""
        self.model = produktionslinien
        self.column_view.set_model(Gtk.SingleSelection(model=produktionslinien))

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)

        column = Gtk.ColumnViewColumn(
            title="Name", factory=factory, expand=True, resizable=True
        )
        self.column_view.append_column(column)

    def add_column(self, plm: 'ProduktionslinienModell'):
        """Add a new item to the model."""
        if self.model is not None:
            self.model.append(plm)

    def _on_factory_setup(self, factory, list_item: Gtk.ColumnViewCell):
        """Set up the list item for the column view."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label()
        box.append(label)
        list_item.set_child(box)  # Set the box (not label) as the child
        self.column_view.connect("activate", lambda view, index: self._on_column_click(view, index, self.model.get_item(index)))

    def _on_factory_bind(self, factory, list_item: Gtk.ColumnViewCell):
        """Bind data to the list item."""
        item: 'ProduktionslinienModell' = list_item.get_item()
        box = list_item.get_child()
        label = box.get_first_child()
        label.set_text(item.name)

    def _on_column_click(self, column_view: Gtk.ColumnView, index: int, item: 'ProduktionslinienModell'):
        print(f"ref: {item.name}")


class ProduktionslinienModell(GObject.Object):
    def __init__(self, name: str):
        super().__init__()
        self._name = name  

    @GObject.Property(type=str)
    def name(self):
        """Get the name of the Produktionslinie."""
        return self._name


