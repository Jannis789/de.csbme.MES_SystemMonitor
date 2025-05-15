import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject

class DataObject(GObject.GObject):

    __gtype_name__ = 'DataObject'

    text = GObject.Property(type=str, default=None)
    
    def __init__(self, text, number):
        
        super().__init__()

        self.text = text
        self.number = number
               

def setup_c1(widget, item):
    """Setup the widget to show in the Gtk.Listview"""
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    label = Gtk.Label()
    box.append(label)
    item.set_child(box)


def bind_c1(widget, item):
    """bind data from the store object to the widget"""
    label = item.get_child()
   
    obj = item.get_item()
    
    label.set_text(obj.text)
    label.bind_property("text", obj, "text")

    
def setup_c2(widget, item):
    """Setup the widget to show in the Gtk.Listview"""
    number = Gtk.Label()    
    item.set_child(number)


def bind_c2(widget, item):
    """bind data from the store object to the widget"""
    number = item.get_child()
    obj = item.get_item()   
    number.set_text(obj.number)

    
def on_activate(app):
    win = Gtk.ApplicationWindow(
        application=app,
        title="Gtk4 is Awesome !!!",
        default_height=400,
        default_width=400,
    )
    sw = Gtk.ScrolledWindow()
    list_view = Gtk.ColumnView()  
    factory_c1 = Gtk.SignalListItemFactory()
    factory_c1.connect("setup", setup_c1)
    factory_c1.connect("bind", bind_c1)
    
    factory_c2 = Gtk.SignalListItemFactory()
    factory_c2.connect("setup", setup_c2)
    factory_c2.connect("bind", bind_c2)    
    
    selection = Gtk.SingleSelection()
    
    store = Gio.ListStore.new(DataObject)  
    
    selection.set_model(store)
    
    list_view.set_model(selection)
    
    column1 = Gtk.ColumnViewColumn.new("column01", factory_c1)
    column2 = Gtk.ColumnViewColumn.new("column02", factory_c2)
    
    list_view.append_column(column1)
    list_view.append_column(column2)
    
    v1 = DataObject("entry", "02")
    v2 = DataObject("other", "33")
    
    store.append(v1)
    store.append(v2)  

    sw.set_child(list_view)
    win.set_child(sw)
    win.present()

app = Gtk.Application(application_id="org.gtk.Example")
app.connect("activate", on_activate)
app.run(None)