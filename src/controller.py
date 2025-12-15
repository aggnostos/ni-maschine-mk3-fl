"""NI Maschine MK3 Controller abstract class"""

from src.colors import *
from src.controls import *


__all__ = ["Controller"]


class Controller:
    """Represents the state of the Maschine MK3 controller"""

    def __init__(self):
        pass

    def OnInit(self):
        """Initializes the controller state on script load/reload"""
        pass

    def OnDeInit(self):
        """De-initializes the controller state on script unload/reload"""
        pass

    def OnRefresh(self, flags: int):
        """Refreshes the controller state when FL Studio requests it"""
        pass
