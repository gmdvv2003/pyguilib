from pygame import Vector2


class UDim(object):
    def __init__(self, scale: float, offset: float) -> "UDim":
        self._vector = Vector2(scale, offset)

    @property
    def scale(self) -> float:
        return self._vector.x

    @property
    def offset(self) -> float:
        return self._vector.y

    def __add__(self, other: "UDim") -> "UDim":
        return UDim(self.scale + other.scale, self.offset + other.offset)

    def __sub__(self, other: "UDim") -> "UDim":
        return UDim(self.scale - other.scale, self.offset - other.offset)

    def __mul__(self, other: "UDim") -> "UDim":
        return UDim(self.scale * other.scale, self.offset * other.offset)

    def __truediv__(self, other: "UDim") -> "UDim":
        return UDim(self.scale / other.scale, self.offset / other.offset)

    def __floordiv__(self, other: "UDim") -> "UDim":
        return UDim(self.scale // other.scale, self.offset // other.offset)

    def __str__(self) -> str:
        return f"UDim({self.scale}, {self.offset})"


class UDim2(object):
    def __init__(self, scale_x: float, offset_x: float, scale_y: float, offset_y: float) -> "UDim2":
        self._x = UDim(scale_x, offset_x)
        self._y = UDim(scale_y, offset_y)

    @property
    def x(self) -> UDim:
        return self._x

    @x.setter
    def x(self, value: UDim):
        self._x = value

    @property
    def y(self) -> UDim:
        return self._y

    @y.setter
    def y(self, value: UDim):
        self._y = value

    def __add__(self, other: "UDim2") -> "UDim2":
        return UDim2(
            self.x.scale + other.x.scale,
            self.x.offset + other.x.offset,
            self.y.scale + other.y.scale,
            self.y.offset + other.y.offset,
        )

    def __sub__(self, other: "UDim2") -> "UDim2":
        return UDim2(
            self.x.scale - other.x.scale,
            self.x.offset - other.x.offset,
            self.y.scale - other.y.scale,
            self.y.offset - other.y.offset,
        )

    def __mul__(self, other: "UDim2") -> "UDim2":
        return UDim2(
            self.x.scale * other.x.scale,
            self.x.offset * other.x.offset,
            self.y.scale * other.y.scale,
            self.y.offset * other.y.offset,
        )

    def __truediv__(self, other: "UDim2") -> "UDim2":
        return UDim2(
            self.x.scale / other.x.scale,
            self.x.offset / other.x.offset,
            self.y.scale / other.y.scale,
            self.y.offset / other.y.offset,
        )

    def __floordiv__(self, other: "UDim2") -> "UDim2":
        return UDim2(
            self.x.scale // other.x.scale,
            self.x.offset // other.x.offset,
            self.y.scale // other.y.scale,
            self.y.offset // other.y.offset,
        )

    def __str__(self) -> str:
        return f"UDim2({self.x.scale}, {self.x.offset}, {self.y.scale}, {self.y.offset})"
