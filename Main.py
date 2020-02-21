from Body import Body
from Simulation import Simulation
from FileReader import FileReader

def main ():
    # File reader object is created
    readFile = FileReader("simData.txt")

    # If no error occured while reading from file, the simulation is initiated.
    if (readFile.status == "OK"):
        readFile.createCelestialBodies()
        mySim  = Simulation(readFile.bodies,readFile.quadrantSize, readFile.iterations, readFile.timeStep)
        mySim.runSim()
    else:
        print ("ERROR: File could not be found or read.")

if __name__ == "__main__":
    main()