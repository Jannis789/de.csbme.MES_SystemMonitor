from gi.repository import GObject

class ProductionLineModel(GObject.Object):
    def __init__(self, name: str):
        super().__init__()
        self._name = name  

    @GObject.Property(type=str)
    def name(self):
        """Get the name of the ProductionLine."""
        return self._name