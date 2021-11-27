from datetime import timedelta, datetime

from graph import Graph
from result import Trial, Experiment

class Bpp:
    def __init__(self, bpp_id, trials, items, b, p, e, fe):
        self.bpp_id = bpp_id
        self.trials = trials
        self.items = items
        self.b = b
        self.p = p
        self.e = e
        self.fe = fe
        self.results = None

    def run_experiment(self, experiment_num, p, e):
        print(f'Experiment {experiment_num}: p = {p}, e = {e}')

        self.graph = Graph(self.b, self.items)
        trials = []
        experiment = Experiment(self.bpp_id, experiment_num, p, e)
        times = []
        start = datetime.now()

        for i in range(0, self.trials):
            self.graph.add_pheromone()

            trials.append(Trial(self.bpp_id, experiment_num, i))
            current_evaluations = 0
            while current_evaluations < self.fe:

                paths, time = self.graph.generate_paths(p, self.b)
                times.append(time)
                self.graph.update_pheromones(paths)

                self.graph.evaporate_pheromone(e)

                current_evaluations += p

                # Data collection
                fitnesses = [self.graph.calculate_path_fitness(path) for path in paths]
                trials[i].avg_fitness.append([current_evaluations, sum(fitnesses) / len(fitnesses)])

            trials[i].best_path, trials[i].best_fitness = self.graph.best_path(paths)

            print(f'Trial {i+1}, Fitness: {trials[i].best_fitness}')

        for trial in trials:
            #trial.plot()
            experiment.trials.append(trial)

        average_timedelta = sum(times, timedelta()) / len(times)
        print(f'Average path gen time: {average_timedelta}')
        print(f'Total time: {datetime.now() - start}')
        print()

        experiment.calc_result()
        experiment.plot_result()
        return experiment
