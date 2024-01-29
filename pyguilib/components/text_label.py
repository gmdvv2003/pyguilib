from enum import Enum
from typing import List

import pygame
from pygame import Color, Vector2
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance


class TextXAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class TextYAlignment(Enum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2


text_x_alignment_offsets = [0, 0.5, 1]
text_y_alignment_offsets = [0, 0.5, 1]

_circle_points_cache = {}


# https://github.com/lordmauve/pgzero/blob/master/pgzero/ptext.py#L233
def _circle_points(radius):
    if radius in _circle_points_cache:
        return _circle_points_cache[radius]

    x, y = radius, 0
    error = 1 - radius

    _circle_points_cache[radius] = points = []

    while x >= y:
        points.append((x, y))

        y += 1

        if error < 0:
            error += 2 * y - 1
        else:
            x -= 1
            error += 2 * (y - x) - 1

    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]

    points.sort()

    return points


class TextLabel(PyGuiInstance):
    """
    TextLabel class represents a GUI component for displaying text.

    Inherits from:
        PyGuiInstance

    Args:
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If there is an error loading the font.

    Methods:
        text_position(): Calculates the position of the text based on alignment.
        text_bounds(): Gets the bounding box of the text.

    Properties:
        text (str): The text content.
        text_color (Color): The text color.
        text_transparency (int): The text transparency.
        text_size (int): The text size.
        text_font (pygame.font.Font): The text font.
        text_border_color (Color): The text border color.
        text_border_size (int): The text border size.
        text_x_alignment (TextXAlignment): The text horizontal alignment.
        text_y_alignment (TextYAlignment): The text vertical alignment.
    """

    def __init__(self, **kwargs) -> "TextLabel":
        super(TextLabel, self).__init__(
            **kwargs,
        )

        self._text = [*kwargs.get("text", "TextLabel")]

        self._text_color = kwargs.get("text_color", Color(255, 255, 255, 255))
        self._text_transparency = kwargs.get("text_transparency", 255)
        self._text_size = kwargs.get("text_size", 16)
        self._text_font = kwargs.get("text_font", pygame.font.SysFont("Arial", self._text_size))

        self._text_border_color = kwargs.get("text_border_color", Color(0, 0, 0, 255))
        self._text_border_size = kwargs.get("text_border_size", 1)

        self._text_x_alignment = kwargs.get("text_x_alignment", TextXAlignment.CENTER)
        self._text_y_alignment = kwargs.get("text_y_alignment", TextYAlignment.CENTER)

        self._text_bounds = Vector2(0, 0)

        self._add_instance_updater_handler(self.__instance_updater)
        self._add_instance_drawer_handler(self.__instance_drawer)

        self._register_property_change_listener("text", lambda _: self.text)
        self._register_property_change_listener("text_color", lambda _: self.text_color)
        self._register_property_change_listener("text_transparency", lambda _: self.text_transparency)
        self._register_property_change_listener("text_size", lambda _: self.text_size)
        self._register_property_change_listener("text_font", lambda _: self.text_font)
        self._register_property_change_listener("text_x_alignment", lambda _: self.text_x_alignment)
        self._register_property_change_listener("text_y_alignment", lambda _: self.text_y_alignment)

        def _update_dynamic_properties(*_):
            self.__recalculate_text_bounds()

        _update_dynamic_properties()

        self.get_property_changed_signal("text").connect(_update_dynamic_properties)
        self.get_property_changed_signal("text_size").connect(_update_dynamic_properties)
        self.get_property_changed_signal("text_font").connect(_update_dynamic_properties)
        self.get_property_changed_signal("position").connect(_update_dynamic_properties)
        self.get_property_changed_signal("size").connect(_update_dynamic_properties)
        self.get_property_changed_signal("anchor_point").connect(_update_dynamic_properties)
        self.get_property_changed_signal("text_x_alignment").connect(_update_dynamic_properties)
        self.get_property_changed_signal("text_y_alignment").connect(_update_dynamic_properties)

    def __recalculate_text_bounds(self):
        max_text_width = 0
        max_text_height = 0

        for line in self.text.split("\n"):
            max_text_width = max(max_text_width, self.text_font.size(line)[0])
            max_text_height += self.text_font.get_height()

        self._text_bounds = Vector2(max_text_width, max_text_height)

    @property
    def text(self) -> str:
        """
        Get or set the text content of the TextLabel.

        Returns:
            str: The current text content.
        """
        return "".join(self._text)

    @text.setter
    @PyGuiInstance._update_screen_buffer
    def text(self, value: str):
        self._text = [*value]
        self._invoke_property_change_listener("text")

    @property
    def text_color(self) -> Color:
        """
        Get or set the color of the text within the TextLabel.

        Returns:
            Color: The current color of the text.
        """
        return self._text_color

    @text_color.setter
    @PyGuiInstance._update_screen_buffer
    def text_color(self, value: Color):
        self._text_color = value
        self._invoke_property_change_listener("text_color")

    @property
    def text_transparency(self) -> int:
        """
        Get or set the transparency of the text within the TextLabel.

        Returns:
            int: The current transparency of the text.
        """
        return self._text_transparency

    @text_transparency.setter
    @PyGuiInstance._update_screen_buffer
    def text_transparency(self, value: int):
        self._text_transparency = value
        self._invoke_property_change_listener("text_transparency")

    @property
    def text_size(self) -> int:
        """
        Get or set the size of the text within the TextLabel.

        Returns:
            int: The current size of the text.
        """
        return self._text_size

    @text_size.setter
    @PyGuiInstance._update_screen_buffer
    def text_size(self, value: int):
        self._text_size = value
        self._invoke_property_change_listener("text_size")

    @property
    def text_font(self) -> pygame.font.Font:
        """
        Get or set the font used for the text within the TextLabel.

        Returns:
            pygame.font.Font: The current font used for the text.
        """
        return self._text_font

    @text_font.setter
    @PyGuiInstance._update_screen_buffer
    def text_font(self, value: pygame.font.Font):
        self._text_font = value
        self._invoke_property_change_listener("text_font")

    @property
    def text_border_color(self) -> Color:
        """
        Get or set the color of the text border within the TextLabel.

        Returns:
            Color: The current color of the text border.
        """
        return self._text_border_color

    @text_border_color.setter
    @PyGuiInstance._update_screen_buffer
    def text_border_color(self, value: Color):
        self._text_border_color = value
        self._invoke_property_change_listener("text_border_color")

    @property
    def text_border_size(self) -> int:
        """
        Get or set the size of the text border within the TextLabel.

        Returns:
            int: The current size of the text border.
        """
        return self._text_border_size

    @text_border_size.setter
    @PyGuiInstance._update_screen_buffer
    def text_border_size(self, value: int):
        self._text_border_size = value
        self._invoke_property_change_listener("text_border_size")

    @property
    def text_x_alignment(self) -> TextXAlignment:
        """
        Get or set the horizontal alignment of the text within the TextLabel.

        Returns:
            TextXAlignment: The current horizontal alignment.
        """
        return self._text_x_alignment

    @text_x_alignment.setter
    @PyGuiInstance._update_screen_buffer
    def text_x_alignment(self, value: TextXAlignment):
        self._text_x_alignment = value

    @property
    def text_y_alignment(self) -> TextYAlignment:
        """
        Get or set the vertical alignment of the text within the TextLabel.

        Returns:
            TextYAlignment: The current vertical alignment.
        """
        return self._text_y_alignment

    @text_y_alignment.setter
    @PyGuiInstance._update_screen_buffer
    def text_y_alignment(self, value: TextYAlignment):
        self._text_y_alignment = value

    @property
    def text_position(self) -> Vector2:
        """
        Get the position of the text based on alignment within the TextLabel.

        Returns:
            Vector2: The position of the text.
        """
        return Vector2(
            self.absolute_position.x + (self.absolute_size.x - self._text_bounds.x) * text_x_alignment_offsets[self._text_x_alignment.value],
            self.absolute_position.y + (self.absolute_size.y - self._text_bounds.y) * text_y_alignment_offsets[self._text_y_alignment.value],
        )

    @property
    def text_bounds(self) -> Vector2:
        """
        Get the bounding box of the text.

        Returns:
            Vector2: The bounding box dimensions (width, height).
        """
        return self._text_bounds

    def __instance_updater(self, events: List[Event]):
        pass

    def __instance_drawer(self):
        text_lines = self.text.split("\n")
        text_lines.reverse()

        for index, line in enumerate(text_lines):
            (text_width, text_height) = self.text_font.size(line)

            text_border_surface = pygame.Surface((text_width + self._text_border_size * 2, text_height + self._text_border_size * 2)).convert_alpha()
            text_border_surface.fill((0, 0, 0, 0))
            text_border_surface.blit(self._text_font.render(line, True, self._text_border_color).convert_alpha(), (0, 0))

            drawable_text_surface = text_border_surface.copy()
            drawable_text_surface.set_alpha(self._text_transparency)

            for x, y in _circle_points(self._text_border_size):
                drawable_text_surface.blit(text_border_surface, (x + self._text_border_size, y + self._text_border_size))

            drawable_text_surface.blit(self._text_font.render(line, True, self._text_color).convert_alpha(), (self._text_border_size, self._text_border_size))

            line_x = (self.text_bounds.x - text_width) * text_x_alignment_offsets[self._text_x_alignment.value]
            line_y = text_height * (len(text_lines) - 1) - text_height * index

            (text_position_x, text_position_y) = self.text_position

            self._get_drawable_surface().blit(
                drawable_text_surface,
                (
                    text_position_x + line_x,
                    text_position_y + line_y,
                ),
            )
