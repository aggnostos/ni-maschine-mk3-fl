# name=NI Maschine MK3 by Aggnostos


from controller import Controller


controller = Controller()


def OnInit() -> None:
    """
    Called when FL Studio initializes the script.

    Note that the script may be kept in memory after being de-initialized with OnDeInit(),
    so this function may be called more than once during the lifetime of this Python script.
    """
    controller.OnInit()


def OnDeInit() -> None:
    """
    Called before FL Studio de-initializes the script.

    This function should be used to shut down the attached device
    """
    controller.OnDeInit()


def OnRefresh(flags: int) -> None:
    """
    Called when certain events occur within FL Studio. Scripts should use the provided flags to update required interfaces on their associated controllers.
    flags values will be a bitwise combination of the OnRefresh flags.

    Args:
        flags (int): flags to represent the changes in FL Studio's state.
    """
    controller.OnRefresh(flags)
