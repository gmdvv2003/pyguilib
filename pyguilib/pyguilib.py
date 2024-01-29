import traceback
from typing import List

import pygame
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance
from pyguilib.services.action_service import update as action_service_update
from pyguilib.services.tween_service import update as tween_service_update
from pyguilib.utilities.quadtree import Quadtree
from pyguilib.utilities.udim import UDim2

PYGUI_SERVICES_UPDATERS = [
    action_service_update,
    tween_service_update,
]

instantiated_pygui_instances = []

last_mouse_over_instance = None
current_mouse_over_instance = None

last_pygame_window_size = None


class PyGui(PyGuiInstance):
    """
    PyGui class representing the main PyGui instance.

    Raises:
        Exception: If pygame is not initialized.
    """

    def __init__(self) -> "PyGui":
        if not pygame.get_init():
            raise Exception("Pygame is not initialized")

        self._root_quadtree = Quadtree(0, pygame.Rect(0, 0, *pygame.display.get_surface().get_size()))

        super(PyGui, self).__init__(position=UDim2(0, 0, 0, 0), size=UDim2(1, 0, 1, 0), name="PyGui")

        instantiated_pygui_instances.append(self)


def update(events: List[Event]):
    """
    Update function for PyGui, responsible for handling events and updating services.

    Args:
        events (List[Event]): List of pygame events.
    """
    global current_mouse_over_instance, last_mouse_over_instance
    global last_pygame_window_size

    this_frame_pygame_window_size = pygame.display.get_surface().get_size()
    if last_pygame_window_size is None or last_pygame_window_size != this_frame_pygame_window_size:
        for pygui in instantiated_pygui_instances:
            pygui.clear()
            pygui.draw()

        last_pygame_window_size = this_frame_pygame_window_size

    for service_updater in PYGUI_SERVICES_UPDATERS:
        try:
            service_updater(events)
        except Exception:
            print(f"An error occurred while updating a service: {traceback.format_exc()}")

    for pygui in instantiated_pygui_instances:
        retrieved_childs = pygui._root_quadtree.query(pygame.Rect(*pygame.mouse.get_pos(), 1, 1))

        if len(retrieved_childs) > 0:
            deepest_retrieved_child = retrieved_childs[-1].item

            if current_mouse_over_instance != deepest_retrieved_child:
                if last_mouse_over_instance is not None:
                    last_mouse_over_instance.mouse_leaving.fire()

                deepest_retrieved_child.mouse_entered.fire()

            for event in events:
                match event.type:
                    case pygame.MOUSEMOTION:
                        deepest_retrieved_child.mouse_moved.fire()
                    case pygame.MOUSEBUTTONDOWN:
                        deepest_retrieved_child.mouse_button_down.fire()
                    case pygame.MOUSEBUTTONUP:
                        deepest_retrieved_child.mouse_button_up.fire()

            last_mouse_over_instance = current_mouse_over_instance
            current_mouse_over_instance = deepest_retrieved_child
        else:
            if last_mouse_over_instance is not None:
                last_mouse_over_instance.mouse_leaving.fire()

            last_mouse_over_instance = None
            current_mouse_over_instance = None

        pygui.update(events)
