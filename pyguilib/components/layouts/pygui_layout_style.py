from enum import Enum
from typing import Any, Callable, Optional

from pyguilib.components.pygui_instance import PyGuiInstance


class HorizontalAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class VerticalAlignment(Enum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2


class FillDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class SortOrder(Enum):
    NAME = 0
    LAYOUT_ORDER = 1
    CUSTOM = 2


def name_sorter(self: "PyGuiLayoutStyle", child: "PyGuiInstance") -> int:
    return 0


def layout_order_sorter(self: "PyGuiLayoutStyle", child: "PyGuiInstance") -> int:
    return child.layout_order


def custom_sorter(self: "PyGuiLayoutStyle", child: "PyGuiInstance") -> int:
    return 0


class PyGuiLayoutStyle(object):
    def __init__(
        self,
        on_layout_instance_child_added: Optional[Callable[[Any], Any]] = lambda: None,
        on_layout_instance_child_removed: Optional[Callable[[Any], Any]] = lambda: None,
        on_layout_applied: Optional[Callable[[Any], Any]] = lambda: None,
        on_layout_removed: Optional[Callable[[Any], Any]] = lambda: None,
        layout_order_manager: Optional[Callable[[Any], Any]] = lambda: None,
        **kwargs,
    ) -> "PyGuiLayoutStyle":
        super(PyGuiLayoutStyle, self).__init__()

        self._horizontal_alignment = kwargs.get("horizontal_alignment", HorizontalAlignment.LEFT)
        self._vertical_alignment = kwargs.get("vertical_alignment", VerticalAlignment.TOP)
        self._fill_direction = kwargs.get("fill_direction", FillDirection.HORIZONTAL)
        self._sort_order = kwargs.get("sort_order", SortOrder.NAME)

        self._on_layout_instance_child_added = on_layout_instance_child_added
        self._on_layout_instance_child_removed = on_layout_instance_child_removed
        self._on_layout_applied = on_layout_applied
        self._on_layout_removed = on_layout_removed
        self._layout_order_manager = layout_order_manager

        self._sorted_instance_childs = []

    def _update_layout_order(original_caller: Callable[["PyGuiLayoutStyle", Any], None], *_) -> Callable[[Any], None]:
        def decorator(self: "PyGuiLayoutStyle", *kwargs):
            original_caller(self, *kwargs)
            self._layout_order_manager(self._sorted_instance_childs)

        return decorator

    def _sort_instance_childs(self):
        self._sorted_instance_childs = sorted(self._sorted_instance_childs, key=lambda child: child.layout_order)

    @property
    def instance(self) -> "PyGuiInstance":
        try:
            return self._instance
        except AttributeError:
            return None

    @property
    def horizontal_alignment(self) -> HorizontalAlignment:
        return self._horizontal_alignment

    @horizontal_alignment.setter
    @_update_layout_order
    def horizontal_alignment(self, value: HorizontalAlignment):
        self._horizontal_alignment = value

    @property
    def vertical_alignment(self) -> VerticalAlignment:
        return self._vertical_alignment

    @vertical_alignment.setter
    @_update_layout_order
    def vertical_alignment(self, value: VerticalAlignment):
        self._vertical_alignment = value

    @property
    def fill_direction(self) -> FillDirection:
        return self._fill_direction

    @fill_direction.setter
    @_update_layout_order
    def fill_direction(self, value: FillDirection):
        self._fill_direction = value

    @property
    def sort_order(self) -> SortOrder:
        return self._sort_order

    @sort_order.setter
    @_update_layout_order
    def sort_order(self, value: SortOrder):
        self._sort_order = value
