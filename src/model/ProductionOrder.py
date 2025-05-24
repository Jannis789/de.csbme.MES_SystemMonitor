from gi.repository import GObject

from ..controller.Utility import Utility

class ProductionOrderModel(GObject.Object):
    """produced_units, status, efficiency is optional, since it should be set initially to 0 or 'Initial'"""

    __gtype_name__ = "ProductionOrderModel"
    def __init__(
        self,
        name: str,
        order_number: int,
        units: int,
        produced_units: int = 0,
        status: str = "Initial",
        efficiency: float = 0.0,
    ):
        super().__init__()
        self._name = name
        self._order_number = int(order_number)
        self._units = units
        self._produced_units = produced_units
        self._status = status
        self._efficiency = efficiency

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name != value:
            self._name = value
            self.notify("name")

    @GObject.Property(type=int)
    def order_number(self):
        return self._order_number

    @order_number.setter
    def order_number(self, value):
        value = int(value)
        if self._order_number != value:
            self._order_number = value
            self.notify("order_number")

    @GObject.Property(type=int)
    def units(self):
        return self._units

    @GObject.Property(type=str)
    def units_string(self):
        return f"{self.produced_units}/{self.units}"

    def notify_units_string(self):
        self.notify("units_string")

    @units.setter
    def units(self, value):
        if self._units != value:
            self._units = value
            self.notify("units")
            self.notify_units_string()

    @GObject.Property(type=int)
    def produced_units(self):
        return self._produced_units

    @produced_units.setter
    def produced_units(self, value):
        if self._produced_units != value:
            self._produced_units = value
            self.notify("produced_units")
            self.notify_units_string()
            if self._units >= self._produced_units:
                self.efficiency = Utility.calculate_efficiency(self._units, self._produced_units)

    @GObject.Property(type=str)
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if self._status != value:
            self._status = value
            self.notify("status")

    @GObject.Property(type=float)
    def efficiency(self):
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value):
        if self._efficiency != value:
            self._efficiency = value
            self.notify("efficiency")