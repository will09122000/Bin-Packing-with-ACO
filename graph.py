from datetime import datetime
from random import uniform

from node import Node
from edge import Edge

class Graph:
    """
    A class to represent the graph navigated by ants in the colony representing the bin packing
    problem.

    Attributes
    ----------
    items:  list[int] | A list of items that are to be packed into bins, the number represents the
                        weight of the item.
    b:            int | The number of bins the above items can be packed into.
    nodes: list[Node] | A list of all nodes in the graph.
    """

    def __init__(self, b, items):
        self.items = items
        self.b = b
        self.nodes = self.create_nodes(b, items)
        self.create_edges(b)

    def create_nodes(self, b, items):
        """Creates all nodes required for the graph."""
        nodes = []

        # Start node.
        nodes.append(Node(None, None))

        # Each combination of item and bin will have its own node.
        for item in items:
            for bin_id in range(0, b):
                nodes.append(Node(bin_id, item))

        # End node.
        nodes.append(Node(None, None))

        return nodes

    def create_edges(self, b):
        """
        Creates all edges between the nodes to allow the ants to navigate the graph.
        """

        # Add initial edges to the start node.
        for node in self.nodes[1:b+1]:
            edge = Edge(self.nodes[0], node)
            self.nodes[0].edges.append(edge)

        # Iterate through all nodes that need an edge pointing to another active node (Not pointing
        # to the end node).
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
        """Add the initial random pheromone to each edge in the graph."""

        for node in self.nodes:
            for edge in node.edges:
                edge.randomise_pheromone()

    def generate_paths(self, p, b):
        """Generate a path for each ant in the colony."""

        paths = []
        start = datetime.now()

        # Repeat for each ant that needs a path.
        for _ in range(0, p):
            path = []

            # First decision.
            route_taken = self.pick_route(self.nodes[0].edges)
            path.append(route_taken)

            # Repeat for the number of route decisions that need to be made by the ant (apart from
            # the last and first decision).
            for _ in range(1, len(self.nodes)-b-1, b):
                # Pick the edge.
                route_taken = self.pick_route(path[-1].destination.edges)
                # Add the edge to that path.
                path.append(route_taken)

            # Last node in the path will always point to the end node.
            path.append(path[-1].destination.edges[0])

            paths.append(path)

        return paths, datetime.now() - start

    def pick_route(self, edges):
        """Picks a route for an ant from a list of edges."""

        total_pheromone = 0

        # Pick a random float between 0 and the total amount of pheromone in the list of edges.
        for edge in edges:
            total_pheromone += edge.pheromone
        choice = uniform(0, total_pheromone)

        cumulative = 0
        # Pick an edge by summing the pheromone of each edge until it is less than or equal to the
        # random amount of pheromone created above.
        for edge in edges:
            cumulative += edge.pheromone
            if choice <= cumulative:
                route_taken = edge
                break

        return route_taken

    def calculate_path_fitness(self, path):
        """Calculates the fitness of a specific path taken by an ant."""

        # List of 0's of length equal to the number of bins.
        bin_weights = [0] * self.b

        # Add the items to their respective bins.
        for edge in path:
            if edge.start.bin != None:
                bin_weights[edge.start.bin] += edge.start.item

        # Subtract the lowest weight of a bin from the laregest weight of bin.
        return max(bin_weights) - min(bin_weights)

    def update_pheromones(self, paths):
        """Updates the graph edge's pheromone based on the fitness of each path."""

        for path in paths:
            # Calculate the fitness of the path.
            fitness = self.calculate_path_fitness(path)
            for edge in path:
                # Prevents a divide by zero error for smaller BPPs when testing.
                try:
                    edge.pheromone += 100 / fitness
                except:
                    edge.pheromone += 100

    def evaporate_pheromone(self, evaporation_rate):
        """Partially evaporate the pheromone for every edge in the graph."""

        for node in self.nodes:
            for edge in node.edges:
                edge.evaporate_pheromone(evaporation_rate)

    def best_path(self, paths):
        """Calculates the best path and fitness for a trial."""

        # Set the first path as the best path intially.
        best_path = paths[0]
        best_fitness = self.calculate_path_fitness(paths[0])

        for path in paths[1:]:
            path_fitness = self.calculate_path_fitness(path)
            # Update the best path and fitness if the current fitness is better than the current
            # best fitness.
            if path_fitness < best_fitness:
                best_path = path
                best_fitness = path_fitness

        return best_path, best_fitness
