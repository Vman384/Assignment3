from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:

    key: Point
    item: I
    subtree_size: int = 1
    children: list[BeeNode | None] = field(default_factory=lambda: [None]*8)

    def get_octant_index(self, point: Point) -> int:
        index = 0
        if point[0] >= self.key[0]: index |= 4
        if point[1] >= self.key[1]: index |= 2
        if point[2] >= self.key[2]: index |= 1
        return index
    
    def get_child_for_key(self, point: Point) -> BeeNode | None:
        index = self.get_octant_index(point)
        return self.children[index]


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        return len(self) == 0

    def __len__(self) -> int:
        return self.length

    def __contains__(self, key: Point) -> bool:
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        current = self.root
        while current is not None:
            if current.key == key:
                return current
            else:
                for child in current.children:
                    if child is not None and child.key == key:
                        current = child
                        break
                else:
                    raise KeyError('Key not found in tree')
        raise KeyError('Key not found in tree')

    def __setitem__(self, key: Point, item: I) -> None:
        if self.root is None:
            self.root = BeeNode(key, item, subtree_size=1)  # Consider root in the subtree size
        else:
            self.root = self.insert_aux(self.root, key, item)
        self.root.subtree_size = 1 + sum(c.subtree_size for c in self.root.children if c is not None)  # update root's subtree_size
        self.length += 1

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        index = current.get_octant_index(key)
        if current.children[index] is None:
            current.children[index] = BeeNode(key, item, subtree_size=1)
        else:
            current.children[index] = self.insert_aux(current.children[index], key, item)
        current.subtree_size = 1 + sum(c.subtree_size for c in current.children if c is not None)  # update current node's subtree_size
        return current

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2
