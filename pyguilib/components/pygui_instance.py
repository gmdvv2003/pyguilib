import uuid
from typing import Any, Callable, List, Optional

import pygame
from pygame import SRCALPHA, Color, Surface, Vector2
from pygame.event import Event

from pyguilib.utilities.quadtree import QuadTreeItem
from pyguilib.utilities.signal import PyGuiSignal
from pyguilib.utilities.udim import UDim2


class PyGuiInstance(object):
    """
    PyGuiInstance is the base class for GUI elements in a Pygame-based GUI library.

    Args:
        draw_order (int): The order in which the GUI instance is drawn.
        background_color (Color): The background color of the GUI instance.
        background_transparency (float): The transparency of the GUI instance background.
        border_color (Color): The color of the GUI instance border.
        border_size (int): The size of the GUI instance border.
        position (UDim2): The position of the GUI instance relative to its parent.
        size (UDim2): The size of the GUI instance relative to its parent.
        anchor_point (Vector2): The anchor point around which the GUI instance is positioned and scaled.
        layout_order (int): The order in which the GUI instance is laid out.
        parent (Optional[PyGuiInstance]): The parent GUI instance.
        name (str): The name of the GUI instance.

    Methods:
        build() -> "PyGuiInstance": Build the GUI instance and add it to the parent.
        get_property_changed_signal(property_name: str) -> PyGuiSignal: Get the signal for property changes.
        update(events: List[Event]): Update the GUI instance based on events.
        clear(): Clear the GUI instance.
        draw(): Draw the GUI instance.

    Properties:
        visible (bool): Property indicating whether the GUI instance is visible.
        draw_order (int): Property indicating the draw order of the GUI instance.
        background_color (Color): Property indicating the background color of the GUI instance.
        background_transparency (float): Property indicating the transparency of the GUI instance background.
        border_color (Color): Property indicating the border color of the GUI instance.
        border_size (int): Property indicating the border size of the GUI instance.
        position (UDim2): Property indicating the position of the GUI instance.
        absolute_position (Vector2): Property indicating the absolute position of the GUI instance.
        size (UDim2): Property indicating the size of the GUI instance.
        absolute_size (Vector2): Property indicating the absolute size of the GUI instance.
        anchor_point (Vector2): Property indicating the anchor point of the GUI instance.
        layout_order (int): Property indicating the layout order of the GUI instance.
        parent (Optional[PyGuiInstance]): Property indicating the parent GUI instance.
        name (str): Property indicating the name of the GUI instance.
        BLOCKING_SCREEN_BUFFER_UPDATE (int): Property to block screen buffer updates.
    """

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

    def _get_drawable_surface(self) -> Surface:
        """
        Get the drawable surface for rendering.

        Returns:
            Surface: The drawable surface.
        """
        return pygame.display.get_surface()

    def build(self) -> "PyGuiInstance":
        """
        Build the GUI element and add it to the parent.

        Returns:
            PyGuiInstance: The GUI element.
        """

        if self._BUILT:
            return self

        if not self._parent:
            print(f"{self._name} was not added to any parent")
        else:
            self._parent._childrens[self._name] = self

            try:
                self._root_quadtree_reference = getattr(self._parent, "_root_quadtree_reference")
            except AttributeError:
                pass

            self.__instance_depth = self._parent.__instance_depth + 1

            self._root_quadtree_reference.insert(QuadTreeItem(self, lambda: self.absolute_position, lambda: self.absolute_size))
            self._parent.child_added.fire(self)

            self.clear()
            self.draw()

            self._BUILT = True

        return self

    def get_property_changed_signal(self, property_name: str) -> PyGuiSignal:
        """
        Get the signal for a property change.

        Parameters:
            property_name (str): The name of the property.

        Returns:
            PyGuiSignal: The signal for the property change.
        """
        assert property_name in self._properties_listeners, f"Property {property_name} is not registered"
        return self._properties_listeners[property_name]

    @property
    def BLOCKING_SCREEN_BUFFER_UPDATE(self) -> bool:
        """
        Property for controlling blocking of screen buffer updates.

        Returns:
            bool: Whether screen buffer updates are blocked.
        """
        return self._parent._BLOCKING_SCREEN_BUFFER_UPDATE > 0

    @BLOCKING_SCREEN_BUFFER_UPDATE.setter
    @_update_screen_buffer
    def BLOCKING_SCREEN_BUFFER_UPDATE(self, value: bool):
        self._parent._BLOCKING_SCREEN_BUFFER_UPDATE = max(0, self._parent._BLOCKING_SCREEN_BUFFER_UPDATE + (1 if value else -1))

    @property
    def visible(self) -> bool:
        """
        Property for controlling the visibility of the GUI element.

        Returns:
            bool: The visibility of the GUI element.
        """
        return self._visible

    @visible.setter
    @_update_screen_buffer
    def visible(self, value: bool):
        self._visible = value
        self._invoke_property_change_listener("visible")

    @property
    def draw_order(self) -> int:
        """
        Property for controlling the draw order of the GUI element.

        Returns:
            int: The draw order of the GUI element.
        """
        return self._draw_order

    @draw_order.setter
    @_update_screen_buffer
    def draw_order(self, value: int):
        self._draw_order = value
        self._invoke_property_change_listener("draw_order")

    @property
    def background_color(self) -> Color:
        """
        Property for controlling the background color of the GUI element.

        Returns:
            Color: The background color of the GUI element.
        """
        return self._background_color

    @background_color.setter
    @_update_screen_buffer
    def background_color(self, value: Color):
        self._background_color = value
        self._invoke_property_change_listener("background_color")

    @property
    def border_color(self) -> Color:
        """
        Property for controlling the border color of the GUI element.

        Returns:
            Color: The border color of the GUI element.
        """
        return self._border_color

    @border_color.setter
    @_update_screen_buffer
    def border_color(self, value: Color):
        self._border_color = value
        self._invoke_property_change_listener("border_color")

    @property
    def background_transparency(self) -> float:
        """
        Property for controlling the transparency of the GUI element background.

        Returns:
            float: The transparency of the GUI element background.
        """
        return self._background_transparency

    @background_transparency.setter
    @_update_screen_buffer
    def background_transparency(self, value: float) -> float:
        self._background_transparency = value
        self._invoke_property_change_listener("background_transparency")

    @property
    def border_size(self) -> int:
        """
        Property for controlling the border size of the GUI element.

        Returns:
            int: The border size of the GUI element.
        """
        return self._border_size

    @border_size.setter
    @_update_screen_buffer
    def border_size(self, value: int):
        self._border_size = value
        self._invoke_property_change_listener("border_size")

    @property
    def position(self) -> UDim2:
        """
        Property for controlling the position of the GUI element.

        Returns:
            UDim2: The position of the GUI element.
        """
        return self._get_overrided_property("position") or self._position

    @position.setter
    @_update_screen_buffer
    def position(self, value: UDim2):
        self._position = value
        self._invoke_property_change_listener("position")

    @property
    def absolute_position(self) -> Vector2:
        """
        Property for getting the absolute position of the GUI element.

        Returns:
            Vector2: The absolute position of the GUI element.
        """
        parent_absolute_position = self.parent.absolute_position if self.parent else Vector2(0, 0)
        parent_absolute_size = self.parent.absolute_size if self.parent else Vector2(*pygame.display.get_surface().get_size())

        return Vector2(
            (parent_absolute_position.x + parent_absolute_size.x * self.position.x.scale + self.position.x.offset) - self.absolute_size.x * self.anchor_point.x,
            (parent_absolute_position.y + parent_absolute_size.y * self.position.y.scale + self.position.y.offset) - self.absolute_size.y * self.anchor_point.y,
        )

    @property
    def size(self) -> UDim2:
        """
        Property for controlling the size of the GUI element.

        Returns:
            UDim2: The size of the GUI element.
        """
        return self._get_overrided_property("size") or self._size

    @size.setter
    @_update_screen_buffer
    def size(self, size: UDim2):
        self._size = size
        self._invoke_property_change_listener("size")

    @property
    def absolute_size(self) -> Vector2:
        """
        Property for getting the absolute size of the GUI element.

        Returns:
            Vector2: The absolute size of the GUI element.
        """
        parent_absolute_size = self.parent.absolute_size if self.parent else Vector2(*pygame.display.get_surface().get_size())

        return Vector2(
            parent_absolute_size.x * self.size.x.scale + self.size.x.offset,
            parent_absolute_size.y * self.size.y.scale + self.size.y.offset,
        )

    @property
    def anchor_point(self) -> Vector2:
        """
        Property for controlling the anchor point of the GUI element.

        Returns:
            Vector2: The anchor point of the GUI element.
        """
        return self._get_overrided_property("anchor_point") or self._anchor_point

    @anchor_point.setter
    @_update_screen_buffer
    def anchor_point(self, value: Vector2):
        self._anchor_point = value
        self._invoke_property_change_listener("anchor_point")

    @property
    def layout_order(self) -> int:
        """
        Property for controlling the layout order of the GUI element.

        Returns:
            int: The layout order of the GUI element.
        """
        return self._layout_order

    @layout_order.setter
    def layout_order(self, value: int):
        self._layout_order = value
        self._invoke_property_change_listener("layout_order")

    @property
    def parent(self) -> Optional["PyGuiInstance"]:
        """
        Property for getting the parent GUI element.

        Returns:
            Optional[PyGuiInstance]: The parent GUI element.
        """
        return self._parent

    @parent.setter
    def parent(self, value: Optional["PyGuiInstance"]):
        pass

    @property
    def name(self) -> str:
        """
        Property for getting the name of the GUI element.

        Returns:
            str: The name of the GUI element.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._parent._childrens[value] = self._parent._childrens.pop(self._name)

    def update(self, events: List[Event]):
        """
        Update the GUI element based on the given events.

        Parameters:
            events (List[Event]): The events to update the GUI element with.
        """
        for instance_updater in self.__instance_updaters:
            instance_updater(events)

        for child in self._childrens.values():
            child.update(events)

    def clear(self):
        """
        Clear the GUI element.
        """
        pass

    def draw(self):
        """
        Draw the GUI element on the screen.
        """
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

            self._get_drawable_surface().blit(self._surface, self.absolute_position)

            for instance_drawer in self.__instance_drawers:
                instance_drawer()

            for child in self._childrens.values():
                child.clear()
                child.draw()
