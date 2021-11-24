from graph import Graph

bins = 3
items = [1, 2, 3, 4, 5]
p = 100
e = 0.90

graph = Graph(bins, items)

graph.add_pheromone()

fitness_evaluations = 0

while fitness_evaluations < 10000:

    paths = graph.generate_paths(p, bins)

    graph.update_pheromones(paths)

    graph.evaporate_pheromone(e)

    fitness_evaluations += p


for path in paths:
    #for edge in path:
        #print('Start: bin: ' + str(edge.start.bin) + ', item: ' + str(edge.start.item) + 'kg')
        #print('Destination: bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg')

    print('Fitness: ' + str(graph.calculate_path_fitness(path)))

#for node in graph.nodes:
    #print('bin: ' + str(node.bin) + ', item: ' + str(node.item) + 'kg')
    #if len(node.edges) > 0:
        #print('Edges:')
        #for edge in node.edges:
            #print('bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg, pheromone: ' + str(edge.pheromone))
    #print()