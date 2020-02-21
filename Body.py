import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Body (object):
    # Initiate instance variables
    def __init__(self, name, mass, initialPosition, radius, color):
        self.mass         = mass
        self.position     = np.array([initialPosition[0], initialPosition[1]])
        self.radius       = radius 
        self.color        = color
        self.acceleration = np.array([0,0])     # Placeholder until calculated
        self.velocity     = np.array([0,0])     # Placeholder until calculated
        self.name         = name

    # Creates the patch that will be displayed in the simulation to represent the body.
    def patch (self):
        patch = patches.Circle((self.position[0], self.position[1]), self.radius, color = self.color, animated = True)
        return patch