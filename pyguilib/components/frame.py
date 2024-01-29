from pyguilib.components.layouts.pygui_layout_container import PyGuiLayoutContainer
from pyguilib.components.pygui_instance import PyGuiInstance


class Frame(PyGuiInstance, PyGuiLayoutContainer):
    """
    Frame class representing a container with layout capabilities.

    Inherits from:
        PyGuiInstance
        PyGuiLayoutContainer

    Args:
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, **kwargs) -> "Frame":
        super(Frame, self).__init__(**kwargs)
