from abc import ABC, abstractmethod

#Autonomous elements
class Agent:
    def __init__(self, period, name, pos):
        self.name=name
        self.period=period
        self.counter=period
        self.active=True
        self.pos=pos

    def go(self):
        self.counter-=1
        if not self.counter:
            self.action()
            self.counter=self.period    
    
    @abstractmethod
    def action(self):
        pass

class Trap(Agent):
    def __init__(self, period, name, pos):
        super().__init__(period, name, pos)
        self.activated = True

    def action(self): 
        if self.activated:
            print(self.name, " est actif en ", self.pos,)
            self.activated=False
        else:
            print(self.name,"se ferme en ", self.pos)
            self.activated=True
            
    
class Lemming(Agent):

    def __init__(self, period, name, pos, goal, dir):
        super().__init__(period,name, pos)
        self.goal=goal #TODO: will become EXIT ? reify ?
        self.active = True
        self.dir = dir

    def action(self):
        self.pos+=self.dir
        print(self.name," avance en ",self.pos)
        if self.pos==self.goal:
            self.active=False
            print(self.name," a fini")
        
