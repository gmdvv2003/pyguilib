import uuid
from typing import Any, Callable, List, Optional

import pygame
from pygame import SRCALPHA, Color, Surface, Vector2
from pygame.event import Event

from pyguilib.utilities.quadtree import QuadTreeItem
from pyguilib.utilities.signal import PyGuiSignal
from pyguilib.utilities.udim import UDim2


class PyGuiInstance(object):
    def __init__(
        self,
        draw_order: int = 0,
        background_color: Color = Color(140, 140, 140, 255),
        background_transparency: float = 255,
        border_color: Color = Color(0, 0, 0, 255),
        border_size: int = 0,
        position: UDim2 = UDim2(0, 0, 0, 0),
        size: UDim2 = UDim2(0, 0, 0, 0),
        anchor_point: Vector2 = Vector2(0, 0),
        layout_order: int = 0,
        parent: Optional["PyGuiInstance"] = None,
        name: str = None,
        **_,
    ) -> "PyGuiInstance":
        self._visible = True

        self._draw_order = draw_order

        self._background_color = background_color
        self._background_transparency = background_transparency

        self._border_color = border_color
        self._border_size = border_size

        self._position = position
        self._size = size
        self._anchor_point = anchor_point

        self._layout_order = layout_order

        self._parent = parent

        self.__instance_updaters = []
        self.__instance_drawers = []

        self._name = name or f'Child_{str(uuid.uuid4()).replace("-", "_")}'

        self._childrens = {}
        self._properties_listeners = {}
        self._properties_overrides = {}

        self.__instance_depth = 0

        self.child_added = PyGuiSignal()
        self.child_removed = PyGuiSignal()

        self.mouse_moved = PyGuiSignal()

        self.mouse_entered = PyGuiSignal()
        self.mouse_leaving = PyGuiSignal()

        self.mouse_button_down = PyGuiSignal()
        self.mouse_button_up = PyGuiSignal()

        self._register_property_change_listener("visible", lambda _: self.visible)
        self._register_property_change_listener("draw_order", lambda _: self.draw_order)
        self._register_property_change_listener("background_color", lambda _: self.background_color)
        self._register_property_change_listener("border_color", lambda _: self.border_color)
        self._register_property_change_listener("background_transparency", lambda _: self.background_transparency)
        self._register_property_change_listener("border_size", lambda _: self.border_size)
        self._register_property_change_listener("position", lambda _: self.position)
        self._register_property_change_listener("size", lambda _: self.size)
        self._register_property_change_listener("anchor_point", lambda _: self.anchor_point)

        super(PyGuiInstance, self).__init__()

        def _sort_childrens(*_):
            self._childrens = dict(
                sorted(
                    self._childrens.items(),
                    key=lambda item: item[1].draw_order,
                )
            )

        self.child_added.connect(_sort_childrens)
        self.child_removed.connect(_sort_childrens)

        _sort_childrens()

        self._BLOCKING_SCREEN_BUFFER_UPDATE = 0
        self._BUILT = False

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def _add_instance_updater_handler(self, handler: Callable[[Any], Any], index: int = 0):
        self.__instance_updaters.insert(index, handler)

    def _add_instance_drawer_handler(self, handler: Callable[[Any], Any], index: int = 0):
        self.__instance_drawers.insert(index, handler)

    def _update_screen_buffer(original_caller: Callable[["PyGuiInstance", Any], None], *_) -> Callable[[Any], None]:
        def decorator(self: "PyGuiInstance", *kwargs):
            original_caller(self, *kwargs)

            if self._BUILT and not self.BLOCKING_SCREEN_BUFFER_UPDATE:
                self._parent.clear()
                self._parent.draw()

            # print(f'Updating {self._name}')

        return decorator

    def _invoke_property_change_listener(self, property_name: str):
        assert property_name in self._properties_listeners, f"Property {property_name} is not registered"
        self._properties_listeners[property_name].fire()

    def _register_property_change_listener(self, property_name: str, callback: Callable[[Any], Any]):
        assert property_name not in self._properties_listeners, f"Property {property_name} is already registered"

        property_event = PyGuiSignal()
        property_event.connect(callback)

        self._properties_listeners[property_name] = property_event

    def _get_overrided_property(self, property_name: str) -> Any:
        return self._properties_overrides.get(property_name, None)

    @_update_screen_buffer
    def _add_property_override(self, property_name: str, value: Any):
        self._properties_overrides[property_name] = value

    @_update_screen_buffer
    def _remove_property_override(self, property_name: str):
        del self._properties_overrides[property_name]

    def build(self) -> "PyGuiInstance":
        if self._BUILT:
            return self

        if not self._parent:
            print(f"{self._name} was not added to any parent")
        else:
            self._parent._childrens[self._name] = self

            try:
                self._root_quadtree_reference = (
                    getattr(self._parent, "_root_quadtree_reference")
                    if hasattr(self._parent, "_root_quadtree_reference")
                    else getattr(self._parent, "_root_quadtree")
                )
            except AttributeError:
                pass

            self.__instance_depth = self._parent.__instance_depth + 1

            self._root_quadtree_reference.insert(QuadTreeItem(self, lambda: self.absolute_position, lambda: self.absolute_size))
            self._parent.child_added.fire(self)

            self.clear()
            self.draw()

            self._BUILT = True

        return self

    def get_drawable_surface(self) -> Surface:
        return pygame.display.get_surface()

    def get_property_changed_signal(self, property_name: str) -> PyGuiSignal:
        assert property_name in self._properties_listeners, f"Property {property_name} is not registered"
        return self._properties_listeners[property_name]

    @property
    def BLOCKING_SCREEN_BUFFER_UPDATE(self) -> int:
        return self._parent._BLOCKING_SCREEN_BUFFER_UPDATE > 0

    @BLOCKING_SCREEN_BUFFER_UPDATE.setter
    @_update_screen_buffer
    def BLOCKING_SCREEN_BUFFER_UPDATE(self, value: bool):
        self._parent._BLOCKING_SCREEN_BUFFER_UPDATE = max(0, self._parent._BLOCKING_SCREEN_BUFFER_UPDATE + (1 if value else -1))

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    @_update_screen_buffer
    def visible(self, value: bool):
        self._visible = value
        self._invoke_property_change_listener("visible")

    @property
    def draw_order(self) -> int:
        return self._draw_order

    @draw_order.setter
    @_update_screen_buffer
    def draw_order(self, value: int):
        self._draw_order = value
        self._invoke_property_change_listener("draw_order")

    @property
    def background_color(self) -> Color:
        return self._background_color

    @background_color.setter
    @_update_screen_buffer
    def background_color(self, value: Color):
        self._background_color = value
        self._invoke_property_change_listener("background_color")

    @property
    def border_color(self) -> Color:
        return self._border_color

    @border_color.setter
    @_update_screen_buffer
    def border_color(self, value: Color):
        self._border_color = value
        self._invoke_property_change_listener("border_color")

    @property
    def background_transparency(self) -> float:
        return self._background_transparency

    @background_transparency.setter
    @_update_screen_buffer
    def background_transparency(self, value: float) -> float:
        self._background_transparency = value
        self._invoke_property_change_listener("background_transparency")

    @property
    def border_size(self) -> int:
        return self._border_size

    @border_size.setter
    @_update_screen_buffer
    def border_size(self, value: int):
        self._border_size = value
        self._invoke_property_change_listener("border_size")

    @property
    def position(self) -> UDim2:
        return self._get_overrided_property("position") or self._position

    @position.setter
    @_update_screen_buffer
    def position(self, value: UDim2):
        self._position = value
        self._invoke_property_change_listener("position")

    @property
    def absolute_position(self) -> Vector2:
        parent_absolute_position = self.parent.absolute_position if self.parent else Vector2(0, 0)
        parent_absolute_size = self.parent.absolute_size if self.parent else Vector2(*pygame.display.get_surface().get_size())

        return Vector2(
            (parent_absolute_position.x + parent_absolute_size.x * self.position.x.scale + self.position.x.offset) - self.absolute_size.x * self.anchor_point.x,
            (parent_absolute_position.y + parent_absolute_size.y * self.position.y.scale + self.position.y.offset) - self.absolute_size.y * self.anchor_point.y,
        )

    @property
    def size(self) -> UDim2:
        return self._get_overrided_property("size") or self._size

    @size.setter
    @_update_screen_buffer
    def size(self, size: UDim2):
        self._size = size
        self._invoke_property_change_listener("size")

    @property
    def absolute_size(self) -> Vector2:
        parent_absolute_size = self.parent.absolute_size if self.parent else Vector2(*pygame.display.get_surface().get_size())

        return Vector2(
            parent_absolute_size.x * self.size.x.scale + self.size.x.offset,
            parent_absolute_size.y * self.size.y.scale + self.size.y.offset,
        )

    @property
    def anchor_point(self) -> Vector2:
        return self._get_overrided_property("anchor_point") or self._anchor_point

    @anchor_point.setter
    @_update_screen_buffer
    def anchor_point(self, value: Vector2):
        self._anchor_point = value
        self._invoke_property_change_listener("anchor_point")

    @property
    def layout_order(self) -> int:
        return self._layout_order

    @layout_order.setter
    def layout_order(self, value: int):
        self._layout_order = value
        self._invoke_property_change_listener("layout_order")

    @property
    def parent(self) -> Optional["PyGuiInstance"]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional["PyGuiInstance"]):
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._parent._childrens[value] = self._parent._childrens.pop(self._name)

    def update(self, events: List[Event]):
        for instance_updater in self.__instance_updaters:
            instance_updater(events)

        for child in self._childrens.values():
            child.update(events)

    def clear(self):
        pass

    def draw(self):
        if self.visible:
            self._surface = Surface(self.absolute_size, SRCALPHA)

            self._surface.set_alpha(self.background_transparency)
            self._surface.fill(self.background_color)

            if self.border_size > 0:
                for x in range(2):
                    for y in range(2):
                        pygame.draw.rect(
                            self._surface,
                            self.border_color,
                            (
                                x,
                                y,
                                self.absolute_size.x - x * 2,
                                self.absolute_size.y - y * 2,
                            ),
                            self.border_size,
                        )

            self.get_drawable_surface().blit(self._surface, self.absolute_position)

            for instance_drawer in self.__instance_drawers:
                instance_drawer()

            for child in self._childrens.values():
                child.clear()
                child.draw()