from pygame import Vector2


class UDim(object):
    """
    Represents a one-dimensional user interface dimension (UDim) with a scale and offset.

    Args:
        scale (float): The scaling factor of the UDim.
        offset (float): The offset of the UDim.

    Methods:
        __add__(self, other: "UDim") -> "UDim": Addition of two UDim instances.
        __sub__(self, other: "UDim") -> "UDim": Subtraction of two UDim instances.
        __mul__(self, other: "UDim") -> "UDim": Multiplication of two UDim instances.
        __truediv__(self, other: "UDim") -> "UDim": Division of two UDim instances.
        __floordiv__(self, other: "UDim") -> "UDim": Floor division of two UDim instances.
        __str__(self) -> str: String representation of the UDim instance.

    Properties:
        scale (float): The scaling factor of the UDim.
        offset (float): The offset of the UDim.
    """

    def __init__(self, scale: float, offset: float) -> "UDim":
        self._vector = Vector2(scale, offset)

    @property
    def scale(self) -> float:
        """
        Returns:
            float: The scaling factor of the UDim.
        """
        return self._vector.x

    @property
    def offset(self) -> float:
        """
        Returns:
            float: The offset of the UDim.
        """
        return self._vector.y

    def __add__(self, other: "UDim") -> "UDim":
        """Adds two UDim instances."""
        return UDim(self.scale + other.scale, self.offset + other.offset)

    def __sub__(self, other: "UDim") -> "UDim":
        """Subtracts two UDim instances."""
        return UDim(self.scale - other.scale, self.offset - other.offset)

    def __mul__(self, other: "UDim") -> "UDim":
        """Multiplies two UDim instances."""
        return UDim(self.scale * other.scale, self.offset * other.offset)

    def __truediv__(self, other: "UDim") -> "UDim":
        """Divides two UDim instances."""
        return UDim(self.scale / other.scale, self.offset / other.offset)

    def __floordiv__(self, other: "UDim") -> "UDim":
        """Floor divides two UDim instances."""
        return UDim(self.scale // other.scale, self.offset // other.offset)

    def __str__(self) -> str:
        """Returns a string representation of the UDim instance."""
        return f"UDim({self.scale}, {self.offset})"


class UDim2(object):
    """
    Represents a two-dimensional user interface dimension (UDim2) with separate X and Y dimensions.

    Args:
        scale_x (float): The scaling factor of the X dimension.
        offset_x (float): The offset of the X dimension.
        scale_y (float): The scaling factor of the Y dimension.
        offset_y (float): The offset of the Y dimension.

    Methods:
        __add__(self, other: "UDim2") -> "UDim2": Addition of two UDim2 instances.
        __sub__(self, other: "UDim2") -> "UDim2": Subtraction of two UDim2 instances.
        __mul__(self, other: "UDim2") -> "UDim2": Multiplication of two UDim2 instances.
        __truediv__(self, other: "UDim2") -> "UDim2": Division of two UDim2 instances.
        __floordiv__(self, other: "UDim2") -> "UDim2": Floor division of two UDim2 instances.
        __str__(self) -> str: String representation of the UDim2 instance.

    Properties:
        x (UDim): The UDim instance for the X dimension.
        y (UDim): The UDim instance for the Y dimension.
    """

    def __init__(self, scale_x: float, offset_x: float, scale_y: float, offset_y: float) -> "UDim2":
        self._x = UDim(scale_x, offset_x)
        self._y = UDim(scale_y, offset_y)

    @property
    def x(self) -> UDim:
        """
        Returns:
            UDim: The UDim instance for the X dimension.
        """
        return self._x

    @x.setter
    def x(self, value: UDim):
        """
        Returns:
            UDim: The UDim instance for the X dimension.
        """
        self._x = value

    @property
    def y(self) -> UDim:
        """
        Returns:
            UDim: The UDim instance for the Y dimension.
        """
        return self._y

    @y.setter
    def y(self, value: UDim):
        """
        Returns:
            UDim: The UDim instance for the Y dimension.
        """
        self._y = value

    def __add__(self, other: "UDim2") -> "UDim2":
        """Adds two UDim2 instances."""
        return UDim2(
            self.x.scale + other.x.scale,
            self.x.offset + other.x.offset,
            self.y.scale + other.y.scale,
            self.y.offset + other.y.offset,
        )

    def __sub__(self, other: "UDim2") -> "UDim2":
        """Subtracts two UDim2 instances."""
        return UDim2(
            self.x.scale - other.x.scale,
            self.x.offset - other.x.offset,
            self.y.scale - other.y.scale,
            self.y.offset - other.y.offset,
        )

    def __mul__(self, other: "UDim2") -> "UDim2":
        """Multiplies two UDim2 instances."""
        return UDim2(
            self.x.scale * other.x.scale,
            self.x.offset * other.x.offset,
            self.y.scale * other.y.scale,
            self.y.offset * other.y.offset,
        )

    def __truediv__(self, other: "UDim2") -> "UDim2":
        """Divides two UDim2 instances."""
        return UDim2(
            self.x.scale / other.x.scale,
            self.x.offset / other.x.offset,
            self.y.scale / other.y.scale,
            self.y.offset / other.y.offset,
        )

    def __floordiv__(self, other: "UDim2") -> "UDim2":
        """Floor divides two UDim2 instances."""
        return UDim2(
            self.x.scale // other.x.scale,
            self.x.offset // other.x.offset,
            self.y.scale // other.y.scale,
            self.y.offset // other.y.offset,
        )

    def __str__(self) -> str:
        """Returns a string representation of the UDim2 instance."""
        return f"UDim2({self.x.scale}, {self.x.offset}, {self.y.scale}, {self.y.offset})"
