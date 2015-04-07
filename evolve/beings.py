import sklearn as skl
import numpy as np
from time import sleep
from threading import Thread
#for debug
import pdb
from Tkinter import END

directionMap = {i:x for i,x in enumerate("N S E W".split())}

class Beings:
    def __init__(self, world, predCount, preyCount, sbtn, bbox):
        '''args world (eg Canvas object), predCount and preyCount, initiates life process when live is called in pain loop
        '''
        self.world = world
        self.world.state = {'state' : 'inactive'}

        self.predators = [Predator() for i in range(predCount)]
        self.prey = [Prey() for i in range(preyCount)]

        self.beings = list(self.predators + self.prey)
        self.tags = list()

        #stop button and being box for binding after live() is called 
        self.sbtn = sbtn
        self.bbox = bbox


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
                pred.hunt(self.prey, self.world)
                pred.kill(self.world, self.prey, self.beings) 
            
            self.bbox.delete(1.0, END)
            bboxstr = "Predators \n"
            for pred in self.predators:
                bboxstr += "tag-%s; vR-%s; kR-%s; kC-%s; \n" % (pred.tag, pred.visionRange, pred.killRange, pred.killCount,)
            self.bbox.insert("1.0", bboxstr)
            sleep(.1)
            
    def move(self, being):
        '''
        Receives a predator or prey object and gives it a new set of position attributes
        '''
        #if N, decrease Y by speed coef and ensure being isn't above N world boundary
        if directionMap[being.direction] == 'N':
            being.curY = self.world.coords(being.tag)[1]
            being.offset = -1 * (being.speed * .5)
            if being.curY < 35:
                being.offset = (being.speed * .5) / 2 # being.genY + (being.genY - self.world.winfo_height())
        #if S, increase Y by speed coef and check to see if it is below the bottom world boudary 
        elif directionMap[being.direction] == 'S':
            being.curY = self.world.coords(being.tag)[1]
            being.offset = being.speed * .5
            if being.curY > self.world.winfo_height()-100:
                being.offset = (-1 * (being.speed * .5))/2 #being.genY - (self.world.winfo_height()-being.genY)
        #if E decrease X by speed coef and ensure not outside E world boundary
        elif directionMap[being.direction] == 'E':
            being.curX = self.world.coords(being.tag)[0]
            being.offset = being.speed * .5
            if being.curX > self.world.winfo_width()-100:
                being.offset = (-1 * (being.speed * .5) / 2)
        #if W increase X by speed coef and ensure not outside W world boundary
        elif directionMap[being.direction] == 'W':
            being.curX = self.world.coords(being.tag)[0]
            being.offset = -1 * (being.speed * .5)
            if being.curX < 15:
                being.offset = (being.speed * .5) / 2 # being.genX + (being.genX - self.world.winfo_width())

        #randomize being vector if idle
        if being.state == 'idle':
            being.direction = np.random.randint(4)
        if being.type == 'prey':
            being.direction = np.random.randint(4)

        #move the being to the new coords
        if directionMap[being.direction] in ['N','S']:
           self.world.move(being.tag, 0, being.offset)
        elif directionMap[being.direction] in ['E','W']:
           self.world.move(being.tag, being.offset, 0)

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
        self.state = 'idle'
        self.generation = 1
        self.speed = np.random.randint(1,11)
        self.persistence = np.random.randint(21,51)
        self.curPersistence = self.persistence
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(100, 501)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.visionRange = np.random.randint(21, 51)
        self.strength = np.random.randint(1, 11)
        self.killRange = np.random.randint(5,21)
        self.genX = np.random.randint(18, 400)
        self.genY = np.random.randint(37, 400)
        self.curX = self.genX
        self.curY = self.genY
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])
        self.killCount = 0 
        self.target = None

    def hunt(self, beings, world):
        '''
            the 'beings' are actually just prey
        '''
        #refresh predator coordinates
        self.curX, self.curY = world.coords(self.tag)[0], world.coords(self.tag)[1]

        #if we have a target and the predator is still persisting
        if self.target and self.curPersistence > 0:
            return self.navToTarget(self.target, world)
        #if we have a target and the target is still in range
        elif self.target and self.target in range(int(self.target.curX - self.visionRange), int(self.target.curX + self.visionRange)) and self.curY in range(int(self.target.curY - self.visionRange), int(self.target.curY + self.visionRange)):
            return self.navToTarget(self.target, world)
        #if there isn't a target
        else:
            #try and find a target
            for being in beings:
                if self.curX in range(int(being.curX - self.visionRange), int(being.curX + self.visionRange)) and self.curY in range(int(being.curY - self.visionRange), int(being.curY + self.visionRange)):
                    self.state = 'hunting'
                    self.curPersistence = self.persistence
                    self.target = being
                    return self.navToTarget(being, world)
                #no target, stay idle
                else:
                    self.state='idle'
                    self.target=None
                    self.curPersistence = self.persistence

    def navToTarget(self, being, world):
        #refresh target coords
        try:
            being.curX, being.curY = world.coords(being.tag)[0], world.coords(being.tag)[1]
        except: pass

        #decrease persistence by 1
        self.curPersistence -= 1
        
        #print (self.curX, self.curY), (being.curX, being.curY)

        #if more east, move west
        if self.curX < (being.curX-self.killRange) and self.curX < (being.curX+self.killRange):
            self.direction = 3
            return
        #if west, move east
        elif self.curX > (being.curX-self.killRange) and self.curX > (being.curX+self.killRange):
            self.direction = 2
            return
        #if north, move south
        elif self.curY < (being.curY-self.killRange) and self.curY < (being.curY+self.killRange):
            self.direction = 1
            return
        #if south, move north
        elif self.curY > (being.curY-self.killRange) and self.curY > (being.curY+self.killRange):
            self.direction = 0
            return

    def kill(self, world, prey, allBeings):
        self.curX, self.curY = world.coords(self.tag)[0], world.coords(self.tag)[1]
        for p in prey:
            p.curX, p.curY = world.coords(p.tag)[0], world.coords(p.tag)[1]
            if p.curX in range(int(self.curX - self.killRange), int(self.curX + self.killRange)) and p.curY in range(int(self.curY - self.killRange), int(self.curY + self.killRange)):
                try:
                    allBeings.pop(allBeings.index(p))
                    prey.pop(prey.index(p))
                    world.delete(p.tag)
                    self.killCount += 1
                    self.target = None
                    self.curPersistence = self.persistence
                    print '%s just KILLED %s!!!!' % (self.tag, p.tag)
                except: pass

class Prey(object):
    def __init__(self):
        '''
        Prey Being : speed, stamina, lifespan, state, direction attributes.
                     hunt, reporduce methods.

        '''
        self.type = 'prey'
        self.state = 'idle'
        self.generation = 1
        self.speed = np.random.randint(1, 11)
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(100, 501)
        self.visionRange = np.random.randint(1, 11)
        self.strength = np.random.randint(1, 11)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.genX = np.random.randint(18, 400)
        self.genY = np.random.randint(37, 400)
        self.curX = self.genX
        self.curY = self.genY
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])

        

            
