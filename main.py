from Bpp import Bpp

bpp_1 = Bpp(bpp_id = 1,
            trials = 5,
            items  = list(range(1, 501)),
            b      = 10,
            p      = [100, 10],
            e      = [0.9, 0.5],
            fe     = 10000)

bpp_2 = Bpp(bpp_id = 2,
            trials = 5,
            items  = [item ** 2 for item in list(range(1, 501))],
            b      = 50,
            p      = [100, 10],
            e      = [0.9, 0.5],
            fe     = 10000)

bpp_3 = Bpp(bpp_id = 3,
            trials = 1,
            items  = [1, 2, 3, 4, 5],
            b      = 3,
            p      = 10,
            e      = 0.9,
            fe     = 1000)

bpps = [bpp_1, bpp_2]

for bpp in bpps:
    print(f'Bin Packing Problem {bpp.bpp_id}')
    experiment_num = 1
    for p in bpp.p:
        for e in bpp.e:
            bpp.results = bpp.run_experiment(experiment_num, p, e)
            experiment_num += 1

#bpp3.run_experiment(bpp3.p, bpp3.e)
#bpp1.run_experiment(bpp1.p[1], bpp1.e[0])
#bpp_2.run_experiment(bpp_2.p[1], bpp_2.e[0])

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