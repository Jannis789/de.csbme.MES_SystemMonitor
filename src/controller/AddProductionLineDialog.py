from gi.repository import Adw, Gtk, GObject

@Gtk.Template(resource_path='/de/csbme/MES_SystemMonitor/view/add-product-line-dialog.ui')
class AddProductionLineDialog(Adw.Dialog):
    __gtype_name__ = 'AddProductionLineDialog'
    __gsignals__ = {
        'add-product-line': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }
    
    entry: Gtk.Entry = Gtk.Template.Child()
    add_button: Gtk.Button = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_button.connect('clicked', self.on_add_button_clicked)

    def validate_entry(self) -> bool:
        text = self.entry.get_text().strip()
        return len(text) > 1

    def on_add_button_clicked(self, button):
        if self.validate_entry():
            self.emit('add-product-line', self.entry.get_text())
            self.entry.set_text('')
        else:
            pass