import random
from numpy.random import choice
import numpy as np

"""
p: num_ants (100 or 10), index usually denoted by n
e: pheromone_evaporation_rate (0.9 or 0.6)
b: num_bins (10 or 50), depends or BPP1 or BPP2, index usually denoted by j
k: num_items (500), index usually denoted by i
w_b: list_weight_in_bins
w_i: #list_item_weight (=item no. i or =(i^2)/2)
bpp: BPP1 or BPP2 (1 or 2)
Pij: corresponding probabilities to each entry in T
T: Pheromone matrix
SE: set of ant paths from S to E (item in list ranges from 1 to 10, representing the bins)
"""

def GenerateSE(T, k, b, p):
    SE = [[] for n in range(p)]

    denom=np.sum(T, axis = 1) # denominator
    Pij=[T[i]/denom[i] for i in range(k)] # probabilities
    for n in range(p):
        for i in range(k):
            """
            choice = random.uniform(0, sum(T[i]))
            cumulative = 0
            for j in range(b):
                cumulative += T[i][j]
                if choice <= cumulative:
                    SE[n].append(j)
            """

            SE[n].append(choice([j for j in range(b)], p=Pij[i])+1) # using choice to add selected bin acc. to prob.
    return SE

def Fitness(SE, k, b, p, w_i):
    d = [0 for n in range(p)] # difference d between the heaviest and lightest bins
    for n in range(p):
        w_b=[0 for j in range(b)]
        for i in range(k):

            # OLD (MISTAKE)
            # The value of 'w_i[SE[n][i]-1]' is the index of the bin, not the weight of the item.
            #w_b[SE[n][i]-1] = w_b[SE[n][i]-1] + w_i[SE[n][i]-1]

            # NEW
            w_b[SE[n][i]-1] += i+1

        d[n] = max(w_b) - min(w_b)

    return d

def GenerateResults(d, SE):
    results = [min(d), SE[d.index(min(d))], max(d), SE[d.index(max(d))], sum(d) / len(d)]
    return results

def PrintResults(d, SE):
    results = GenerateResults(d, SE)
    print("Fitness:    Best: ", results[0], "  Worst: ", results[2], "  Average: ", results[4])
    #print(d)
    #print("Best path: ", results[1])
    #print("    Worst path: ", results[3])
    return None

def ACO_BPP(p, e, bpp):

    # Initialization
    
    if (bpp == 1):
        b = 10
        k = 500
        w_i = [i + 1 for i in range(k)]
    elif (bpp == 2):
        b = 50
        k = 500
        w_i=[((i + 1) * (i +1 )) / 2 for i in range(k)]
    elif (bpp == 3):
        b = 5
        k = 25
        w_i = [i + 1 for i in range(k)]


    # 1. Randomly distribute small amounts of pheromone (between 0 and 1) on the construction graph.
    T=[[random.random() for j in range(b)] for i in range(k)]

    current_evaluations = 0
    # 5. Until termination, repeat
    while current_evaluations < 10000:

        # 2. Generate a set of p ant paths from S to E
        SE = GenerateSE(T, k, b, p)

        #3. Update the pheromone in pheromone table.
        d = Fitness(SE, k, b, p, w_i)





        # NEW

        # Iterate through each ant's path.
        for i, path in enumerate(SE):
            # Find pheromone increment value from the path's fitness 
            delta = 100 / d[i]
            # Iterate through each item placement in the ant's path.
            for bin_id in path:
                # Update value in pheromone table.
                T[i][bin_id-1] += delta

        # OLD

        #delta = 100/min(d) #100/fitness
        #for i in range(k):
            #T[i][SE[d.index(min(d))][i]-1] += delta #modified to only update the path with best fitness





        # 4. Evaporate the pheromone for all links in the graph
        T = [[e * T[i][j] for j in range(b)] for i in range(k)] # evaporation: e * T (pheromone matrix)

        # Printing results, best & worst fitness of first & last generation
        #if (itr == 0):
            #print("First generation: ")
            #PrintResults(d, SE)
        current_evaluations += p

        PrintResults(d, SE)


ACO_BPP(10, 0.9, 3)
