class Graph:

    def __init__(self, bins, items):
        self.nodes = self.create_nodes(bins, items)
        self.create_edges(items)

    def create_nodes(self, bins, items):
        nodes = []

        # Start node.
        nodes.append(Node(-1, None))

        for item in range(0, items):
            for bin in range(0, bins):
                nodes.append(Node(item, bin))

        # End node.
        nodes.append(Node(None, None))

        return nodes

    def create_edges(self, items):

        # Start node.
        next_bin = 0
        for destination_node in self.nodes:
            if destination_node.bin == next_bin:
                edge = Edge(destination_node)
                self.nodes[0].edges.append(edge)

        for i, node in enumerate(self.nodes[1:-1]):
            #print(node.bin, node.item)
            if node.bin != items-1:
                next_bin = node.bin + 1
                for destination_node in self.nodes:
                    if destination_node.bin == next_bin:
                        edge = Edge(destination_node)
                        node.edges.append(edge)
            else:
                edge = Edge(self.nodes[-1])
                node.edges.append(edge)

class Node:

    def __init__(self, bin, item):
        self.bin = bin
        self.item = item
        self.edges = []

class Edge:
    def __init__(self, destination, pheromone=None):
        self.destination = destination
        self.pheromone = 0.1 if pheromone is None else pheromone

graph = Graph(3, 5)

for i, node in enumerate(graph.nodes):
    print(i, node.bin, node.item)
    if len(node.edges) > 0:
        print('Edges:')
        for edge in node.edges:
            print(edge.destination.bin, edge.destination.item)
