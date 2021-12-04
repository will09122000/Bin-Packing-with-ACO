import numpy as np
import statistics
import csv
import os
import matplotlib.pyplot as plt
from random import random

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

    def create_directory(self):
        """Create experiment directory if it doesn't already exist."""

        parent_dir = f'Results/bpp_{self.bpp_id}'
        new_dir = f'experiment_{self.experiment_num}'
        path = os.path.join(parent_dir, new_dir)

        try:
            os.mkdir(path)
        except:
            pass

    def calc_result(self, p, e, time):
        """
        Calculates the best, average and standard deviation of the fitness from all trials in the
        experiment.
        """

        trial_fitnesses = [trial.best_fitness for trial in self.trials]
        best_fitness = min(trial_fitnesses)
        avg_fitness = sum(trial_fitnesses) / len(trial_fitnesses)
        try:
            stdev_fitness = statistics.stdev(trial_fitnesses)
        except:
            stdev_fitness = 0

        # Write values to a csv file.
        with open(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/results.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['trial_fitness', trial_fitnesses[0],
                                              trial_fitnesses[1],
                                              trial_fitnesses[2],
                                              trial_fitnesses[3],
                                              trial_fitnesses[4]])
            writer.writerow(['best_fitness', best_fitness])
            writer.writerow(['avg_fitness', avg_fitness])
            writer.writerow(['stdev_fitness', stdev_fitness])

        # Extra experiment data collection.
        if self.bpp_id == 3:
            with open('Results/bpp_3/results.csv','a', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([round(p, 2), round(e, 2), best_fitness, round(avg_fitness, 1), round(stdev_fitness, 1)])
            with open('Results/bpp_3/performance.csv','a', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([round(p, 2), round(e, 2), time.seconds])


    def plot_result(self):
        """
        Plots a graph for each trial showing how the average fitness of the ant's paths changed
        as the number of fitness evaluations increased.
        """

        fig, axs = plt.subplots(len(self.trials), sharex=True, sharey=True, figsize=(10, 15))
        fig.suptitle(f'Bin Packing Problem {self.bpp_id}\nExperiment {self.experiment_num}: p = {self.p}, e = {self.e}\nAvg. Fitness of Colony over Time', fontsize=24)
        plt.xlabel('Fitness Evaluations', fontsize=18)
        fig.text(0.06, 0.5, 'Average Fitness of Colony', ha='center', va='center', rotation='vertical', fontsize=18)

        # Create subplot for each trial.
        for trial in self.trials:
            axs[trial.trial_num].set_title(f'Trial {trial.trial_num+1}')
            x = [coord[0] for coord in trial.avg_fitness]
            y = [coord[1] for coord in trial.avg_fitness]
            axs[trial.trial_num].plot(x, y)

        # Save plot as an image file.
        plt.savefig(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/graph.png')
        plt.clf()

    def display_solution(self, b, num_items):
        """Displays a bar chart of bin weights to visualise the solution of each experiment."""

        # Lists of all trial fitnesses and respective paths for this experiment.
        trial_fitnesses = [trial.best_fitness for trial in self.trials]
        trial_paths = [trial.best_path for trial in self.trials]

        # The best path and fitness for this experiment.
        best_trial_index = trial_fitnesses.index(min(trial_fitnesses))
        best_fitness = trial_fitnesses[best_trial_index]
        best_path = trial_paths[best_trial_index]

        # 2D list for the stacked bar chart.
        bins = [np.array([0] * b) for _ in range(num_items)]
        bin_labels = list(range(1, b+1))

        # Add each item in the path to the correct bin.
        for i, edge in enumerate(best_path[0:-1]):
            bins[i][edge.destination.bin] = edge.destination.item

        # Plot each a bar for each bin.
        total = [0] * b
        for item in bins:
            plt.bar(bin_labels, item, bottom=total, color=(random(), random(), random()))
            total += item

        # Draw plot labels and save as an image file.
        plt.xlabel('Bin', fontsize=18)
        plt.ylabel('Total Weight of Items within Bin (kg)', fontsize=18)
        plt.title(f'Bin Packing Problem {self.bpp_id}\nExperiment {self.experiment_num}: p = {self.p}, e = {self.e}\nSolution with Fitness: {best_fitness}', fontsize=24)
        plt.savefig(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/solution.png')
        plt.clf()
