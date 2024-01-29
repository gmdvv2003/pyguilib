from typing import Any, Callable


class PyGuiConnection(object):
    ...


class PyGuiSignal(object):
    ...


class PyGuiConnection(object):
    """
    Represents a connection between a PyGuiSignal and a callback function.

    Args:
        signal (PyGuiSignal): The PyGuiSignal to be connected to.
        callback (Callable[[Any], Any]): The callback function to be connected.

    Methods:
        disconnect(self): Disconnects the connection from the associated PyGuiSignal.
    """

    def __init__(self, signal: PyGuiSignal, callback: Callable[[Any], Any]) -> "PyGuiConnection":
        self._connected = True
        self._next = None

        self._signal = signal
        self._callback = callback

    def disconnect(self):
        """Disconnects the connection from the associated PyGuiSignal."""
        self._connected = False

        if self._signal._handler_list_head == self:
            self._signal._handler_list_head = self._next
        else:
            current = self._signal._handler_list_head

            while current._next != self:
                current = current._next

            current._next = self._next


class PyGuiSignal(object):
    """
    Represents a signal in PyGui, allowing connections to callback functions.

    Methods:
        connect(self, callback: Callable[[Any], Any]) -> PyGuiConnection: Connects a callback function to the PyGuiSignal and returns a PyGuiConnection.
        fire(self, arguments: Any = None): Fires the PyGuiSignal, invoking all connected callback functions.
        wait(self): Placeholder method for potential future use.
    """

    def __init__(self) -> "PyGuiSignal":
        self._handler_list_head = None

    def connect(self, callback: Callable[[Any], Any]) -> PyGuiConnection:
        """
        Connects a callback function to the PyGuiSignal.

        Args:
            callback (Callable[[Any], Any]): The callback function to be connected.

        Returns:
            PyGuiConnection: The PyGuiConnection representing the connection.
        """
        connection = PyGuiConnection(self, callback)

        if self._handler_list_head:
            connection._next = self._handler_list_head

        self._handler_list_head = connection

        return connection

    def fire(self, arguments: Any = None):
        """
        Fires the PyGuiSignal, invoking all connected callback functions.

        Args:
            arguments (Any): The arguments to be passed to the connected callback functions.
        """
        item = self._handler_list_head
        while item:
            if item._connected:
                item._callback(arguments)

            item = item._next

    def wait(self):
        """Not implemented."""
        pass
