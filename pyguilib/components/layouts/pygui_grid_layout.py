from typing import List

from pyguilib.components.layouts.pygui_layout_style import PyGuiLayoutStyle
from pyguilib.components.pygui_instance import PyGuiInstance


class PyGuiGridLayout(PyGuiLayoutStyle):
    """
    PyGuiGridLayout class represents a grid layout style for a PyGui instance.

    Inherits from:
        PyGuiLayoutStyle

    Args:
        **kwargs: Additional keyword arguments passed to the parent class constructor.
    """

    def __init__(self, **kwargs) -> "PyGuiGridLayout":
        super(PyGuiGridLayout, self).__init__(
            **kwargs,
            on_layout_applied=self.__on_layout_applied,
            on_layout_removed=self.__on_layout_removed,
            layout_order_manager=self.__layout_order_manager,
        )

    def __on_layout_applied(self):
        """
        Hook method called when the layout is applied.

        Note:
            This method can be overridden to provide specific behavior when the layout is applied.
        """
        pass

    def __on_layout_removed(self):
        """
        Hook method called when the layout is removed.

        Note:
            This method can be overridden to provide specific behavior when the layout is removed.
        """
        pass

    def __layout_order_manager(self, childs: List[PyGuiInstance]):
        """
        Method for managing the order of child elements.

        Args:
            childs (List[PyGuiInstance]): List of PyGuiInstance objects representing child elements.

        Note:
            This method can be overridden to define the order in which child elements should be laid out.
        """
        pass
