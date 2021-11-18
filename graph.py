import random

from node import Node
from edge import Edge

class Graph:

    def __init__(self, bins, items):
        self.nodes = self.create_nodes(bins, items)
        self.create_edges(bins, items)

    def create_nodes(self, bins, items):
        nodes = []

        # Start node.
        nodes.append(Node(None, None))

        for item in items:
            for bin in range(0, bins):
                nodes.append(Node(bin, item))

        # End node.
        nodes.append(Node(None, None))

        return nodes

    def create_edges(self, bins, items):

        # Start node.
        for destination_node in self.nodes[1:bins+1]:
            edge = Edge(destination_node)
            self.nodes[0].edges.append(edge)

        # Iterate through all nodes that are not the start or end nodes.
        next_item = 0
        for node in self.nodes[1:-1]:
            if node.item != len(items):
                next_item = node.item + 1
                #for destination_node in self.nodes[i+1:i+bins+1]:
                for destination_node in self.nodes:
                    if destination_node.item == next_item:
                        edge = Edge(destination_node)
                        node.edges.append(edge)
            # Bins for the last item all point to the end node.
            else:
                edge = Edge(destination=self.nodes[-1])
                node.edges.append(edge)
    
    def add_pheromone(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.pheromone = random.random()

    def generate_paths(self, p, num_bins):
        paths = []

        for _ in range(0, p):
            path = []
            choice = random.random()
            cumulative = 0

            for edge in self.nodes[0].edges:
                cumulative += edge.pheromone
                if choice <= cumulative:
                    destination_node = edge.destination
                    break
            path.append(destination_node)

            for _ in range(1, len(self.nodes)-num_bins-1, num_bins):
                cumulative = 0
                for edge in path[-1].edges:
                    cumulative += edge.pheromone
                    if choice <= cumulative:
                        destination_node = edge.destination
                        break
                path.append(destination_node)

            paths.append(path)

        for path in paths:
            for node in path:
                print('bin: ' + str(node.bin) + ', item: ' + str(node.item) + 'kg')
            print()
