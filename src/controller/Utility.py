import gi
from gi.repository import Gtk, Gdk

class Utility:
    """
    A utility class providing helper methods for common operations.
    """

    @staticmethod
    def gesture_emit_double_click(gesture: Gtk.GestureClick, callback):
        Gtk.Settings.get_default().get_property("gtk-double-click-time")
        gesture.connect("released", lambda *_: print("pressed"))