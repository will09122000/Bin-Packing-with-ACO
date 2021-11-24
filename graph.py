import random

from node import Node
from edge import Edge

class Graph:

    def __init__(self, bins, items):
        self.bins = bins
        self.items = items

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
        for node in self.nodes[1:bins+1]:
            edge = Edge(self.nodes[0], node)
            self.nodes[0].edges.append(edge)

        # Iterate through all nodes that are not the start or end nodes.
        next_item = 0
        for node in self.nodes[1:-1]:
            if node.item != len(items):
                next_item = node.item + 1
                for destination_node in self.nodes:
                    if destination_node.item == next_item:
                        edge = Edge(node, destination_node)
                        node.edges.append(edge)
            # Bins for the last item all point to the end node.
            else:
                edge = Edge(node, self.nodes[-1])
                node.edges.append(edge)
    
    def add_pheromone(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.pheromone = random.random()

    def generate_paths(self, p, num_bins):
        paths = []

        for _ in range(0, p):
            path = []

            cumulative = 0
            total_pheromone = 0

            for edge in self.nodes[0].edges:
                total_pheromone += edge.pheromone
            choice = random.uniform(0, total_pheromone)

            # First decision
            for edge in self.nodes[0].edges:
                cumulative += edge.pheromone
                if choice <= cumulative:
                    route_taken = edge
                    break
            path.append(route_taken)

            for _ in range(1, len(self.nodes)-num_bins-1, num_bins):
                cumulative = 0
                total_pheromone = 0

                for edge in path[-1].destination.edges:
                    total_pheromone += edge.pheromone
                choice = random.uniform(0, total_pheromone)

                for edge in path[-1].destination.edges:
                    cumulative += edge.pheromone
                    if choice <= cumulative:
                        route_taken = edge
                        break
                path.append(route_taken)

            # Last node in the path will always have one edge to the end node (E).
            path.append(path[-1].destination.edges[0])

            paths.append(path)

        return paths

    def calculate_path_fitness(self, path):
        bin_weights = [0] * self.bins

        for edge in path:
            if edge.start.bin != None:
                bin_weights[edge.start.bin] += edge.start.item

        return max(bin_weights) - min(bin_weights)

    def update_pheromones(self, paths):
        for path in paths:
            fitness = self.calculate_path_fitness(path)
            for edge in path:
                if fitness > 0:
                    edge.pheromone += 100 / fitness
                else:
                    edge.pheromone += 100
                    #print("Found perfect solution.")

    def evaporate_pheromone(self, evaporation_rate):
        for node in self.nodes:
            for edge in node.edges:
                edge.pheromone *= evaporation_rate