import numpy as np
import statistics
import csv
import matplotlib.pyplot as plt

class Trial:
    """
    A class to represent the data collected from a single ACO trial.

    Attributes
    ----------
    bpp_id:            int | The identifier for the bin packing problem, either 1 or 2.
    experiment_num:    int | The number of the current experiment, either 1, 2, 3 or 4.
    trial_num:         int | The number of the current trial, either 1, 2, 3, 4 or 5.
    best_path:  list[Edge] | A list of edges that represents the path with the lowest fitness.
    best_fitness:      int | The lowest fitness of the best path in the trial.
    avg_fitness: list[int] | A list of the average fitness of each ant's path after each iteration.
    """

    def __init__(self, bpp_id, experiment_num, trial_num):
        self.bpp_id = bpp_id
        self.experiment_num = experiment_num
        self.trial_num = trial_num
        self.best_path = None
        self.best_fitness = None
        self.avg_fitness = []

class Experiment:
    """
    A class to represent the data collected from a single experiment in one of the bin packing
    problems.

    Attributes
    ----------
    bpp_id:         int | The identifier for the bin packing problem, either 1 or 2.
    experiment_num: int | The number of the current experiment, either 1, 2, 3 or 4.
    trials: list[Trial] | A list of the data collected from each trial in the experiment.
    p:              int | The number of ants used in this experiment.
    e:            float | The pheromone evaporation rate used in this experiment.
    """

    def __init__(self, bpp_id, experiment_num, p, e):
        self.bpp_id = bpp_id
        self.experiment_num = experiment_num
        self.trials = []
        self.p = p
        self.e = e

    def calc_result(self):
        """
        Calculates the best, average and standard deviation of the fitness from all trials in the
        experiment.
        """

        trial_fitnesses = [trial.best_fitness for trial in self.trials]
        best_fitness = min(trial_fitnesses)
        avg_fitness = sum(trial_fitnesses) / len(trial_fitnesses)
        stdev_fitness = statistics.stdev(trial_fitnesses)

        # Write values to a csv file.
        with open(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/results.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['best_fitness', best_fitness])
            writer.writerow(['avg_fitness', avg_fitness])
            writer.writerow(['stdev_fitness', stdev_fitness])

    def plot_result(self):
        """
        Plots a graph for each trial showing how the average fitness of the ant's paths changed
        as the number of fitness evaluations increased.
        """

        fig, axs = plt.subplots(len(self.trials), sharex=True, sharey=True, figsize=(10, 15))
        fig.suptitle(f'Bin Packing Problem {self.bpp_id}, Experiment {self.experiment_num}\np = {self.p}, e = {self.e}', fontsize=24)
        plt.xlabel('Fitness Evaluations', fontsize=18)
        fig.text(0.06, 0.5, 'Average Fitness of Colony', ha='center', va='center', rotation='vertical', fontsize=18)

        # Create subplot for each trial.
        for trial in self.trials:
            axs[trial.trial_num].set_title(f'Trial {trial.trial_num+1}')
            x = [coord[0] for coord in trial.avg_fitness]
            y = [coord[1] for coord in trial.avg_fitness]
            axs[trial.trial_num].plot(x, y)

        plt.savefig(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/graph.png')
