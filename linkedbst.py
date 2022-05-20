"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a level order traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def _height1(top):
            # Helper function
            """Return the height of the subtree rooted at Position p."""
            if top is None:
                return 0
            elif top.left is None and top.right is None:
                return 0
            else:
                return 1 + max(_height1(child)
                               for child in [top.left, top.right])

        start = self._root
        return _height1(start)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        height = self.height()
        size = self._size
        if height < (2 * log(size + 1, 2) - 1):
            return True
        else:
            return False

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        :param low:
        :param high:
        :return:
        """
        tree_list = self._bin_search_tree_to_list()
        smallest = tree_list[0]
        i = 0
        while smallest < low:
            i += 1
            if i >= self._size:
                i = self._size - 1
                break
            smallest = tree_list[i]
        largest = tree_list[-1]
        j = self._size - 1
        while largest > high:
            j -= 1
            if j < 0:
                j = 0
            largest = tree_list[j]
        return tree_list[i:j]

    def _bin_search_tree_to_list(self):
        """returns list from tree elements"""

        def recurse(node):
            """returns list of elements under node, using recursive"""
            if node is None:
                return []
            return recurse(node.left) + [node.data] + recurse(node.right)

        start = self._root
        return recurse(start)

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """

        def list_to_node(lst):
            """takes list and returns root node of balanced tree, using recursive"""
            length = len(lst)
            if length == 0:
                return None
            elif length == 1:
                return BSTNode(lst[0])
            # elif length == 2:
            #     return BSTNode(lst[1], left = BSTNode(lst[0]))
            else:
                return BSTNode(lst[length // 2], list_to_node(lst[:length // 2]), list_to_node(lst[(length // 2) + 1:]))

        tree_list = self._bin_search_tree_to_list()
        self.clear()
        self._root = list_to_node(tree_list)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_list = self._bin_search_tree_to_list()
        smallest = tree_list[0]
        i = 0
        while smallest <= item:
            i += 1
            if i >= self._size:
                return None
            smallest = tree_list[i]
        return smallest

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        tree_list = self._bin_search_tree_to_list()
        largest = tree_list[-1]
        i = self._size - 1
        while largest >= item:
            i -= 1
            if i < 0:
                return None
            largest = tree_list[i]
        return largest

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        lst_of_words = []
        with open(path, "r") as file:
            for line in file:
                lst_of_words.append(line.strip("\n"))
        """час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику (пошук у списку слів з використанням методів вбудованого типу list).
 час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку. Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника, який впорядкований за абеткою.
час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку. Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника який не впорядкований за абеткою (слова у дерево додаються випадковим чином).
час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку після його балансування."""
        print("time for finding 10000 random words:")
        time_since = time.time()
        for _ in range(992):
            word = random.choice(lst_of_words)
            i = lst_of_words.index(word)
        time_since = time.time() - time_since
        print(time_since, "sec  in alphabet ranged list = ", )

        bin_tree = LinkedBST()
        for word in lst_of_words:
            bin_tree.add(word)
        time_since = time.time()
        for _ in range(992):
            word = random.choice(lst_of_words)
            i = bin_tree.find(word)
        time_since = time.time() - time_since
        print(time_since, "sec  in binary search tree, to which nodes were added in alphabetical order")

        bin_tree.clear()
        lst_words = lst_of_words.copy()
        random.shuffle(lst_words)
        for word in lst_words:
            bin_tree.add(word)
        time_since = time.time()
        for _ in range(992):
            word = random.choice(lst_of_words)
            i = bin_tree.find(word)
        time_since = time.time() - time_since
        print(time_since, "sec  in binary search tree, which nodes were added randomly")

        bin_tree.rebalance()
        time_since = time.time()
        for _ in range(992):
            word = random.choice(lst_of_words)
            i = bin_tree.find(word)
        time_since = time.time() - time_since
        print(time_since, "sec  in balanced binary tree")


tree = LinkedBST()
tree.demo_bst("word1.txt")
