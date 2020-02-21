import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import numpy as np

class Simulation (object):

    # Initialize instance variables and the initial parameters of the simulation
    def __init__(self, bodies, quadrantSize, iterations, timeStep):
        self.bodies  = bodies                              # Stores all the body objects in the simulation.
        self.patches = [body.patch() for body in bodies]   # Stores the patches of the bodies in the simulation. 
        self.quadrantSize = quadrantSize                   # Defines window size. 
        self.G = 6.67 * 10 ** -11                          # Gravitational constant
        self.timeStep = timeStep                           # Time step between frames in simulation.
        self.iterations = iterations                       # Number of frames calculated.
        self.calculateBodyAccelerations()                  # Initializes the acceleration of the bodies.
        self.calculateInitialVelocities()                  # Initializes the velocity of the bodies. 
    
    # Create plot and run animation
    def runSim (self):
        fig = plt.figure()
        ax  = plt.axes()
        ax.axis('scaled')
        ax.set_xlim(-self.quadrantSize, self.quadrantSize)
        ax.set_ylim(-self.quadrantSize, self.quadrantSize)
        ax.set_facecolor('0')
        fig.patch.set_facecolor('0')
        for patch in self.patches:
            ax.add_patch(patch)
        anim = FuncAnimation (fig, self.animate, init_func = self.init, frames = self.iterations, repeat = False, interval = 1, blit = True)
        plt.show()

    # Init function of the animation
    def init (self):
        return self.patches

    # Generates each frame of the animation.
    # Calls the function which updates the bodies in the simulation.
    # Every 51 frames the total kinetic energy of the bodies in the simulation is displayed.
    def animate (self, i):
        self.calculateNextPositions()
        for j in range (0, len(self.bodies)):
            body = self.bodies[j]
            xPos = body.position[0]
            yPos = body.position[1]
            self.patches[j].center = (xPos, yPos)

        if (i % 51 == 0):
            print("Total Kinetic Energy = {} Kj".format(round(self.totalKineticEnergy() / 1000, 3)))
            #print("Position of Mars = ({},{})".format(self.bodies[0].position[0], self.bodies[0].position[1]))
        return self.patches

    # Calculates and updates the position of the bodies after a full time step.
    def calculateNextPositions (self):
        for body in self.bodies:
            body.velocity = body.velocity + body.acceleration * self.timeStep
            body.position = body.position + body.velocity * self.timeStep
        self.calculateBodyAccelerations()

    # Calculates and defines the initial velocity of each body except for Mars.
    # Mars is assumed to have an initial velocity of zero.
    # The influence of other bodies (except for Mars) is ignored.
    def calculateInitialVelocities (self):
        mars = self.bodies[0]
        for body in self.bodies:
            if body.name == "Mars":
                body.velocity = 0
            else:
                vectR = body.position - mars.position
                magR  = self.magnitude(vectR)
                magV  = ((self.G * mars.mass) / magR) ** (1/2)
                normR = self.unitVector(self.normalVector(vectR))
                vectV = magV * normR
                body.velocity = vectV


    # Calculates the acceleration of each body due to the other bodies:
    def calculateBodyAccelerations (self):
        for body in self.bodies:
            acceleration = [] # Stores the acceleration due to the other bodies.
            for otherBody in self.bodies:
                if (otherBody.name != body.name):
                    vectR = otherBody.position - body.position        # Vector from current body to other body
                    magR  = self.magnitude(vectR)                     # Magnitude of this vector
                    unitR = self.unitVector(vectR)                    # Unit vector in this direction
                    magA  = ((self.G * otherBody.mass) / (magR ** 2)) # Magnitude of the acceleration due to the other body
                    vectA = magA * unitR
                    acceleration += [vectA]
            netAcceleration = sum(acceleration)                       # The net acceleration is calculated
            body.acceleration = netAcceleration

    # Calculates a unit vector in the direction of the given vector.
    def unitVector (self, vector):
        mag           = self.magnitude(vector)
        unitVector    = np.array([vector[0] / mag, vector[1] / mag])
        return unitVector

    # Calculates a vector that is perpendicular to the given vector.
    def normalVector(self, vector):
        i = vector[0]
        j = vector[1]
        normal = np.array([-j, i])
        return normal

    # Calculates the magnitude of a given vector. 
    def magnitude (self, vector):
        return ((vector[0] ** 2 + vector[1] ** 2) ** (1/2))

    # Calculates the sum of the kinetic energies of all bodies in the simulation. 
    def totalKineticEnergy(self):
        kineticEnergies = [ 0.5 * body.mass * (self.magnitude(body.velocity) ** 2) for body in self.bodies]
        totalKineticEnergy = sum(kineticEnergies)
        return totalKineticEnergy