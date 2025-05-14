from gi.repository import Gtk, Gio  # Added Gio import
from gi.repository import GObject


class ProduktionslinienController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProduktionslinienController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, column_view: Gtk.ColumnView = None):
        if self._initialized:
            return
        self.column_view = column_view
        self.model = None  # Store the ListStore model
        self._initialized = True

    def fill_column_view(self, produktionslinien: Gio.ListStore):
        self.model = produktionslinien  # Save reference to model
        self.column_view.set_model(Gtk.SingleSelection(model=produktionslinien))

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)

        column = Gtk.ColumnViewColumn(title="Name", factory=factory)
        column.set_expand(True)
        column.set_resizable(True)
        self.column_view.append_column(column)

    def add_column(self, plm: 'ProduktionslinienModell'):
        # Add a new row/item to the model instead of a column
        if self.model is not None:
            self.model.append(plm)

    def _on_factory_setup(self, factory, list_item):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        box.append(label)
        gesture = Gtk.GestureClick.new()
        gesture.connect("pressed", self._on_column_view_column_pressed)
        box.add_controller(gesture)
        list_item.set_child(box)

    def _on_factory_bind(self, factory, list_item):
        item = list_item.get_item()
        box = list_item.get_child()
        if box is not None:
            label = box.get_first_child()
            if label is not None:
                label.set_text(item.name)

    def _on_column_view_column_pressed(self, gesture, n_press, x, y):
        print("Column view item pressed")


class ProduktionslinienModell(GObject.Object):
    def __init__(self, name: str):
        super().__init__()
        self._name = name  # Initialize the name property

    @GObject.Property(type=str)
    def name(self):
        return self._name


