from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field


I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:

    key: Point
    item: I
    subtree_size: int = field(default_factory=int)
    children: list[BeeNode | None] = field(default_factory=lambda: [None]*8)
    color: str = field(default="white")

    def get_octant_index(self, point: Point) -> int:
        assert len(point) == 3, f"Invalid point: {point}"
        if point == self.key:
            return -1  # or whatever you decide is best for your application
        index = 0
        if point[0] > self.key[0]: index |= 4
        if point[1] > self.key[1]: index |= 2
        if point[2] > self.key[2]: index |= 1
        return index
    
    def get_child_for_key(self, point: Point) -> BeeNode | None:
        index = self.get_octant_index(point)
        return self.children[index]

    def __hash__(self):
        return hash(self.key)
    
    


class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        self.root = None
        self.length = 0
        self.item = 0
        self.children = [None] * 8
        self.subtree_size = 0
        self.visited = set()
        self.color = field(default="white")

    def contains_cycle(self,node):
        if self.color == "gray":
            return True

        self.color = "gray"
        for child in self.children:
            if child is not None and self.contains_cycle(child):
                return True

        self.color = "black"
        return False    

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
            self.root = BeeNode(key, item, subtree_size=1)
        else:
            self.root = self.insert_aux(self.root, key, item)
        if self.root:
            self.root.subtree_size = 1 + sum(c.subtree_size for c in self.root.children if c is not None)
        self.length += 1

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        if current.key == key:
            return current 
        
        index = current.get_octant_index(key)
        
        if index == -1:  # if the point is the same as the current key
            current.item = item  # overwrite the current item with the new item
            return current

        try:
            if current.children[index] is None:
                current.children[index] = BeeNode(key, item, subtree_size=1)
            else:
                current.children[index] = self.insert_aux(current.children[index], key, item)
        except IndexError:
            print(f"Invalid index: {index}, Key: {key}, Current key: {current.key}, Children list length: {len(current.children)}")
            raise

        current.subtree_size = 1 + sum(c.subtree_size for c in current.children if c is not None)  # update current node's subtree_size

        # After insert operation, check for balance.
        if self.is_unbalanced(current):
            current = self.rebalance(current)

        return current
    
    def is_unbalanced(self, node: BeeNode) -> bool:
        subtree_sizes = [c.subtree_size for c in node.children if c is not None]
        if not subtree_sizes:  # if node has no children
            return False
        largest = max(subtree_sizes)
        smallest = min(subtree_sizes)
        return largest > 7 * smallest

    def rebuild(self, nodes: list[BeeNode]) -> BeeNode:
        if not nodes:
            return None
        # Sort nodes by key
        nodes.sort(key=lambda node: node.key)
        mid = len(nodes) // 2
        node = nodes[mid]
        # Recurse on left and right halves of nodes
        if len(nodes) < 8:
            node.children[:len(nodes)] = nodes
            node.children[len(nodes):] = [None] * (8 - len(nodes))
        else:
            octant_sizes = len(nodes) // 8  # calculate size of each octant
            node.children = [self.rebuild(nodes[i:i+octant_sizes]) for i in range(0, len(nodes), octant_sizes)]  # split nodes evenly into 8 octants
        # Update subtree_size of the current node
        node.subtree_size = 1 + sum(c.subtree_size for c in node.children if c is not None)
        return node

    def collect_nodes(self, node: BeeNode) -> list[BeeNode]:
        if node in self.visited:
            print(f"Node {node} has been visited before! Cycle detected.")
            return []
        self.visited.add(node)

        nodes = [node]
        for child in node.children:
            if child is not None:
                nodes.extend(self.collect_nodes(child))
        return nodes

    def rebalance(self, node: BeeNode) -> BeeNode:
        # Collect all nodes under the node to rebalance
        nodes = self.collect_nodes(node)
        # Clear children of node
        node.children = [None]*8
        # Rebuild subtree from collected nodes
        node = self.rebuild(nodes)
        return node

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2
    tdbt = ThreeDeeBeeTree()
    # ... insert some nodes ...
    if tdbt.contains_cycle(tdbt.root):
        print("Cycle detected!")
    else:
        print("No cycle found.")
