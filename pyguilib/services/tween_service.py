import math
import time
from enum import Enum
from typing import Any, Dict, List

from pygame import Color, Vector2
from pygame.event import Event

from pyguilib.components.pygui_instance import PyGuiInstance
from pyguilib.utilities.signal import PyGuiSignal
from pyguilib.utilities.udim import UDim2


class TweenStatus(Enum):
    PLAYING = 0
    PAUSED = 1
    CANCELED = 2
    ENDED = 3


class TweenType(Enum):
    LINEAR = 0

    SINE_IN = 1
    SINE_OUT = 2
    SINE_IN_OUT = 3

    QUAD_IN = 4
    QUAD_OUT = 5
    QUAD_IN_OUT = 6

    CUBIC_IN = 7
    CUBIC_OUT = 8
    CUBIC_IN_OUT = 9

    QUART_IN = 10
    QUART_OUT = 11
    QUART_IN_OUT = 12

    QUINT_IN = 13
    QUINT_OUT = 14
    QUINT_IN_OUT = 15

    EXPO_IN = 16
    EXPO_OUT = 17
    EXPO_IN_OUT = 18

    CIRC_IN = 19
    CIRC_OUT = 20
    CIRC_IN_OUT = 21

    BACK_IN = 22
    BACK_OUT = 23
    BACK_IN_OUT = 24

    ELASTIC_IN = 25
    ELASTIC_OUT = 26
    ELASTIC_IN_OUT = 27

    BOUNCE_IN = 28
    BOUNCE_OUT = 29
    BOUNCE_IN_OUT = 30


# https://easings.net/
def sine_in(alpha):
    return 1 - math.cos(alpha * math.pi / 2)


def sine_out(alpha):
    return math.sin(alpha * math.pi / 2)


def sine_in_out(alpha):
    return -(math.cos(math.pi * alpha) - 1) / 2


def quad_in(alpha):
    return alpha * alpha


def quad_out(alpha):
    return 1 - (1 - alpha) * (1 - alpha)


def quad_in_out(alpha):
    return 2 * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 2) / 2


def cubic_in(alpha):
    return alpha * alpha * alpha


def cubic_out(alpha):
    return 1 - math.pow(1 - alpha, 3)


def cubic_in_out(alpha):
    return 4 * alpha * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 3) / 2


def quart_in(alpha):
    return alpha * alpha * alpha * alpha


def quart_out(alpha):
    return 1 - math.pow(1 - alpha, 4)


def quart_in_out(alpha):
    return 8 * alpha * alpha * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 4) / 2


def quint_in(alpha):
    return alpha * alpha * alpha * alpha * alpha


def quint_out(alpha):
    return 1 - math.pow(1 - alpha, 5)


def quint_in_out(alpha):
    return 16 * alpha * alpha * alpha * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 5) / 2


def expo_in(alpha):
    return 0 if alpha == 0 else math.pow(2, 10 * alpha - 10)


def expo_out(alpha):
    return 1 if alpha == 1 else 1 - math.pow(2, -10 * alpha)


def expo_in_out(alpha):
    return 0 if alpha == 0 else 1 if alpha == 1 else math.pow(2, 20 * alpha - 10) / 2 if alpha < 0.5 else (2 - math.pow(2, -20 * alpha * 2 + 10)) / 2


def circ_in(alpha):
    return 1 - math.sqrt(1 - math.pow(alpha, 2))


def circ_out(alpha):
    return math.sqrt(1 - math.pow(alpha - 1, 2))


def circ_in_out(alpha):
    return (1 - math.sqrt(1 - math.pow(2 * alpha, 2))) / 2 if alpha < 0.5 else (math.sqrt(1 - math.pow(-2 * alpha + 2, 2)) + 1) / 2


def back_in(alpha):
    bounce = 1.70158
    return (bounce + 1) * alpha * alpha * alpha - bounce * alpha * alpha


def back_out(alpha):
    bounce = 1.70158
    return 1 + (bounce + 1) * math.pow(alpha - 1, 3) + bounce * math.pow(alpha - 1, 2)


def back_in_out(alpha):
    bounce = 1.70158 * 1.525
    return (
        (math.pow(2 * alpha, 2) * ((bounce + 1) * 2 * alpha - bounce)) / 2
        if alpha < 0.5
        else (math.pow(2 * alpha - 2, 2) * ((bounce + 1) * (alpha * 2 - 2) + bounce) + 2) / 2
    )


def elastic_in(alpha):
    elasticity = (2 * math.pi) / 3
    return 0 if alpha == 0 else 1 if alpha == 1 else -math.pow(2, 10 * alpha - 10) * math.sin((alpha * 10 - 10.75) * elasticity)


def elastic_out(alpha):
    elasticity = (2 * math.pi) / 3
    return 0 if alpha == 0 else 1 if alpha == 1 else math.pow(2, -10 * alpha) * math.sin((alpha * 10 - 0.75) * elasticity) + 1


def elastic_in_out(alpha):
    elasticity = (2 * math.pi) / 4.5
    return (
        0
        if alpha == 0
        else 1
        if alpha == 1
        else -(math.pow(2, 20 * alpha - 10) * math.sin((20 * alpha - 11.125) * elasticity)) / 2
        if alpha < 0.5
        else (math.pow(2, -20 * alpha + 10) * math.sin((20 * alpha - 11.125) * elasticity)) / 2 + 1
    )


def bounce_in(alpha):
    return 1 - bounce_out(1 - alpha)


def bounce_out(alpha):
    amplitude = 7.5625
    duration = 2.75

    if alpha < 1 / duration:
        return amplitude * alpha * alpha
    elif alpha < 2 / duration:
        alpha -= 1.5 / duration
        return amplitude * alpha * alpha + 0.75
    elif alpha < 2.5 / duration:
        alpha -= 2.25 / duration
        return amplitude * alpha * alpha + 0.9375
    else:
        alpha -= 2.625 / duration
        return amplitude * alpha * alpha + 0.984375


def bounce_in_out(alpha):
    return (1 - bounce_out(1 - 2 * alpha)) / 2 if alpha < 0.5 else (1 + bounce_out(2 * alpha - 1)) / 2


def map(start, end, alpha, min_value=float("-inf"), max_value=float("inf")):
    return max(min(start + (end - start) * alpha, max_value), min_value)


PROPERTIES_MAPPERS = {
    int: map,
    float: map,
    Color: lambda start, end, alpha: Color(
        int(map(start.r, end.r, alpha, min_value=0, max_value=255)),
        int(map(start.g, end.g, alpha, min_value=0, max_value=255)),
        int(map(start.b, end.b, alpha, min_value=0, max_value=255)),
        int(map(start.a, end.a, alpha, min_value=0, max_value=255)),
    ),
    Vector2: lambda start, end, alpha: Vector2(map(start.x, end.x, alpha), map(start.y, end.y, alpha)),
    UDim2: lambda start, end, alpha: UDim2(
        map(start.x.scale, end.x.scale, alpha),
        map(start.x.offset, end.x.offset, alpha),
        map(start.y.scale, end.y.scale, alpha),
        map(start.y.offset, end.y.offset, alpha),
    ),
}

instantiated_tweens = []


class Tween(object):
    def __init__(
        self,
        instance: PyGuiInstance,
        properties: Dict[str, Any],
        duration: float = 1,
        tween_type: TweenType = TweenType.LINEAR,
    ) -> "Tween":
        self._original_properties = {}

        for property_name, property_value in properties.items():
            try:
                assert type(property_value) == type(instance[property_name])
            except TypeError:
                raise Exception(f"Property {property_name} expected type of {type(instance[property_name])} but got {type(property_value)}")
            except AttributeError:
                raise Exception(f"Property {property_name} is not a valid property")

            self._original_properties[property_name] = instance[property_name]

        self._instance = instance
        self._properties = properties

        self._duration = duration
        self._tween_type = tween_type

        self._tween_status = TweenStatus.PAUSED

        self._start_time = 0
        self._end_time = 0

        match tween_type:
            case TweenType.LINEAR:
                self._tween_function = lambda alpha: alpha
            case TweenType.SINE_IN:
                self._tween_function = sine_in
            case TweenType.SINE_OUT:
                self._tween_function = sine_out
            case TweenType.SINE_IN_OUT:
                self._tween_function = sine_in_out
            case TweenType.QUAD_IN:
                self._tween_function = quad_in
            case TweenType.QUAD_OUT:
                self._tween_function = quad_out
            case TweenType.QUAD_IN_OUT:
                self._tween_function = quad_in_out
            case TweenType.CUBIC_IN:
                self._tween_function = cubic_in
            case TweenType.CUBIC_OUT:
                self._tween_function = cubic_out
            case TweenType.CUBIC_IN_OUT:
                self._tween_function = cubic_in_out
            case TweenType.QUART_IN:
                self._tween_function = quart_in
            case TweenType.QUART_OUT:
                self._tween_function = quart_out
            case TweenType.QUART_IN_OUT:
                self._tween_function = quart_in_out
            case TweenType.QUINT_IN:
                self._tween_function = quint_in
            case TweenType.QUINT_OUT:
                self._tween_function = quint_out
            case TweenType.QUINT_IN_OUT:
                self._tween_function = quint_in_out
            case TweenType.EXPO_IN:
                self._tween_function = expo_in
            case TweenType.EXPO_OUT:
                self._tween_function = expo_out
            case TweenType.EXPO_IN_OUT:
                self._tween_function = expo_in_out
            case TweenType.CIRC_IN:
                self._tween_function = circ_in
            case TweenType.CIRC_OUT:
                self._tween_function = circ_out
            case TweenType.CIRC_IN_OUT:
                self._tween_function = circ_in_out
            case TweenType.BACK_IN:
                self._tween_function = back_in
            case TweenType.BACK_OUT:
                self._tween_function = back_out
            case TweenType.BACK_IN_OUT:
                self._tween_function = back_in_out
            case TweenType.ELASTIC_IN:
                self._tween_function = elastic_in
            case TweenType.ELASTIC_OUT:
                self._tween_function = elastic_out
            case TweenType.ELASTIC_IN_OUT:
                self._tween_function = elastic_in_out
            case TweenType.BOUNCE_IN:
                self._tween_function = bounce_in
            case TweenType.BOUNCE_OUT:
                self._tween_function = bounce_out
            case TweenType.BOUNCE_IN_OUT:
                self._tween_function = bounce_in_out
            case _:
                raise Exception(f"Unknown tween type {tween_type}")

        self.tween_ended = PyGuiSignal()

    @property
    def alpha(self) -> float:
        return max(0, min(1, (time.time() - self._start_time) / self._duration))

    def play(self):
        if self._tween_status == TweenStatus.PLAYING:
            raise Exception("Tween is already playing")

        self._tween_status = TweenStatus.PLAYING

        self._start_time = time.time()
        self._end_time = time.time() + self._duration

        instantiated_tweens.append(self)

        def on_tween_ended(tween_status: TweenStatus):
            instantiated_tweens.remove(self)

        self.tween_ended.connect(on_tween_ended)

    def pause(self):
        pass

    def cancel(self):
        for property_name, _ in self._properties.items():
            self._instance[property_name] = self._original_properties[property_name]

        self._tween_status = TweenStatus.CANCELED


def update(events: List[Event]):
    for tween in instantiated_tweens:
        tween._instance.BLOCKING_SCREEN_BUFFER_UPDATE = True

        tweened_alpha = tween._tween_function(tween.alpha)
        for property_name, property_value in tween._properties.items():
            tween._instance[property_name] = PROPERTIES_MAPPERS[type(property_value)](
                tween._original_properties[property_name],
                property_value,
                tweened_alpha,
            )

        if time.time() > tween._end_time:
            tween._tween_status = TweenStatus.ENDED

        if tween._tween_status != TweenStatus.PLAYING:
            tween.tween_ended.fire(tween._tween_status)

        tween._instance.BLOCKING_SCREEN_BUFFER_UPDATE = False
