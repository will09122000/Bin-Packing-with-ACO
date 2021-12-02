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
            num_trials = 1,
            items      = [1, 2, 3, 4, 5],
            b          = 3,
            p          = 10,
            e          = 0.9,
            fe         = 1000)

bpps = [bpp_1, bpp_2]

# Run each experiment for each bin packing problem.
if __name__ == '__main__':
    for bpp in bpps:
        print(f'Bin Packing Problem {bpp.bpp_id}')
        experiment_num = 1
        for p in bpp.p:
            for e in bpp.e:
                bpp.results.append(bpp.run_experiment(experiment_num, p, e))
                experiment_num += 1

    #bpp3.run_experiment(bpp3.p, bpp3.e)
    #bpp1.run_experiment(bpp1.p[1], bpp1.e[0])
    #bpp_2.run_experiment(bpp_2.p[1], bpp_2.e[0])
