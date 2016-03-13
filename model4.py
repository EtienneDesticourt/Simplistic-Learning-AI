import numpy as np
from math import log

class World(object):
    "The World the being lives in. For now a collection of objects the being can access through his senses."
    def __init__(self):
        self.content = None
    def whatsOutThere(self):
        return self.content

def getSense(World, Being):
    @Being.learn
    @Being.instinct
    def sense(perception=None, recollectionLevel=0):
        if not perception:
            perception = World.whatsOutThere()
        print("I sense "+perception+".")
        return perception
    return sense

class Being(object):
    def __init__(self):
        self.fear = False
        self.running = False
        self.scary = ["Black ball"] #instinctive fear of Black ball
        self.memories = []
        self.concepts = []
        self.shortTermMemoryCapacity = 5 #Number of concepts stored in short term memory at a time
        self.associations = np.array([]) #Association is now an association weight (0.-1.) matrix
        self.startPotential = 10
        self.patternSensitivity = 0.01 #Tendency to link events, the higher it is, the higher the weight/occurence ratio
        self.activationSensitivity = 1 #Higher sensitivity, harder to activate (activation = weight * potential)
        #first pass 0.1 weights get activated, second pass 0.2, third 0.4, fourth 0.8, fifth None (rework?)
        #Lots of activations on first pass, filter needed (divide potential among concepts?, keep best n concepts?)
    #Senses
    def sense(self):
        pass
    #Learning
##    def strengthenAssociation(self, assoc):
##        s = self.associationSensitivity        
##        occurences =  s * assoc / (1 - assoc)
##        occurences += 1
##        return occurences / (occurences + s)
    def strengthenAssociation(self, w):
        "Increases association weight value."
        associations = self.calcAssociationNumber(w)
        return self.calcAssociationWeight(associations+1)
    def integrate(self, concept): #Might have to distinguish concepts and events at some point
        self.concepts.append(concept)
        if self.associations.shape == (0,):
            self.associations = np.array([[0]])
            return
        sizeX = len(self.concepts)-1
        conceptRow = np.zeros((1, sizeX))
        weightColumn = np.zeros((len(self.concepts), 1))
        self.associations = np.append(self.associations, conceptRow, 0)
        self.associations = np.append(self.associations, weightColumn, 1)
    def calcAssociationWeight(self, n):
        "Calculates association weights from the number (n) of time two concepts were associated."
        if n == 0 : return 0
        return self.patternSensitivity**(1/n)
    def calcAssociationNumber(self, w):
        "Calculates number of associations between two concepts based on their ass. weight."
        if w == 0: return 0
        return 1/log(w, self.patternSensitivity)
    def calcPotentialDegradation(self, recLevel):
        "Calculates new potential from recollection level."
        return self.startPotential*(0.5**recLevel) #10, 5, 2.5, 1.25, 0.625
    def learn(self, sense):
        def func(*args):
            sensed = sense(*args)
            print("I'm thinking about what I sensed.")
            perception, recollectionLevel = args
            potential = self.calcPotentialDegradation(recollectionLevel)

            #Learn new concepts
            if sensed not in self.concepts:
                self.integrate(sensed)
                
            #Associate preceeding concepts to current concept
            sensedIndex = self.concepts.index(sensed)
            for memory in self.memories[-self.shortTermMemoryCapacity:]:
                memoryIndex = self.concepts.index(memory)
                assocWeight = self.associations[memoryIndex, sensedIndex]
                assocWeight = self.strengthenAssociation(assocWeight)
                self.associations[memoryIndex, sensedIndex] = assocWeight #Should prolly account for mem distance (5 to 1) 
            self.memories.append(sensed)

            #We need an activation matrix in self to pass activation state
            #through funcs

            if sensed in self.concepts: #Concept representations now separated from association weights
                activationPotentials = self.associations[self.concepts.index(sensed)] * potential     #We select the row corresponding to the sensed concept associations to other concepts   
                activatedConcepts = activationPotentials >= self.activationSensitivity
                #For now we're gonna get the indexes and sense concept names: dirty but I don't want to rework senses just now
                for concept in [self.concepts[i] for i in range(len(activatedConcepts)) if activatedConcepts[i]]:
                    self.sense(concept, recollectionLevel+1)
            
            return sensed
        return func
    #Hardcoded behaviour rules
    def instinct(self, sense): #Instinct bypasses interpretatin, even if their association weight can be lowered
        def func(*args): #By making instinct a wrapper of sense we catch them all easily, maybe we should do same with learn
            sensed = sense(*args)
            print("My instincts are kicking in.")
            perception, recollectionLevel = args
                
            if sensed == "Black ball": #Instinctive fear of black ball
                self.sense("fear", recollectionLevel)
            else:                
                if sensed == "fear": #Instinctive reaction to fear
                    self.run()
                elif self.running:
                    self.stop()
            return sensed
                
        return func
    #Abilities
    def run(self):
        self.running = True
        print("I'm now running.")
    def stop(self):
        self.running = False
        print("I've stopped running.")



        
def runSimulation():
    #Simulation 5
    print("Running simulation 5. Basic learning model.")
    print("We're going to teach it to be afraid of the red ball.")
    World1 = World()
    Being1 = Being()
    Being1.sense = getSense(World1, Being1)
    print("A red ball has appeared.")
    World1.content = "Red ball"
    Being1.sense(None, 0)
    print("----")
    print("A black ball has appeared.")
    World1.content = "Black ball"
    Being1.sense(None, 0)
    print("----")
    print("We fill its memory to simulate some time passing so he doesn't associate the last event to the next one.")
    Being1.sense("Random memory 1",0)
    Being1.sense("Random memory 2",0)
    Being1.sense("Random memory 3",0)
    Being1.sense("Random memory 4",0)
    Being1.sense("Random memory 5",0)
    Being1.sense("Random memory 6",0)
    print("A red ball has appeared.")
    World1.content = "Red ball"
    Being1.sense(None, 0)
    print("----")
    print("A black ball has appeared.")
    World1.content = "Black ball"
    Being1.sense(None, 0)
    print("----")
    Being1.sense("Random memory 7",0)
    Being1.sense("Random memory 8",0)
    Being1.sense("Random memory 9",0)
    Being1.sense("Random memory 10",0)
    Being1.sense("Random memory 11",0)
    Being1.sense("Random memory 12",0)
    print("He should now know to be afraid of red for what might come after.")
    print("A red ball has appeared.")
    World1.content = "Red ball"
    Being1.sense(None, 0)
    print("-----------------\n\n")
    return Being1

#Being1 = runSimulation()
