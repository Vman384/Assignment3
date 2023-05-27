from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil,floor
from bst import BinarySearchTree
from node import TreeNode

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        self.store = BinarySearchTree()
    
    def add_point(self, item: T):

        """
        Complexity : 

        Best case : The best case scenario for the add_point function is when the BST 
                    is either empty or the new item needs to be inserted at the root of the tree. 
                    In both cases, the operation is done immediately without any further traversal, 
                    hence the best case complexity is O(1).
        
        Worst case : The worst case scenario for the add_point function is when the new item needs to be inserted 
                     at a leaf node. This requires traversing from the root of the BST to a leaf. In a skewed tree 
                     (which resembles a linked list more than a tree), this traversal can be as long as n (the number 
                     of nodes in the tree), hence the worst-case time complexity is O(n).

        """
        self.store[item] = item 
    
    def remove_point(self, item: T):
        """
        Complexity : 

        Best case : The best case scenario for the remove_point function is when the 
                    item to be removed is at the root of the tree. In this case, the operation is 
                    done immediately without any further traversal. Therefore, the best case complexity is O(1).
        
        Worst case : The worst case scenario for the remove_point function is when the item to be removed is a leaf node. 
                     This requires traversing from the root of the BST to a leaf. If the tree is skewed (i.e., more like a 
                     linked list than a tree), this path can be as long as n (the number of nodes in the tree), hence the worst-case
                     time complexity is O(n).
        
        """
        del self.store[item]

    
    def ratio(self, x, y) -> list[T]:

        """
        
        Complexity : 

        Best case : If the kth_smallest method finds the nodes at the root and the ratio_aux only visits the root, 
                    the best case time complexity will be O(1) for each, resulting in an overall best case complexity of O(1).
        
        Worst case : If both kth_smallest calls traverse the entire tree and ratio_aux also visits every node in the tree, the 
                     worst case time complexity will be O(n) for each, resulting in an overall worst case complexity of O(3n) which simplifies to O(n) as we generally ignore constants in Big O notation.
        
        """
        bottom = self.store.kth_smallest(ceil((x/100) * self.store.length+1),self.store.root)
        top = self.store.kth_smallest(floor(self.store.length - (self.store.length * (y/100))),self.store.root)
        values = []

        def ratio_aux(current: TreeNode):
            """
            Complexity :

            Best case : The best-case scenario for ratio_aux function is when the tree is perfectly balanced, the root node 
                        falls between the range bottom.key and top.key, and there is no need to make recursive calls to the left 
                        and right children of the root node. In this case, the time complexity of the function would be constant 
                        i.e., O(1).
            
            Worst case : The worst-case scenario for the ratio_aux function is when the tree is heavily skewed either to the left or 
                         right (essentially becoming a linked list), or when all nodes fall in the range defined by bottom.key and top.key, 
                         requiring to visit every node in the tree. The function makes recursive calls to left and right children of the current node, so in the worst-case scenario, it would visit all nodes in the tree. If there are n nodes in the tree, the time complexity of the function would be linear i.e., O(n).
            
            """
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
