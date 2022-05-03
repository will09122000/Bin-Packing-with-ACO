import random

class Edge:
    """
    A class to represent an edge connecting one node to another.

    Attributes
    ----------
    start:       Node | The start node of the edge.
    destination: Node | The destination node of the edge.
    pheromone:  float | The pheromone level of the edge.
    """

    def __init__(self, start, destination):
        self.start = start
        self.destination = destination
        self.pheromone = None

    def randomise_pheromone(self):
        """Assign a random pheromone level from 0 to 1."""

        self.pheromone = random.random()
        #self.pheromone = 0.5

    def evaporate_pheromone(self, evaporation_rate):
        """Evaporate the pheromone by the evaporation rate (e)."""

        self.pheromone *= evaporation_rate
