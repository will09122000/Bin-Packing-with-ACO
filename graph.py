class Graph:

    def __init__(self, bins, items):
        self.nodes = self.create_nodes(bins, items)
        self.create_edges(bins, items)

    def create_nodes(self, bins, items):
        nodes = []

        # Start node.
        nodes.append(Node(-1, None))

        for item in range(0, items):
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
        for i, node in enumerate(self.nodes[1:-1]):
            if node.item != items-1:
                next_item = node.item + 1
                #for destination_node in self.nodes[i+1:i+bins+1]:
                for destination_node in self.nodes:
                    if destination_node.item == next_item:
                        edge = Edge(destination_node)
                        node.edges.append(edge)
            # Bins for the last item all point to the end node.
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
    print(" ")
