from Bpp import Bpp

bpp1 = Bpp(trials = 1,
           items  = list(range(1, 501)),
           b      = 10,
           p      = [100, 10],
           e      = [0.9, 0.5],
           fe     = 10000)

bpp2 = Bpp(trials = 5,
           items  = [item ** 2 for item in list(range(1, 501))],
           b      = 50,
           p      = [100, 10],
           e      = [0.9, 0.5],
           fe     = 10000)

bpp3 = Bpp(trials = 1,
           items  = [1, 2, 3, 4, 5],
           b      = 3,
           p      = 10,
           e      = 0.9,
           fe     = 1000)
"""
print('BPP 1')
for p in bpp1.p:
    for e in bpp1.e:
        bpp1.run_experiment(p, e)
print()
print('BPP 2')
for p in bpp2.p:
    for e in bpp2.e:
        bpp2.run_experiment(p, e)
"""
#bpp3.run_experiment(bpp3.p, bpp3.e)
bpp1.run_experiment(bpp1.p[1], bpp1.e[0])

#for edge in best_path:
    #print('Start: bin: ' + str(edge.start.bin) + ', item: ' + str(edge.start.item) + 'kg')
    #print('Destination: bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg')


#for path in paths:
    #for edge in path:
        #print('Start: bin: ' + str(edge.start.bin) + ', item: ' + str(edge.start.item) + 'kg')
        #print('Destination: bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg')

    #print('Fitness: ' + str(bpp1.graph.calculate_path_fitness(path)))

#for node in graph.nodes:
    #print('bin: ' + str(node.bin) + ', item: ' + str(node.item) + 'kg')
    #if len(node.edges) > 0:
        #print('Edges:')
        #for edge in node.edges:
            #print('bin: ' + str(edge.destination.bin) + ', item: ' + str(edge.destination.item) + 'kg, pheromone: ' + str(edge.pheromone))
    #print()