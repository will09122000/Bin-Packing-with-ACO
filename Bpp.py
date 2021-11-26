from datetime import timedelta, datetime

from graph import Graph
from result import Trial

class Bpp:
    def __init__(self, trials, items, b, p, e, fe):
        self.trials = trials
        self.items = items
        self.b = b
        self.p = p
        self.e = e
        self.fe = fe

    def run_experiment(self, p, e):
        print(f'Experiment: p = {p}, e = {e}')

        self.graph = Graph(self.b, self.items)
        #self.result = Result()
        times = []
        start = datetime.now()
        for i in range(0, self.trials):
            self.graph.add_pheromone()

            trial = Trial(i)
            current_evaluations = 0
            while current_evaluations < self.fe:

                paths, time = self.graph.generate_paths(p, self.b)
                times.append(time)
                self.graph.update_pheromones(paths)

                self.graph.evaporate_pheromone(e)

                current_evaluations += p

                fitnesses = [self.graph.calculate_path_fitness(path) for path in paths]
                trial.avg_fitness.append([current_evaluations, sum(fitnesses) / len(fitnesses)])

            trial.best_path, trial.best_fitness = self.graph.best_path(paths)

            print(f'Trial {i+1}, Fitness: {trial.best_fitness}')

        trial.plot()
        average_timedelta = sum(times, timedelta()) / len(times)
        print(f'Average path gen time: {average_timedelta}')
        print(f'Total time: {datetime.now() - start}')
        print()
