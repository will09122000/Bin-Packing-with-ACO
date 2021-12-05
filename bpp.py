from datetime import timedelta, datetime
import tracemalloc

from graph import Graph
from result import Trial, Experiment

class Bpp:
    """
    A class to run a single bin packing problem for which multiple experiments are run from.

    Attributes
    ----------
    bpp_id:      int | The identifier for the bin packing problem, either 1 or 2.
    num_trials:  int | The number of trials for this experiment, 5 trials used for all experiments
                       in this CA.
    items: list[int] | A list of items that are to be packed into bins, the number represents the
                       weight of the item.
    b:           int | The number of bins the above items can be packed into.
    p:     list[int] | A list of the number of ants used throughout the experiments.
    e:   list[float] | A list of the pheromone evaporation rate used throughout the experiments.
    fe:          int | The number of fitness evaluations that must be taken before the ACO can
                       terminate.
    """

    def __init__(self, bpp_id, num_trials, items, b, p, e, fe):
        self.bpp_id = bpp_id
        self.num_trials = num_trials
        self.items = items
        self.b = b
        self.p = p
        self.e = e
        self.fe = fe
        self.results = []

    def run_experiment(self, experiment_num, p, e):
        """Runs a single experiment within a bin packing problem."""
        tracemalloc.start()
        print(f'Experiment {experiment_num}: p = {p}, e = {e}')

        # Create the graph object for ants to navigate.
        self.graph = Graph(self.b, self.items)
        # Create the experiment object used for data collection.
        experiment = Experiment(self.bpp_id, experiment_num, p, e)

        trials = []
        times = []
        start = datetime.now()

        # Repeat for the number of trials in the experiment.
        for i in range(0, self.num_trials):
            trials.append(Trial(self.bpp_id, experiment_num, i))
            self.run_trial(p, e, trials, i, times)

        # Add trials to experiment object for data collection.
        experiment.trials.extend(trials)

        # Calculate time taken and memory used.
        average_timedelta = sum(times, timedelta()) / len(times)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f'Average path gen time: {average_timedelta}')
        print(f'Total time: {datetime.now() - start}')
        print(f'Current memory: {current / 10**6}MB, Peak memory: {peak / 10**6}MB')
        print()

        # Calculate results and plot data.
        # Commented out to keep the results in the directory consistent with the results in the report.
        #experiment.create_directory()
        #experiment.calc_result(p, e, datetime.now() - start, current / 10**6, peak / 10**6)
        #experiment.plot_result()
        #experiment.display_solution(self.b, len(self.items))

        return experiment

    def run_trial(self, p, e, trials, i, times):
        """Runs a single ACO trial for an experiment within a specific bin packing problem."""

        # Add the initial random pheromone to each edge in the graph.
        self.graph.add_pheromone()

        current_evaluations = 0
        # Repeat until the number of fitness evaluations (10,000) has been reached.
        while current_evaluations < self.fe:

            # Generate a path for each ant in the colony.
            paths, time = self.graph.generate_paths(p, self.b)
            times.append(time)

            # Update the pheromone for each edge on the graph determined by the fitness of each
            # ant's path.
            self.graph.update_pheromones(paths)

            # Partially evaporate the pheromone for every edge in the graph.
            self.graph.evaporate_pheromone(e)

            # Increment the number of fitness evaluations by the number of ants in the colony.
            current_evaluations += p

            # Collect data for the average path's fitness for this current evaluation.
            fitnesses = [self.graph.calculate_path_fitness(path) for path in paths]
            trials[i].avg_fitness.append([current_evaluations, sum(fitnesses) / len(fitnesses)])

        # Calculate the best path and fitness for this trial.
        trials[i].best_path, trials[i].best_fitness = self.graph.best_path(paths)

        print(f'Trial {i+1},  Fitness: {trials[i].best_fitness}')
