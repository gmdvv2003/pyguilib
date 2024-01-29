from typing import Any, Callable


class PyGuiConnection(object):
    ...


class PyGuiSignal(object):
    ...


class PyGuiConnection(object):
    def __init__(self, signal: PyGuiSignal, callback: Callable[[Any], Any]) -> "PyGuiConnection":
        self._connected = True
        self._next = None

        self._signal = signal
        self._callback = callback

    def disconnect(self):
        self._connected = False

        if self._signal._handler_list_head == self:
            self._signal._handler_list_head = self._next
        else:
            current = self._signal._handler_list_head

            while current._next != self:
                current = current._next

            current._next = self._next


class PyGuiSignal(object):
    def __init__(self) -> "PyGuiSignal":
        self._handler_list_head = None

    def connect(self, callback: Callable[[Any], Any]) -> PyGuiConnection:
        connection = PyGuiConnection(self, callback)

        if self._handler_list_head:
            connection._next = self._handler_list_head

        self._handler_list_head = connection

        return connection

    def fire(self, arguments: Any = None):
        item = self._handler_list_head
        while item:
            if item._connected:
                item._callback(arguments)

            item = item._next

    def wait(self):
        pass
