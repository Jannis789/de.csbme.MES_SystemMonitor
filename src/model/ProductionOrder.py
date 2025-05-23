from gi.repository import GObject


class ProductionOrderModel(GObject.Object):
    """produced_units, status, efficiency is optional, since it should be set initially to 0 or 'Initial'"""
    
    def __init__(
        self,
        name: str,
        order_number: str,
        units: int,
        produced_units: int = 0,
        status: str = "Initial",
        efficiency: float = 0.0,
    ):
        super().__init__()
        self._name = name
        self._order_number = order_number
        self._units = units
        self._produced_units = produced_units
        self._status = status
        self._efficiency = efficiency

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.notify("name")

    @GObject.Property(type=str)
    def order_number(self):
        return self._order_number

    @order_number.setter
    def order_number(self, value):
        self._order_number = value
        self.notify("order_number")

    @GObject.Property(type=int)
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value
        self.notify("units")

    @GObject.Property(type=int)
    def produced_units(self):
        return self._produced_units

    @produced_units.setter
    def produced_units(self, value):
        self._produced_units = value
        self.notify("produced_units")

    @GObject.Property(type=str)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.notify("status")

    @GObject.Property(type=float)
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        self._efficiency = value
        self.notify("efficiency")