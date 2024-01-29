import os
from typing import List

import pygame
from pygame import Color
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance


class ImageLabel(PyGuiInstance):
    """
    ImageLabel class representing an image label component.

    Inherits from:
        PyGuiInstance

    Args:
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If no image is provided or if there is an error loading the image.

    Properties:
        image_color (Color): The image color.
        image_transparency (int): The image transparency.
    """

    def __init__(self, **kwargs) -> "ImageLabel":
        image = kwargs.get("image", None)
        if image is None:
            raise Exception("You must pass an image to the ImageLabel component")

        try:
            self._image_surface = pygame.image.load(os.path.join(os.getcwd(), image)).convert_alpha()
        except Exception as exception:
            raise Exception(f"Error loading image: {exception}")

        super(ImageLabel, self).__init__(
            **kwargs,
        )

        self._image_color = kwargs.get("image_color", (255, 255, 255, 255))
        self._image_transparency = kwargs.get("image_transparency", 255)

        self._register_property_change_listener("image_color", lambda _: self.image_color)
        self._register_property_change_listener("image_transparency", lambda _: self.image_transparency)

        self._add_instance_updater_handler(self.__instance_updater)
        self._add_instance_drawer_handler(self.__instance_drawer)

    @property
    def image_color(self) -> Color:
        """
        Property for getting the image color.

        Returns:
            Color: The image color.
        """
        return self._image_color

    @image_color.setter
    @PyGuiInstance._update_screen_buffer
    def image_color(self, value: Color):
        self._image_color = value
        self._invoke_property_change_listener("image_color")

    @property
    def image_transparency(self) -> int:
        """
        Property for getting the image transparency.

        Returns:
            int: The image transparency.
        """
        return self._image_transparency

    @image_transparency.setter
    @PyGuiInstance._update_screen_buffer
    def image_transparency(self, value: int):
        self._image_transparency = value
        self._invoke_property_change_listener("image_transparency")

    def __instance_updater(self, events: List[Event]):
        pass

    def __instance_drawer(self):
        image_surface_copy = pygame.transform.scale(self._image_surface.copy(), self.absolute_size)

        image_surface_copy.set_alpha(self.image_transparency)
        image_surface_copy.fill(self.image_color, special_flags=pygame.BLEND_RGBA_MULT)

        self._get_drawable_surface().blit(image_surface_copy, self.absolute_position)
