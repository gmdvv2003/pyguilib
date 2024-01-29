from enum import Enum
from typing import Any, Callable, List, Optional

from pygame.event import Event

INTERNAL_PRIORITY_THRESHOLD = 1000


class ActionResult(Enum):
    SINK = 0
    PASS = 1


binds_events_queue = []


def bind_action(action_name: str, callback: Callable[[Any], Optional[ActionResult]], events: List[int], priority: int = 0, internal: bool = False):
    if any(bind[0] == action_name for bind in binds_events_queue):
        raise ValueError(f"An action with the name {action_name} already exists")

    binds_events_queue.append((action_name, callback, events, priority + (INTERNAL_PRIORITY_THRESHOLD if internal else 0)))


def unbind_action(action_name: str):
    binds_events_queue[:] = [bind for bind in binds_events_queue if bind[0] != action_name]


def update(events: List[Event]):
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
