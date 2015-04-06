import sklearn as skl
import numpy as np
from time import sleep
from threading import Thread
#for debug
import pdb

directionMap = {i:x for i,x in enumerate("N S E W".split())}

class Beings:
    def __init__(self, world, predCount, preyCount, sbtn):
        '''args world (eg Canvas object), predCount and preyCount, initiates life process when live is called in pain loop
        '''
        self.world = world
        self.world.state = {'state' : 'inactive'}

        self.predators = [Predator() for i in range(predCount)]
        self.prey = [Prey() for i in range(preyCount)]

        self.beings = list(self.predators + self.prey)
        self.tags = list()

        #stop button for binding after live() is called 
        self.sbtn = sbtn

    def live(self):
        self.world.state['state'] = 'active'
        
        for being in self.beings:
            if being.type == 'predator':
                being.tag = self.world.create_rectangle(being.genX, being.genY, being.genX+10, being.genY-10, fill=being.color)
            else:
                being.tag = self.world.create_oval(being.genX, being.genY, being.genX+10, being.genY-10, fill=being.color)
        
        self.session = Thread(target=self.activate)
        self.session.start()
        
        #bind the Thread object _Thread__stop() method to the stop button
        self.sbtn.config(command=self.session._Thread__stop())

    def activate(self):
        while self.world.state['state'] == 'active':
            #move each being
            map(lambda x: self.move(x), self.beings)
            
            #predators hunt!
            for pred in self.predators:
                pred.hunt(self.prey)
                pred.kill(self.world, self.prey, self.beings) 
            sleep(.3)

    def move(self, being):
        '''
        Receives a predator or prey object and gives it a new set of position attributes
        '''
        #if N, decrease Y by speed coef and ensure being isn't above N world boundary
        if directionMap[being.direction] == 'N':
            thisC = being.genY
            being.offset = -1 * (being.speed * .5)
            being.genY = being.genY - being.offset
            if being.genY < 20:
                being.offset = 0 # being.genY + (being.genY - self.world.winfo_height())
                being.genY = thisC # - being.offset
        #if S, increase Y by speed coef and check to see if it is below the bottom world boudary 
        elif directionMap[being.direction] == 'S':
            thisC = being.genY
            being.offset = being.speed * .5
            being.genY = being.genY + being.offset
            if being.genY > self.world.winfo_height():
                being.offset = 0 #being.genY - (self.world.winfo_height()-being.genY)
                being.genY = thisC + being.offset
        #if E decrease X by speed coef and ensure not outside E world boundary
        elif directionMap[being.direction] == 'E':
            thisC = being.genX
            being.offset = being.speed * .5
            being.genX = being.genX + being.offset
            if being.genX > self.world.winfo_width():
                being.offset = 0
                being.genX = thisC + being.offset
        #if W increase X by speed coef and ensure not outside W world boundary
        elif directionMap[being.direction] == 'W':
            thisC = being.genX
            being.offset = -1 * (being.speed * .5)
            being.genX = being.genX - being.offset
            if being.genX < 20:
                being.offset = 0 # being.genX + (being.genX - self.world.winfo_width())
                being.genX = thisC# - being.offset

        #randomize being vector
        being.direction = np.random.randint(4)

        #move the being to the new coords
        if directionMap[being.direction] in ['N','S']:
           self.world.move(being.tag, 0, being.offset)
        elif directionMap[being.direction] in ['E','W']:
           self.world.move(being.tag, being.offset, 0)
        #pdb.set_trace()

    #take one step forward (in dev)
    def walk(self):
        for pred in self.predators:
            self.move(pred)
        for prey in self.prey:
            self.move(prey)
    

class Predator(object):
    def __init__(self):
        '''
        Predator Being: speed, stamina, lifespan, state, direction attributes.
                        hunt, reproduce methods.
        '''
        self.type = 'predator'
        self.generation = 1
        self.speed = np.random.randint(1,11)
        self.stamina = np.random.randint(11)
        self.lifespan = np.random.randint(501)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.visionRange = np.random.randint(31)
        self.strength = np.random.randint(11)
        self.killRange = np.random.randint(11)
        self.genX = np.random.randint(300)
        self.genY = np.random.randint(300)
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])
        
    def hunt(self, beings):
        '''
            the 'beings' are actually just prey
        '''
        for being in beings:
            if self.genX in range(int(being.genX - self.visionRange), int(being.genX + self.visionRange)) and self.genY in range(int(being.genY - self.visionRange), int(being.genY + self.visionRange)):
                #if more east, move west
                if self.genX > being.genX:
                    self.direction = 3
                #if west, move east
                elif self.genX < being.genX:
                    self.direction = 2
                #if north, move south
                elif self.genY > being.genY:
                    self.direction = 1
                #if south, move north
                elif self.genY < being.genY:
                    self.direction = 0
                print '%s is hunting %s!!' % (self.tag, being.tag)

    def kill(self, world, prey, allBeings):
        for p in prey:
            if self.genX in range(int(p.genX - self.killRange), int(p.genX + self.killRange)) and self.genY in range(int(p.genY - self.killRange), int(p.genY + self.killRange)):
                victims = world.find_overlapping(self.genX-self.killRange, self.genY-self.killRange, self.genX+self.killRange, self.genY+self.killRange)
                pdb.set_trace()
                lambda x: world.delete(x), victims
                lambda x: allBeings.pop(allBeings.index(x)), victims
                print '%s just KILLED %s!!!!' % (self.tag, p.tag)

class Prey(object):
    def __init__(self):
        '''
        Prey Being : speed, stamina, lifespan, state, direction attributes.
                     hunt, reporduce methods.

        '''
        self.type = 'prey'
        self.generation = 1
        self.speed = np.random.randint(11)
        self.stamina = np.random.randint(11)
        self.lifespan = np.random.randint(501)
        self.visionRange = np.random.randint(11)
        self.strength = np.random.randint(11)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.genX = np.random.randint(300)
        self.genY = np.random.randint(300)
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])

        

            
