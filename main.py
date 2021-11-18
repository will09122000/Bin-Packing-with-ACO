from graph import Graph
import random

bins = 3
items = [1, 2, 3, 4, 5]

graph = Graph(bins, items)

graph.add_pheromone()

graph.generate_paths(p=5, num_bins=bins)



#for node in graph.nodes:
    #print('bin: ' + str(node.bin) + ', item: ' + str(node.item) + 'kg')
    #if len(node.edges) > 0:
        #print('Edges:')
        #for edge in node.edges:
            #print('bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg, pheromone: ' + str(edge.pheromone))
    #print()