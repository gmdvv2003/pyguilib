import time
from typing import List

import imageio
import pygame
from pygame import Color
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance


class VideoLabel(PyGuiInstance):
    """
    VideoLabel class represents a GUI component for displaying a GIF.

    Inherits from:
        PyGuiInstance

    Args:
        **kwargs: Additional keyword arguments.

    Raises:
        Exception: If no GIF is provided or if there is an error loading the GIF.

    Methods:
        pause(): Placeholder method for pausing the GIF.
        resume(): Placeholder method for resuming the GIF.

    Properties:
        current_gif_frame (int): Index of the current GIF frame.
        gif_playback_speed (int): The GIF playback speed.
        gif_color (Color): The GIF color.
        gif_transparency (int): The GIF transparency.
    """

    def __init__(self, **kwargs) -> "VideoLabel":
        gif = kwargs.get("gif", None)
        if gif is None:
            raise Exception("You must pass a gif to the VideoLabel component")

        try:
            self._gif_reader = imageio.get_reader(gif)
        except Exception as exception:
            raise Exception(f"Error loading gif: {exception}")

        super(VideoLabel, self).__init__(
            **kwargs,
        )

        self.__gif_creating_timestamp = time.time()

        self._gif_playback_speed = kwargs.get("gif_playback_speed", 1)
        self._gif_color = kwargs.get("gif_color", (255, 255, 255, 255))
        self._gif_transparency = kwargs.get("gif_transparency", 255)

        self._gif_frames = []

        for frame in range(self._gif_reader.get_length()):
            self._gif_frames.append(
                pygame.transform.smoothscale(pygame.transform.rotate(pygame.surfarray.make_surface(self._gif_reader.get_data(frame)), -90), self.absolute_size)
            )

        self._register_property_change_listener("gif_playback_speed", lambda _: self.gif_playback_speed)
        self._register_property_change_listener("gif_color", lambda _: self.gif_color)
        self._register_property_change_listener("gif_transparency", lambda _: self.gif_transparency)

        self._add_instance_updater_handler(self.__instance_updater)
        self._add_instance_drawer_handler(self.__instance_drawer)

        self.get_property_changed_signal("size").connect(lambda *_: self.__update_gif_scale_transform())

    def __update_gif_scale_transform(self):
        for index in range(self._gif_reader.get_length()):
            self._gif_frames[index] = pygame.transform.smoothscale(self._gif_frames[index], self.absolute_size)

    @property
    def current_gif_frame(self) -> int:
        """
        Calculates the index of the current GIF frame based on the playback speed.

        Returns:
            int: Index of the current GIF frame.
        """
        return (
            int((time.time() - self.__gif_creating_timestamp) * (1000 / self._gif_reader.get_meta_data()["duration"]) * self._gif_playback_speed)
        ) % self._gif_reader.get_length()

    def pause():
        """
        Not implemented.
        """
        pass

    def resume():
        """
        Not implemented.
        """
        pass

    @property
    def gif_playback_speed(self) -> int:
        """
        Property for getting the GIF playback speed.

        Returns:
            int: The GIF playback speed.
        """
        return self._gif_playback_speed

    @gif_playback_speed.setter
    def gif_playback_speed(self, value: int):
        self._gif_playback_speed = value
        self._invoke_property_change_listener("gif_playback_speed")

    @property
    def gif_color(self) -> Color:
        """
        Property for getting the GIF color.

        Returns:
            Color: The GIF color.
        """
        return self._gif_color

    @gif_color.setter
    def gif_color(self, value: Color):
        self._gif_color = value
        self._invoke_property_change_listener("gif_color")

    @property
    def gif_transparency(self) -> int:
        """
        Property for getting the GIF transparency.

        Returns:
            int: The GIF transparency.
        """
        return self._gif_transparency

    @gif_transparency.setter
    def gif_transparency(self, value: int):
        self._gif_transparency = value
        self._invoke_property_change_listener("gif_transparency")

    def __instance_updater(self, events: List[Event]):
        self.clear()
        self.draw()

    def __instance_drawer(self):
        current_frame = self._gif_frames[self.current_gif_frame].copy()

        current_frame.set_alpha(self.gif_transparency)
        current_frame.fill(self.gif_color, special_flags=pygame.BLEND_RGBA_MULT)

        self._get_drawable_surface().blit(current_frame, self.absolute_position)
