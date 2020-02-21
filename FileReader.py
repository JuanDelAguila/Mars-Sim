from Body import Body
class FileReader (object):
    # Try to open the given file and extract the simulation data.
    # If this fails, the calling code receives an error message.
    def __init__(self, fileName):
        try:
            self.text = open(fileName, "r").read()
            self.status = "OK"
            self.bodyParameters = []
            self.splitByLines()
            self.extractGeneralParameters()
            self.extractBodyParameters()
        except:
            self.status = "ERROR"
        
    # Creates the body objects based on the data extracted from file.
    def createCelestialBodies(self):
        try:
            self.bodies = []
            for body in self.bodyParameters:
                name             = str(body[0].split(":")[1])
                color            = tuple([float(color) for color in body[1].split(":")[1].split(",")])
                mass             = self.fromSciNot(body[2].split(":")[1]) 
                bodyRadius       = self.fromSciNot(body[3].split(":")[1])
                radiusBias       = self.fromSciNot(body[4].split(":")[1])
                adjBodyRadius    = bodyRadius + radiusBias
                orbitRadius      = self.fromSciNot(body[5].split(":")[1])
                initialPosition  = [orbitRadius,0]
                newCelestialBody = Body(name, mass, initialPosition, adjBodyRadius, color)
                self.bodies     += [newCelestialBody]
        except (ValueError, IndexError):
            print("ERROR: Ill-formatted file")
            self.status = "ERROR"

    # Takes a number strin in scientific notation and returns a float
    def fromSciNot(self, n):
        try:
            terms = n.split("e")
            coefficient = float(terms[0])
            exponent = float(terms[1])
            return coefficient * 10 ** exponent
        except (IndexError):
            return float(n)
        except(ValueError):
            print ("ERROR: Ill-formatted file")
            self.status = "ERROR"

    # Splits the text in the file by lines and removes spaces
    def splitByLines(self):
        self.text = list(filter(lambda x: x != '', self.text.split("\n"))) # Divides the input string by lines.
        self.text = [line.replace (" ", "") for line in self.text] # Removes spaces from each line.

    # Extract general simulation parameters from file.
    def extractGeneralParameters (self):
        try:
            generalParameters = self.text[1:4]
            self.iterations   = int(generalParameters[0].split(":")[1])
            self.timeStep     = int(generalParameters[1].split(":")[1])
            self.quadrantSize = self.fromSciNot(generalParameters[2].split(":")[1])
        except (ValueError, IndexError):
            print ("ERROR: Ill-formatted file")
            self.status = "ERROR"    

    # Extract body parameters from file.
    def extractBodyParameters (self):
        self.text = self.dropWhile(self.text, lambda x: x != 'Celestialbodies:')[1:] # Removes all the initial general parameters
        while (len(self.text) != 0):
            self.bodyParameters += [self.text[:6]]
            self.text = self.text[6:]

    # Helper function: takes items from a list as long as those items satisfy a given predicate.
    def takeWhile (self, xs, f):
        product = []
        for x in xs:
            if (f(x)):
                product += [x]
            else:
                return product
        return product

    # Helper function: removes items from a list as long as those items satisfy a given predicate.
    def dropWhile (self, xs, f):
        for i in range (0, len(xs)):
            if (f(xs[i])):
                pass
            else:
                return xs[i:]
        
