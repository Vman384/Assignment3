""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys


# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        """
        Complexity :

        Best case : The best case scenario is when the key 
                    is found in the root of the tree. In this case, 
                    the time complexity is O(1) because only one comparison is needed.
        
        Worst case : The worst case scenario occurs when the tree is skewed and the key is 
                     located in a leaf node. In this scenario, the method has to traverse from 
                     the root to a leaf. If the tree is skewed, this path can be as long as n 
                     (the number of nodes in the tree), so the worst-case time complexity is O(n).

        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
        Complexity:

        Best case : The best case scenario is when the key is found at the node 
                    which the function starts its search from (it's the 'current' node passed as an 
                    argument to the function). This would mean the key was found immediately without
                    any further recursive calls. Hence, in the best case, the time complexity is O(1).
        
        Worst case : The worst case scenario is similar to get_tree_node_by_key when the tree is skewed. 
                     If the key is located at one of the leaf nodes, the function would have to traverse 
                     from the current node to a leaf node. If the tree is skewed, this path can be as l
                     long as n (the number of nodes in the tree), so the worst-case time complexity is O(n).
        
        """

        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        """
        Complexity : Refer to insert_aux

        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            self.length += 1
        elif key < current.key:
            current.subtree_size+=1
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.subtree_size+=1
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.

            Complexity : 

            Best case : The best case scenario is when the key is located at the root of 
                        the tree. In this case, the time complexity is O(1) if the tree has two or 
                        fewer nodes. However, if the tree has more than two nodes, finding a successor for the root 
                        (when the root has two children) could take up to O(log n) in a balanced tree and O(n) in a skewed 
                        tree. So, in a general scenario, the best case complexity is O(log n) for a balanced tree and O(n) for 
                        a skewed tree.

            Worst case : The worst case scenario occurs when the tree is skewed (i.e., when the keys are not evenly distributed 
                         and the tree takes the shape of a linear linked list). In this case, if the key to be deleted is at one 
                         of the leaf nodes, the method would have to traverse from the root to a leaf. Hence, the worst-case time 
                         complexity is O(n).

        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left  = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.subtree_size -= 1
        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a child node having the smallest key among all the
            larger keys.

            Complexity :

            Best case : The best case scenario occurs when the right child of the current node 
                        is a leaf node or the right child of the current node doesn't have a left child. 
                        In this case, the successor is the right child itself and we don't need to traverse further. 
                        Hence, the best case complexity is O(1).
            
            Worst case : The worst case scenario happens when the right child of the current node has a left child and all 
                         nodes on the right side of the tree also have left children. In this case, we have to traverse down 
                         the leftmost path of the right subtree until we reach a leaf node. If the tree is skewed, this path 
                         can be as long as n (the number of nodes in the tree), so the worst-case time complexity is O(n).
        """
        if current.right is None:
            return None    
        return self.get_minimal(current.right)

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.

            Complexity :

            Best case : The best case scenario is when the given node has no left child. 
                        In this case, the given node itself has the smallest key in its subtree, 
                        so no further traversal is necessary. Hence, the best case complexity is O(1).
            
            Worst case : The worst case scenario is when each node on the path has a left child, meaning we 
                         have to traverse from the root of the subtree to a leaf. If the subtree is 
                         skewed (i.e., more like a linked list than a tree), this path can be as long as n 
                         (the number of nodes in the subtree). Thus, the worst-case time complexity is O(n).
        """

        if current.left is not None:
            return self.get_minimal(current.left)
        return current
        
    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left,  prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode:
        """
        Finds the kth smallest value by key in the subtree rooted at current.

        Complexity :

        Best case : The best case scenario occurs when k equals the size of the left 
                    subtree plus one. This means the kth_smallest is at the root of the subtree,
                    which is found immediately without any further recursive calls. Hence, the best case complexity is O(1).
        
        Worst case : The worst case scenario is when the k-th smallest element is a leaf node, which requires traversing from 
                     the root of the subtree to the leaf. This is analogous to searching for a key in the BST. If the tree is 
                     skewed, this path can be as long as n (the number of nodes in the tree), so the worst-case time complexity 
                     is O(n).
        """
        if current is not None:
            # Compute the size of the left subtree
            left_size = current.left.subtree_size if current.left else 0

            if k <= left_size: 
                return self.kth_smallest(k, current.left)
            elif k == left_size + 1: 
                return current
            else: 
                return self.kth_smallest(k - left_size - 1, current.right)
                #k- left_size-1 as its defs not in left half therefore you have to minus that and its not current node 
                #therefore -1

        



