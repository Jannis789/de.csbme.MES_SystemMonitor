from gi.repository import GObject, Gio

from .ProductionOrder import ProductionOrderModel

class ProductionLineModel(GObject.Object):
    def __init__(self, name: str):
        super().__init__()
        self._name = name  
        self._production_orders = Gio.ListStore.new(ProductionOrderModel)

    @GObject.Property(type=str)
    def name(self):
        """Get the name of the ProductionLine."""
        return self._name

    @GObject.Property(type=Gio.ListStore)
    def production_orders(self):
        """Get the production orders associated with this ProductionLine."""
        return self._production_orders
    
    @production_orders.setter
    def production_orders(self, value: Gio.ListStore):
        if isinstance(value, Gio.ListStore):
            self._production_orders = value
        else:
            raise TypeError("production_orders must be a Gio.ListStore instance")
