from typing import List

from pygame import Vector2

from pyguilib.components.layouts.pygui_layout_style import (
    HorizontalAlignment,
    PyGuiLayoutStyle,
    VerticalAlignment,
)
from pyguilib.components.pygui_instance import PyGuiInstance
from pyguilib.utilities.udim import UDim, UDim2


class PyGuiListLayout(PyGuiLayoutStyle):
    """
    PyGuiListLayout class represents a list layout style for a PyGui instance.

    Inherits from:
        PyGuiLayoutStyle

    Args:
        **kwargs: Additional keyword arguments passed to the parent class constructor.
    """

    def __init__(self, **kwargs) -> "PyGuiListLayout":
        super(PyGuiListLayout, self).__init__(
            **kwargs,
            on_layout_instance_child_added=self.__on_layout_instance_child_added,
            on_layout_instance_child_removed=self.__on_layout_instance_child_removed,
            on_layout_applied=self.__on_layout_applied,
            on_layout_removed=self.__on_layout_removed,
            layout_order_manager=self.__layout_order_manager,
        )

        self._horizontal_padding = kwargs.get("padding", UDim(0, 0))
        self._vertical_padding = kwargs.get("padding", UDim(0, 0))

        self._top_margin = kwargs.get("top_margin", UDim(0, 0))
        self._bottom_margin = kwargs.get("bottom_margin", UDim(0, 0))
        self._left_margin = kwargs.get("left_margin", UDim(0, 0))
        self._right_margin = kwargs.get("right_margin", UDim(0, 0))

    def __on_layout_instance_child_added(self, child: PyGuiInstance):
        """
        Hook method called when a child is added.

        Args:
            child (PyGuiInstance): The added child PyGuiInstance.

        Note:
            Overrides the parent method to set initial position and anchor point for added child elements.
        """
        child._add_property_override("position", UDim2(0, 0, 0, 0))
        child._add_property_override("anchor_point", Vector2(0, 0))

    def __on_layout_instance_child_removed(self, child: PyGuiInstance):
        """
        Hook method called when a child is removed.

        Args:
            child (PyGuiInstance): The removed child PyGuiInstance.

        Note:
            Overrides the parent method to remove position and anchor point overrides for removed child elements.
        """
        child._remove_property_override("position")
        child._remove_property_override("anchor_point")

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
        Manages the order and positioning of child elements.

        Args:
            childs (List[PyGuiInstance]): List of child PyGuiInstance objects.

        Note:
            Overrides the parent method to implement the logic for ordering and positioning child elements.
        """
        largest_child_width = 0
        largest_child_height = 0

        current_row_width = 0
        current_row_height = 0

        (parent_instance_x_position, parent_instance_y_position) = self.instance.absolute_position
        (parent_instance_width, parent_instance_height) = self.instance.absolute_size

        for child in childs:
            child.BLOCKING_SCREEN_BUFFER_UPDATE = True

            child_position_x_offset = 0
            child_position_y_offset = 0

            (child_width, child_height) = child.absolute_size

            match self.horizontal_alignment:
                case HorizontalAlignment.LEFT:
                    if current_row_width + child_width > parent_instance_width:
                        child_position_x_offset, current_row_width, current_row_height = (
                            0,
                            child_width,
                            current_row_height + largest_child_height,
                        )
                    else:
                        child_position_x_offset, current_row_width = (
                            current_row_width,
                            current_row_width + child_width,
                        )
                case HorizontalAlignment.CENTER:
                    pass
                case HorizontalAlignment.RIGHT:
                    if current_row_width + child_width > parent_instance_width:
                        child_position_x_offset, current_row_width, current_row_height = (
                            parent_instance_width - child_width,
                            child_width,
                            current_row_height + largest_child_height,
                        )
                    else:
                        child_position_x_offset, current_row_width = (
                            parent_instance_width - current_row_width - child_width,
                            current_row_width + child_width,
                        )

            match self.vertical_alignment:
                case VerticalAlignment.TOP:
                    child_position_y_offset = current_row_height
                case VerticalAlignment.CENTER:
                    pass
                case VerticalAlignment.BOTTOM:
                    child_position_y_offset = parent_instance_height - child_height - current_row_height

            largest_child_width = max(largest_child_width, child_width)
            largest_child_height = max(largest_child_height, child_height)

            child._add_property_override("position", UDim2(0, child_position_x_offset, 0, child_position_y_offset))

        for child in childs:
            child.BLOCKING_SCREEN_BUFFER_UPDATE = False

        self.instance.clear()
        self.instance.draw()
