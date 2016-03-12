
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
        self.associations = {}
    #Senses
    def sense(self):
        pass
    #Learning
    def learn(self, sense):
        def func(*args):
            sensed = sense(*args)
            print("I'm thinking about what I sensed.")
            perception, recollectionLevel = args
            
            #Learn pattern of associations
            for memory in self.memories[-5:]: #We consider t to t + 5 for associations
                if memory not in self.associations:
                    self.associations[memory] = {}
                if sensed not in self.associations[memory]:
                    self.associations[memory][sensed] = 0
                self.associations[memory][sensed] += 0.1
            self.memories.append(sensed)
            #Recall learned patterns
            #We can override our instincts through discipline and practice therefore instinct should take interpretation as input but that means instinct should do feeling -> action only. Or no, maybe instincts are weighted associations hardcoded, therefore they can be weakened.
            if sensed in self.associations and recollectionLevel < 1: #Potential lowers as we go from memory to memory, eventually no new memory can be activated. Pretty 
                #How to transform event in stimuli? Pass recollection through instinct? No keep stimuli in events
                #After all feeling feel is a perception
                for association in self.associations[sensed]:
                    if self.associations[sensed][association] >= 0.2:
                        print("I recall "+association+".")
                        self.sense(association, recollectionLevel+1) #Recollections are felt up to a point
            
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
    #Simulation 4
    print("Running simulation 4. Basic learning model.")
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
    Being1.memories.append("Random memory 1")
    Being1.memories.append("Random memory 2")
    Being1.memories.append("Random memory 3")
    Being1.memories.append("Random memory 4")
    Being1.memories.append("Random memory 5")
    Being1.memories.append("Random memory 6")
    print("A red ball has appeared.")
    World1.content = "Red ball"
    Being1.sense(None, 0)
    print("----")
    print("A black ball has appeared.")
    World1.content = "Black ball"
    Being1.sense(None, 0)
    print("----")
    Being1.memories.append("Random memory 7")
    Being1.memories.append("Random memory 8")
    Being1.memories.append("Random memory 9")
    Being1.memories.append("Random memory 10")
    Being1.memories.append("Random memory 11")
    Being1.memories.append("Random memory 12")
    print("He should now know to be afraid of red for what might come after.")
    print("A red ball has appeared.")
    World1.content = "Red ball"
    Being1.sense(None, 0)
    print("-----------------\n\n")
    return Being1

Being1 = runSimulation()
