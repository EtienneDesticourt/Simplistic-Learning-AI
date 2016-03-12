
class World(object):
    "A collection of objects the being can access through his senses."
    def __init__(self):
        self.content = None
    def whatsOutThere(self):
        return self.content

def getSense(World):
    def sense():
        perception = World.whatsOutThere()
        print("I sensed a "+perception+".")
        return perception
    return sense

class Being(object):
    def __init__(self):
        self.inDanger = False
        self.running = False
    #Senses
    def sense(self):
        pass
    #Learning
    def interpret(self, sensed):
        print("I'm thinking about what I sensed.")
        if sensed == "Black ball":
            self.inDanger = True
        elif sensed == "White ball":
            self.inDanger = False
    #Hardcoded behaviour rules
    def instinct(self):
        if self.inDanger:
            print("I'm in danger!")
            self.run()
        elif self.running:
            print("I'm not in danger.")
            self.stop()
    #Abilities
    def run(self):
        self.running = True
        print("I'm now running.")
    def stop(self):
        self.running = False
        print("I've stopped running.")

def runSimulation():
    #Simulation 1
    print("Running simulation 1. The model cannot interpret his senses.")
    World1 = World()
    Being1 = Being()
    Being1.sense = getSense(World1)
    print("A black ball has appeared.")
    World1.content = "Black ball"
    Being1.sense()
    Being1.instinct()
    print("A white ball has appeared.")
    World1.content = "White ball"
    Being1.sense()
    Being1.instinct()
    print("-----------------\n\n")
    
    #Simulation 2
    print("Running simulation 2. The model can infer meaning from what his senses perceive.")
    World1 = World()
    Being1 = Being()
    Being1.sense = getSense(World1)
    print("A black ball has appeared.")
    World1.content = "Black ball"
    Being1.interpret(Being1.sense())
    Being1.instinct()
    print("A white ball has appeared.")
    World1.content = "White ball"
    Being1.interpret(Being1.sense())
    Being1.instinct()
    print("-----------------\n\n")

runSimulation()
