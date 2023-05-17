from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree
from node import TreeNode

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        self.store = BinarySearchTree()
    
    def add_point(self, item: T):
        self.store[item] = item 
    
    def remove_point(self, item: T):
        del self.store[item]

    
    def ratio(self, x, y) -> list[T]:
        bottom = self.store.kth_smallest(ceil((x/100) * self.store.length+1),self.store.root)
        top = self.store.kth_smallest(ceil(self.store.length - (self.store.length * (y/100))),self.store.root)
        values = []

        def ratio_aux(current: TreeNode):
            if current is not None:
                if bottom.key <= current.key <= top.key:
                    values.append(current.key)

                if current.left is not None and current.key >= bottom.key:
                    ratio_aux(current.left) 

                if current.right is not None and current.key <= top.key:
                    ratio_aux(current.right)
        ratio_aux(self.store.root)
        return values



if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
