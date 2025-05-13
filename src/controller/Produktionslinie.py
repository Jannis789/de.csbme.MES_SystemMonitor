from gi.repository import Gtk, Gio  # Added Gio import
from gi.repository import GObject


class ProduktionslinienController:
    def __init__(self, column_view: Gtk.ColumnView):
        self.column_view = column_view

    def fill_column_view(self, produktionslinien: Gio.ListStore):

        self.column_view.set_model(Gtk.SingleSelection(model=produktionslinien))

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)

        """ Maybe someday we need to solve this with a dynamic Class generation"""
        column = Gtk.ColumnViewColumn(title="Name", factory=factory)
        column.set_expand(True)
        column.set_resizable(True)
        self.column_view.append_column(column)

    def _on_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        # label.add_css_class("title-2")
        list_item.set_child(label)

    def _on_factory_bind(self, factory, list_item):
        # Bind the label to the item's name property
        item = list_item.get_item()
        list_item.get_child().set_text(item.name)
            


class ProduktionslinienModell(GObject.Object):
    def __init__(self, name: str):
        super().__init__()
        self._name = name  # Initialize the name property

    @GObject.Property(type=str)
    def name(self):
        return self._name


