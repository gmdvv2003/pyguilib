from typing import Any, Callable, List, Tuple

from pygame import Rect

CAPACITY = 6
MAX_DEPTH = 10

quadtrees_items_inventory = {}


class QuadTreeItem(object):
    """
    Represents an item within a Quadtree.

    Args:
        item (Any): The item to be stored in the QuadTreeItem.
        get_location (Callable[[None], Tuple[int, int]]): A function that returns the location of the item.
        get_size (Callable[[None], Tuple[int, int]]): A function that returns the size of the item.

    Properties:
        item (Any): The item stored in the QuadTreeItem.
        position (Tuple[int, int]): The position of the item.
        size (Tuple[int, int]): The size of the item.
        rect (Rect): The Rect object representing the item's position and size.
    """

    def __init__(
        self,
        item: Any,
        get_location: Callable[[None], Tuple[int, int]],
        get_size: Callable[[None], Tuple[int, int]],
    ) -> "QuadTreeItem":
        self._item = item
        self._get_location = get_location
        self._get_size = get_size

    @property
    def item(self) -> Any:
        """
        Returns the item stored in the QuadTreeItem.

        Returns:
            Any: The item stored in the QuadTreeItem.
        """
        return self._item

    @property
    def position(self) -> Tuple[int, int]:
        """
        Returns the position of the item.

        Returns:
            Tuple[int, int]: The position of the item.
        """
        return self._get_location()

    @property
    def size(self) -> Tuple[int, int]:
        """
        Returns the size of the item.

        Returns:
            Tuple[int, int]: The size of the item.
        """
        return self._get_size()

    @property
    def rect(self) -> Rect:
        """
        Returns a Rect object representing the item's position and size.

        Returns:
            Rect: The Rect object representing the item's position and size.
        """
        return Rect(self.position, self.size)


class Quadtree(object):
    """
    Represents a Quadtree data structure for spatial partitioning.

    Args:
        depth (int): The depth of the Quadtree.
        rect (Rect): The Rect object representing the Quadtree's position and size.

    Methods:
        update(self): Updates the Quadtree by reinserting all items from the global inventory.
        insert(self, item: QuadTreeItem): Inserts a QuadTreeItem into the Quadtree.
        remove(self, item: QuadTreeItem): Removes a QuadTreeItem from the Quadtree.
        subdivide(self): Subdivides the Quadtree into four sub-Quadtrees.
        query(self, rect: Rect) -> List[QuadTreeItem]: Queries the Quadtree for items within a given Rect.
        reset(self): Resets the Quadtree by clearing objects and sub-Quadtrees.
    """

    def __init__(self, depth: int, rect: Rect) -> "Quadtree":
        self._depth = depth
        self._rect = rect

        self._objects = []
        self._quadrants = []

        if depth == 0:
            quadtrees_items_inventory[self] = []

    def update(self):
        """Updates the Quadtree by reinserting all items from the global inventory."""
        self._objects.clear()
        self._quadrants.clear()

        for item in quadtrees_items_inventory[self]:
            self.insert(item)

    def insert(self, item: QuadTreeItem):
        """
        Inserts a QuadTreeItem into the Quadtree.

        Args:
            item (QuadTreeItem): The QuadTreeItem to be inserted.
        """
        if self._rect.contains(item.rect):
            if len(self._objects) < CAPACITY or self._depth > MAX_DEPTH:
                self._objects.append(item)
            else:
                if not self._quadrants:
                    self.subdivide()

                self._quadrants[0].insert(item)
                self._quadrants[1].insert(item)
                self._quadrants[2].insert(item)
                self._quadrants[3].insert(item)

    def remove(self, item: QuadTreeItem):
        """
        Removes a QuadTreeItem from the Quadtree.

        Args:
            item (QuadTreeItem): The QuadTreeItem to be removed.
        """
        if self._rect.contains(item.rect):
            if item in self._objects:
                self._objects.remove(item)
            else:
                for quadrant in self._quadrants:
                    quadrant.remove(item)

    def subdivide(self):
        """Subdivides the Quadtree into four sub-Quadtrees."""
        width = self._rect.width
        height = self._rect.height

        (center_x, center_y) = self._rect.center

        top_left_x = center_x - width / 2
        top_left_y = center_y - height / 2

        self._quadrants.append(Quadtree(self._depth + 1, Rect(top_left_x, top_left_y, width / 2, height / 2)))
        self._quadrants.append(Quadtree(self._depth + 1, Rect(center_x, top_left_y, width / 2, height / 2)))
        self._quadrants.append(Quadtree(self._depth + 1, Rect(top_left_x, center_y, width / 2, height / 2)))
        self._quadrants.append(Quadtree(self._depth + 1, Rect(center_x, center_y, width / 2, height / 2)))

    def query(self, rect: Rect) -> List[QuadTreeItem]:
        """
        Queries the Quadtree for items within a given Rect.

        Args:
            rect (Rect): The Rect representing the query area.

        Returns:
            List[QuadTreeItem]: The list of QuadTreeItems within the query area.
        """
        items = []

        if self._rect.contains(rect):
            for item in self._objects:
                if item.rect.contains(rect):
                    items.append(item)

            for quadrant in self._quadrants:
                items.extend(quadrant.query(rect))

        return items

    def reset(self):
        """Resets the Quadtree by clearing objects and sub-Quadtrees."""
        self._objects.clear()
        self._quadrants.clear()
