from typing import Any, Callable, List, Tuple

from pygame import Rect

CAPACITY = 6
MAX_DEPTH = 10

quadtrees_items_inventory = {}


class QuadTreeItem(object):
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
        return self._item

    @property
    def position(self) -> Tuple[int, int]:
        return self._get_location()

    @property
    def size(self) -> Tuple[int, int]:
        return self._get_size()

    @property
    def rect(self) -> Rect:
        return Rect(self.position, self.size)


class Quadtree(object):
    def __init__(self, depth: int, rect: Rect) -> "Quadtree":
        self._depth = depth
        self._rect = rect

        self._objects = []
        self._quadrants = []

        if depth == 0:
            quadtrees_items_inventory[self] = []

    def update(self):
        self._objects.clear()
        self._quadrants.clear()

        for item in quadtrees_items_inventory[self]:
            self.insert(item)

    def insert(self, item: QuadTreeItem):
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
        if self._rect.contains(item.rect):
            if item in self._objects:
                self._objects.remove(item)
            else:
                for quadrant in self._quadrants:
                    quadrant.remove(item)

    def subdivide(self):
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
        items = []

        if self._rect.contains(rect):
            for item in self._objects:
                if item.rect.contains(rect):
                    items.append(item)

            for quadrant in self._quadrants:
                items.extend(quadrant.query(rect))

        return items

    def reset(self):
        self._objects.clear()
        self._quadrants.clear()
