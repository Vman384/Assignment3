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
        """
        Complexity : 

        Best case : The get_octant_index function operates in constant time, i.e., O(1). This is because it 
                    performs a fixed number of operations that do not depend on the size or shape of the tree, or the 
                    number of children.
        
        Worst case :  Similarly, the worst case time complexity is also O(1). Even in the worst case scenario, the function 
                      performs the same fixed number of operations: comparing the dimensions of the point with the dimensions 
                      of the node's key and calculating the octant index. Therefore, the time complexity does not depend on the 
                      size of the tree or any other variable parameters.
        """
        index = 0
        if point[0] >= self.key[0]: index |= 4
        if point[1] >= self.key[1]: index |= 2
        if point[2] >= self.key[2]: index |= 1
        return index
    
    def get_child_for_key(self, point: Point) -> BeeNode | None:
        """
        Complexity :

        Best case : The function get_child_for_key requires calculating the octant index and 
                    accessing the child at that index in the children array. Both of these operations 
                    take constant time, i.e., their time complexity is not dependent on the size or shape of the 
                    tree or the number of children. Therefore, the best case time complexity is O(1).
        
        worst case : Similarly, the worst case time complexity is also O(1) because even in the worst case, the function 
                     is just performing a fixed number of operations: calculating the octant index and accessing the child 
                     at that index. It doesn't need to traverse or search through the tree or the list of children.
        
        """
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
        """
        Complexity : 

        Best case : The best case scenario would be if the key we're looking for is 
                    located at the root of the tree, which means we would find the key in 
                    constant time, so the best case time complexity would be O(1).
        
        Worst case : The worst case scenario would be if the key we're looking for is located at one 
                     of the leaf nodes of the tree, in which case we would have to traverse down to the leaf 
                     level of the Octree. The number of steps it takes to reach a leaf node is proportional to the 
                     height of the tree. For a balanced Octree, this would result in a worst case time complexity of O(log n). 
                     However, in an unbalanced Octree, it can degrade to O(n), where n is the number of nodes in the tree.
        
        """
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

        """
        Complexity :

        Best case : The best case scenario occurs when there is no root (the tree is empty), 
                    in which case the operation takes constant time, O(1), to set the root.

        Worst case : The worst case scenario occurs when the tree is filled, and the new key to be inserted is 
                     located at a leaf node of the tree. We would have to traverse down to the leaf level of the Octree.
                     The time complexity of this operation is dependent on the depth of the tree. In a balanced Octree, 
                     the depth is proportional to log(n) where n is the number of nodes. Therefore, the worst case time 
                     complexity would be O(log n) for a balanced Octree. However, in case of an unbalanced Octree, 
                     the time complexity can degrade to O(n), where n is the number of nodes in the tree.
        
        """
        if self.root is None:
            self.root = BeeNode(key, item, subtree_size=1)  # Consider root in the subtree size
        else:
            self.root = self.insert_aux(self.root, key, item)
        self.root.subtree_size = 1 + sum(c.subtree_size for c in self.root.children if c is not None)  # update root's subtree_size
        self.length += 1

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
        Complexity :

        Best case : The best case scenario occurs when the key to be inserted corresponds to an empty child 
                    of the current node. In this case, the function just inserts the new node and updates the 
                    subtree_size which takes constant time. Thus, the best case time complexity is O(1).
        
        Worst case : The worst case scenario happens when the tree is filled and the new key to be inserted is 
                     located at a leaf node of the tree. The function would have to traverse down to the leaf level of the Octree. 
                     The time complexity of this operation is dependent on the depth of the tree. In a balanced Octree, the depth 
                     is proportional to log(n) where n is the number of nodes. So, in the worst case, the time complexity would be 
                     O(log n). However, for an unbalanced Octree, the time complexity can degrade to O(n), where n is the number of 
                     nodes in the tree.
        
        """
        index = current.get_octant_index(key)
        if current.children[index] is None:
            current.children[index] = BeeNode(key, item, subtree_size=1)
        else:
            current.children[index] = self.insert_aux(current.children[index], key, item)
        current.subtree_size = 1 + sum(c.subtree_size for c in current.children if c is not None)  # update current node's subtree_size
        return current
    
    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """
        pass
        # Not needed to complete the task efficiently

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2