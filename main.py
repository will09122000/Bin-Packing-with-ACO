from numpy import arange
from bpp import Bpp

# Bin packing problem 1.
bpp_1 = Bpp(bpp_id     = 1,
            num_trials = 5,
            items      = list(range(1, 501)),
            b          = 10,
            p          = [100, 10],
            e          = [0.9, 0.5],
            fe         = 10000)

# Bin packing problem 2.
bpp_2 = Bpp(bpp_id     = 2,
            num_trials = 5,
            items      = [item ** 2 for item in list(range(1, 501))],
            b          = 50,
            p          = [100, 10],
            e          = [0.9, 0.5],
            fe         = 10000)

bpp_3 = Bpp(bpp_id     = 3,
            num_trials = 10,
            items      = list(range(1, 251)),
            b          = 5,
            p          = [1, 2, 3, 4] + list(range(5, 115, 5)),
            e          = list(arange(0.05, 1.05, 0.05)),
            fe         = 10000)

bpps = [bpp_1, bpp_2]

# Run each experiment for each bin packing problem.
if __name__ == '__main__':
    """
    for bpp in bpps:
        print(f'Bin Packing Problem {bpp.bpp_id}')
        experiment_num = 1
        for p in bpp.p:
            for e in bpp.e:
                bpp.results.append(bpp.run_experiment(experiment_num, p, e))
                experiment_num += 1
    """

    experiment_num = 1
    for p in bpp_3.p:
        for e in bpp_3.e:
            bpp_3.results.append(bpp_3.run_experiment(experiment_num, p, e))
            experiment_num += 1
