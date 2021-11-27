import numpy as np
import statistics
import csv
import matplotlib.pyplot as plt

class Trial:
    def __init__(self, bpp_id, experiment_num, trial_num):
        self.bpp_id = bpp_id
        self.experiment_num = experiment_num
        self.trial_num = trial_num
        self.best_path = None
        self.best_fitness = None
        self.avg_fitness = []
        self.time = None

    def plot(self):
        x_coords = [coord[0] for coord in self.avg_fitness]
        y_coords = [coord[1] for coord in self.avg_fitness]
        plt.plot(x_coords, y_coords)
        plt.savefig(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/trial_{self.bpp_id}.png')

class Experiment:
    def __init__(self, bpp_id, experiment_num, p, e):
        self.bpp_id = bpp_id
        self.experiment_num = experiment_num
        self.trials = []
        self.p = p
        self.e = e

    def calc_result(self):
        trial_fitnesses = [trial.best_fitness for trial in self.trials]
        best_fitness = min(trial_fitnesses)
        avg_fitness = sum(trial_fitnesses) / len(trial_fitnesses)
        stdev_fitness = statistics.stdev(trial_fitnesses)

        with open(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/results.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['best_fitness', best_fitness])
            writer.writerow(['avg_fitness', avg_fitness])
            writer.writerow(['stdev_fitness', stdev_fitness])

    def plot_result(self):
        fig, axs = plt.subplots(len(self.trials), sharex=True, sharey=True, figsize=(10, 15))
        fig.suptitle(f'Bin Packing Problem {self.bpp_id}, Experiment {self.experiment_num}\np = {self.p}, e = {self.e}', fontsize=24)
        plt.xlabel('Fitness Evaluations', fontsize=18)
        fig.text(0.06, 0.5, 'Average Fitness of Colony', ha='center', va='center', rotation='vertical', fontsize=18)
        for trial in self.trials:
            axs[trial.trial_num].set_title(f'Trial {trial.trial_num+1}')
            x_coords = [coord[0] for coord in trial.avg_fitness]
            y_coords = [coord[1] for coord in trial.avg_fitness]
            axs[trial.trial_num].plot(x_coords, y_coords)

        plt.savefig(f'Results/bpp_{self.bpp_id}/experiment_{self.experiment_num}/graph.png')
