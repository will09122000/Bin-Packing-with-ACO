class Node:
    """A class to represent a single node in the graph navigated by the ants."""

    def __init__(self, bin, item):
        self.bin = bin
        self.item = item
        self.edges = []
