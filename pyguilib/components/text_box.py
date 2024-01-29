from typing import Any, Callable, List

import pygame
from pygame import Color
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance
from pyguilib.components.text_label import TextLabel
from pyguilib.services import action_service
from pyguilib.services.action_service import ActionResult
from pyguilib.utilities.signal import PyGuiSignal


def default_cursor_apparence() -> pygame.Surface:
    pass


class TextBox(TextLabel, PyGuiInstance):
    """
    TextBox class represents a GUI component for text input.

    Inherits from:
        TextLabel
        PyGuiInstance

    Args:
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If there is an error loading the font.

    Attributes:
        focus_gained (PyGuiSignal): Signal emitted when the TextBox gains focus.
        focus_lost (PyGuiSignal): Signal emitted when the TextBox loses focus.

    Methods:
        is_focused(): Check if the TextBox is currently focused.
        capture_focus(): Capture focus for the TextBox.
        release_focus(enter_pressed: bool = False): Release focus for the TextBox.
        placeholder_text(): Get or set the placeholder text.
        placeholder_text_color(): Get or set the color of the placeholder text.
        placeholder_text_transparency(): Get or set the transparency of the placeholder text.
        placeholder_text_font(): Get or set the font used for the placeholder text.
        text_editable(): Get or set the flag indicating whether the text is editable.
        clear_text_on_focus_lost(): Get or set the flag indicating whether to clear text on focus lost.
        selection_start(): Get the starting index of the text selection.
        selection_end(): Get the ending index of the text selection.
        cursor_position(): Get the current cursor position in the text.

    Properties:
        placeholder_text (str): The current placeholder text.
        placeholder_text_color (Color): The current color of the placeholder text.
        placeholder_text_transparency (int): The current transparency of the placeholder text.
        placeholder_text_font (pygame.font.Font): The current font used for the placeholder text.
        text_editable (bool): True if the text is editable, False otherwise.
        clear_text_on_focus_lost (bool): True if text should be cleared on focus lost, False otherwise.
        selection_start (int): The starting index of the text selection.
        selection_end (int): The ending index of the text selection.
        cursor_position (int): The current cursor position.
    """

    def __init__(self, **kwargs) -> "TextBox":
        super(TextBox, self).__init__(
            **kwargs,
        )

        self._placeholder_text = kwargs.get("placeholder_text", "TextBox")

        self._placeholder_text_color = kwargs.get("placeholder_text_color", (255, 0, 0, 255))
        self._placeholder_text_transparency = kwargs.get("placeholder_text_transparency", 255)
        self._placeholder_text_font = kwargs.get("text_font", pygame.font.SysFont("Arial", self._text_size, italic=True))

        self._text_editable = kwargs.get("text_editable", True)
        self._clear_text_on_focus_lost = kwargs.get("clear_text_on_focus_lost", False)

        self._selection_color = kwargs.get("selection_color", (255, 255, 255, 255))
        self._selection_transparency = kwargs.get("selection_transparency", 170)

        self._cursor_blink_interval = kwargs.get("cursor_blink_interval", 0.5)
        self._cursor_appeareance = kwargs.get("cursor_appeareance", default_cursor_apparence)

        self.focus_gained = PyGuiSignal()
        self.focus_lost = PyGuiSignal()

        self._register_property_change_listener("placeholder_text", lambda _: self.placeholder_text)
        self._register_property_change_listener("placeholder_text_color", lambda _: self.placeholder_text_color)
        self._register_property_change_listener("placeholder_text_transparency", lambda _: self.placeholder_text_transparency)
        self._register_property_change_listener("placeholder_text_font", lambda _: self.placeholder_text_font)

        self._register_property_change_listener("text_editable", lambda _: self.text_editable)
        self._register_property_change_listener("clear_text_on_focus_lost", lambda _: self.clear_text_on_focus_lost)

        self._original_text_color = self._text_color
        self._original_text_transparency = self._text_transparency
        self._original_text_font = self._text_font

        self.text = self._placeholder_text
        self.text_color = self._placeholder_text_color
        self.text_transparency = self._placeholder_text_transparency
        self.text_font = self._placeholder_text_font

        def _update_original_property_value(key: str) -> Callable[[Any], None]:
            def wrapper(value: Any):
                setattr(self, key, value)

            return wrapper

        self.get_property_changed_signal("text_color").connect(_update_original_property_value("_original_text_color"))
        self.get_property_changed_signal("text_transparency").connect(_update_original_property_value("_original_text_transparency"))
        self.get_property_changed_signal("text_font").connect(_update_original_property_value("_original_text_font"))

        self._selection_start = 0
        self._selection_end = 0

        self._furthest_cursor_position = 0
        self._cursor_position = 0

        self._is_focused = False

        def _text_box_mouse_interaction(*_):
            self.capture_focus()

        def _text_box_focus_gained(*_):
            self._is_focused = True

            self.text_color = self._original_text_color
            self.text_transparency = self._original_text_transparency
            self.text_font = self._original_text_font

            self._cursor_position = len(self._text)

            def on_backspace_pressed(event: Event):
                if event.type != pygame.KEYDOWN:
                    return ActionResult.PASS

                if self._cursor_position == 0:
                    return ActionResult.SINK

                self.text = self._text[: self._cursor_position - 1] + self._text[self._cursor_position :]
                self._cursor_position -= 1

                return ActionResult.SINK

            def on_return_pressed(event: Event):
                if event.type != pygame.KEYDOWN:
                    return ActionResult.PASS

                self.text = self.text[: self._cursor_position] + "\n" + "" if self._cursor_position == len(self.text) else self.text[self._cursor_position :]
                self._cursor_position += 1

                return ActionResult.SINK

            def on_left_arrow_pressed(event: Event):
                if event.type != pygame.KEYDOWN:
                    return ActionResult.PASS

                self._cursor_position = max(0, self._cursor_position - 1)
                return ActionResult.SINK

            def on_right_arrow_pressed(event: Event):
                if event.type != pygame.KEYDOWN:
                    return ActionResult.PASS

                self._cursor_position = min(len(self.text), self._cursor_position + 1)
                return ActionResult.SINK

            def on_up_arrow_pressed(event: Event):
                return ActionResult.SINK

            def on_down_arrow_pressed(event: Event):
                return ActionResult.SINK

            def on_text_input(event: Event):
                self.text = self.text[: self._cursor_position] + event.unicode + self.text[self._cursor_position :]
                self._cursor_position += 1
                return ActionResult.SINK

            action_service.bind_action("backspace_pressed", on_backspace_pressed, [pygame.K_BACKSPACE], priority=0, internal=True)
            action_service.bind_action("return_pressed", on_return_pressed, [pygame.K_RETURN], priority=0, internal=True)
            action_service.bind_action("left_arrow_pressed", on_left_arrow_pressed, [pygame.K_LEFT], priority=0, internal=True)
            action_service.bind_action("right_arrow_pressed", on_right_arrow_pressed, [pygame.K_RIGHT], priority=0, internal=True)
            action_service.bind_action("up_arrow_pressed", on_up_arrow_pressed, [pygame.K_UP], priority=0, internal=True)
            action_service.bind_action("down_arrow_pressed", on_down_arrow_pressed, [pygame.K_DOWN], priority=0, internal=True)
            action_service.bind_action("text_input", on_text_input, [pygame.KEYDOWN], priority=10, internal=True)

        def _text_box_focus_lost(*_):
            self._is_focused = False

            self.text_color = self._placeholder_text_color
            self.text_transparency = self._placeholder_text_transparency
            self.text_font = self._placeholder_text_font

            if self._clear_text_on_focus_lost:
                self._text = self._placeholder_text

            self._cursor_position = 0

            action_service.unbind_action("backspace_pressed")
            action_service.unbind_action("return_pressed")
            action_service.unbind_action("left_arrow_pressed")
            action_service.unbind_action("right_arrow_pressed")
            action_service.unbind_action("up_arrow_pressed")
            action_service.unbind_action("down_arrow_pressed")
            action_service.unbind_action("text_input")

        self.mouse_button_down.connect(_text_box_mouse_interaction)

        self.focus_gained.connect(_text_box_focus_gained)
        self.focus_lost.connect(_text_box_focus_lost)

        self._add_instance_updater_handler(self.__instance_updater, 1)
        self._add_instance_drawer_handler(self.__instance_drawer, 1)

    @property
    def is_focused(self) -> bool:
        """
        Check if the TextBox is currently focused.

        Returns:
            bool: True if the TextBox is focused, False otherwise.
        """
        return self._is_focused

    def capture_focus(self):
        """
        Capture focus for the TextBox.
        """
        if self._text_editable and not self._is_focused:
            self.focus_gained.fire()

    def release_focus(self, enter_pressed: bool = False):
        """
        Release focus for the TextBox.

        Args:
            enter_pressed (bool): Flag indicating whether the Enter key was pressed.
        """
        if self._is_focused:
            self.focus_lost.fire(enter_pressed)

    @property
    def placeholder_text(self) -> str:
        """
        Get or set the placeholder text.

        Returns:
            str: The current placeholder text.
        """
        return self._placeholder_text

    @placeholder_text.setter
    @PyGuiInstance._update_screen_buffer
    def placeholder_text(self, value: str):
        self._placeholder_text = value
        self._invoke_property_change_listener("placeholder_text")

    @property
    def placeholder_text_color(self) -> Color:
        """
        Get or set the color of the placeholder text.

        Returns:
            Color: The current color of the placeholder text.
        """
        return self._placeholder_text_color

    @placeholder_text_color.setter
    @PyGuiInstance._update_screen_buffer
    def placeholder_text_color(self, value: Color):
        self._placeholder_text_color = value
        self._invoke_property_change_listener("placeholder_text_color")

    @property
    def placeholder_text_transparency(self) -> int:
        """
        Get or set the transparency of the placeholder text.

        Returns:
            int: The current transparency of the placeholder text.
        """
        return self._placeholder_text_transparency

    @placeholder_text_transparency.setter
    @PyGuiInstance._update_screen_buffer
    def placeholder_text_transparency(self, value: int):
        self._placeholder_text_transparency = value
        self._invoke_property_change_listener("placeholder_text_transparency")

    @property
    def placeholder_text_font(self) -> pygame.font.Font:
        """
        Get or set the font used for the placeholder text.

        Returns:
            pygame.font.Font: The current font used for the placeholder text.
        """
        return self._placeholder_text_font

    @placeholder_text_font.setter
    @PyGuiInstance._update_screen_buffer
    def placeholder_text_font(self, value: pygame.font.Font):
        self._placeholder_text_font = value
        self._invoke_property_change_listener("placeholder_text_font")

    @property
    def text_editable(self) -> bool:
        """
        Get or set the flag indicating whether the text is editable.

        Returns:
            bool: True if the text is editable, False otherwise.
        """
        return self._text_editable

    @text_editable.setter
    @PyGuiInstance._update_screen_buffer
    def text_editable(self, value: bool):
        self._text_editable = value
        self._invoke_property_change_listener("text_editable")

    @property
    def clear_text_on_focus_lost(self) -> bool:
        """
        Get or set the flag indicating whether to clear text on focus lost.

        Returns:
            bool: True if text should be cleared on focus lost, False otherwise.
        """
        return self._clear_text_on_focus_lost

    @clear_text_on_focus_lost.setter
    @PyGuiInstance._update_screen_buffer
    def clear_text_on_focus_lost(self, value: bool):
        self._clear_text_on_focus_lost = value
        self._invoke_property_change_listener("clear_text_on_focus_lost")

    @property
    def selection_start(self) -> int:
        """
        Get the starting index of the text selection.

        Returns:
            int: The starting index of the text selection.
        """
        return self._selection_start

    @property
    def selection_end(self) -> int:
        """
        Get the ending index of the text selection.

        Returns:
            int: The ending index of the text selection.
        """
        return self._selection_end

    @property
    def cursor_position(self) -> int:
        """
        Get the current cursor position in the text.

        Returns:
            int: The current cursor position.
        """
        return self._cursor_position

    def __instance_updater(self, events: List[Event]):
        pass

    def __instance_drawer(self):
        if self._is_focused:
            drawable_surface = self._get_drawable_surface()
            if self._selection_start != self._selection_end:
                selected_text = self._text[self._selection_start : self._selection_end]
            else:
                pass
