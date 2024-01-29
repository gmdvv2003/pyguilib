from enum import Enum
from typing import Any, Callable, List, Optional

from pygame.event import Event

INTERNAL_PRIORITY_THRESHOLD = 1000


class ActionResult(Enum):
    """
    Enum representing the result of an action.

    Attributes:
        SINK (int): The action was handled and should not be passed to other callbacks.
        PASS (int): The action was not handled and should be passed to other callbacks.
    """

    SINK = 0
    PASS = 1


binds_events_queue = []


def bind_action(
    action_name: str,
    callback: Callable[[Any], Optional[ActionResult]],
    events: List[int],
    priority: int = 0,
    internal: bool = False,
):
    """
    Binds an action to specific events and assigns a callback function to handle the action.

    Args:
        action_name (str): Name of the action.
        callback (Callable[[Any], Optional[ActionResult]]): Callback function to handle the action.
        events (List[int]): List of events that trigger the action.
        priority (int): Priority of the action (higher values indicate higher priority).
        internal (bool): Indicates whether the action has internal priority.

    Raises:
        ValueError: If an action with the same name already exists.
    """
    if any(bind[0] == action_name for bind in binds_events_queue):
        raise ValueError(f"An action with the name {action_name} already exists")

    binds_events_queue.append((action_name, callback, events, priority + (INTERNAL_PRIORITY_THRESHOLD if internal else 0)))


def unbind_action(action_name: str):
    """
    Unbinds an action based on its name.

    Args:
        action_name (str): Name of the action to unbind.
    """
    binds_events_queue[:] = [bind for bind in binds_events_queue if bind[0] != action_name]


def update(events: List[Event]):
    """
    Updates the bound actions based on the provided events.

    Args:
        events (List[Event]): List of pygame events.
    """
    for event in events:
        event_handled = False

        for _, callback, events, _ in sorted(binds_events_queue, key=lambda item: item[3]):
            if (event.type if hasattr(event, "type") else None) in events or (event.key if hasattr(event, "key") else None) in events:
                if callback(event) == ActionResult.SINK:
                    event_handled = True

            if event_handled:
                break

        if event_handled:
            break
