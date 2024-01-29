from typing import List

from pyguilib.components.layouts.pygui_layout_style import PyGuiLayoutStyle
from pyguilib.components.pygui_instance import PyGuiInstance


class PyGuiGridLayout(PyGuiLayoutStyle):
    def __init__(self, **kwargs) -> "PyGuiGridLayout":
        super(PyGuiGridLayout, self).__init__(
            **kwargs,
            on_layout_applied=self.__on_layout_applied,
            on_layout_removed=self.__on_layout_removed,
            layout_order_manager=self.__layout_order_manager,
        )

    def __on_layout_applied(self):
        pass

    def __on_layout_removed(self):
        pass

    def __layout_order_manager(self, childs: List[PyGuiInstance]):
        pass
