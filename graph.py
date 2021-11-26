import random
from datetime import datetime

from node import Node
from edge import Edge

class Graph:

    def __init__(self, b, items):
        self.b = b
        self.items = items

        self.nodes = self.create_nodes(b, items)
        self.create_edges(b)

    def create_nodes(self, b, items):
        nodes = []

        # Start node.
        nodes.append(Node(None, None))

        for item in items:
            for bin_id in range(0, b):
                nodes.append(Node(bin_id, item))

        # End node.
        nodes.append(Node(None, None))

        return nodes

    def create_edges(self, b):

        # Add initial edges to the start node.
        for node in self.nodes[1:b+1]:
            edge = Edge(self.nodes[0], node)
            self.nodes[0].edges.append(edge)

        # Iterate through nodes that need an edge pointing to an active node.
        for i in range(1, len(self.nodes)-b-1, b):
            for j in range(i, i+b):
                start_node = self.nodes[j]
                for k in range(i+b, i+(b*2)):
                    destination_node = self.nodes[k]
                    edge = Edge(start_node, destination_node)
                    start_node.edges.append(edge)

        # Iterate through nodes that point to the end node.
        for i in range(len(self.nodes)-b-1, len(self.nodes)-1):
            start_node = self.nodes[i]
            edge = Edge(start_node, self.nodes[-1])
            start_node.edges.append(edge)

    def add_pheromone(self):
        for node in self.nodes:
            for edge in node.edges:
                edge.pheromone = random.random()

    def generate_paths(self, p, b):
        paths = []
        start = datetime.now()
        for _ in range(0, p):
            path = []

            # First decision.
            route_taken = self.pick_route(self.nodes[0].edges)
            path.append(route_taken)

            for _ in range(1, len(self.nodes)-b-1, b):
                route_taken = self.pick_route(path[-1].destination.edges)
                path.append(route_taken)

            # Last node in the path will always have one edge to the end node (E).
            path.append(path[-1].destination.edges[0])

            paths.append(path)

        return paths, datetime.now() - start

    def pick_route(self, edges):
        cumulative = 0
        total_pheromone = 0

        for edge in edges:
            total_pheromone += edge.pheromone
        choice = random.uniform(0, total_pheromone)

        for edge in edges:
            cumulative += edge.pheromone
            if choice <= cumulative:
                route_taken = edge
                break

        #route_taken = edges[random.randint(0, len(edges)-1)]

        return route_taken

    def calculate_path_fitness(self, path):
        bin_weights = [0] * self.b

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

    def best_path(self, paths):
        best_path = paths[0]
        best_fitness = self.calculate_path_fitness(paths[0])

        for path in paths[1:]:
            path_fitness = self.calculate_path_fitness(path)
            if path_fitness < best_fitness:
                best_path = path
                best_fitness = path_fitness

        return best_path, best_fitness
