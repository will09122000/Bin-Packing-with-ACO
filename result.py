import numpy as np
import matplotlib.pyplot as plt

class Trial:
    def __init__(self, number):
        self.id = number
        self.best_path = None
        self.best_fitness = None
        self.avg_fitness = []
        self.time = None

    def plot(self):
        x_coords = [coord[0] for coord in self.avg_fitness]
        y_coords = [coord[1] for coord in self.avg_fitness]
        plt.plot(x_coords, y_coords)
        plt.savefig(f'trial_{self.id}.png')

"""
class Result:
    def __init__(self):
        self.best_path = None
        self.best_fitness = None
        self.all_fitness = []
        self.time = None

    #def display_result(self):

"""