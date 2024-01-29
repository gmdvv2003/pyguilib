from pyguilib.components.layouts.pygui_layout_container import PyGuiLayoutContainer
from pyguilib.components.pygui_instance import PyGuiInstance


class Frame(PyGuiInstance, PyGuiLayoutContainer):
    def __init__(self, **kwargs) -> "Frame":
        super(Frame, self).__init__(**kwargs)
