"""
This module provides a basic implementation of Nodes
"""


class Node:
    """Node with next, ll"""

    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return f"node:{self.value}"


class NodeP:
    """Node with next and prev, dll"""

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return f"node:{self.value}"


class NodeLR:
    """Node with left and right, graph"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return f"node:{self.value}"
