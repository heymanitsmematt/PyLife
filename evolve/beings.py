import sklearn as skl
import numpy as np
from time import sleep
import time
from datetime import datetime
from threading import Thread, Event
#for debug
import pdb
from Tkinter import END
from timer import Timer

directionMap = {i:x for i,x in enumerate("N S E W".split())}

class Beings:
    def __init__(self, world, predCount, preyCount, sbtn, bbox, bbox1, timelbl):
        '''args world (eg Canvas object), predCount and preyCount, initiates life process when live is called in pain loop
        '''
        self.world = world
        self.world.state = {'state' : 'inactive'}

        self.predators = [Predator(bbox1) for i in range(predCount)]
        self.prey = [Prey(bbox1) for i in range(preyCount)]

        self.deadPredators = list()
        self.deadPrey = list()

        self.beings = list(self.predators + self.prey)
        self.tags = list()

        #stop button and being box for binding after live() is called 
        self.sbtn = sbtn
        self.bbox = bbox
        self.bbox1 = bbox1
        self.timelbl = timelbl


    def live(self):
        #set the state to active and clear the canvas of all attributes
        self.world.state['state'] = 'active'
        self.world.delete("all")

        for being in self.beings:
            if being.type == 'predator':
                being.tag = self.world.create_rectangle(being.genX, being.genY, being.genX+10, being.genY-10, fill=being.color)
            else:
                being.tag = self.world.create_oval(being.genX, being.genY, being.genX+10, being.genY-10, fill=being.color)
        
        
        #start session thread
        self.stopThread = False
        self.session = Thread(target=self.activate)
        self.session.start()

        #bind the Thread object _Thread__stop() method to the stop button
        self.sbtn.config(command=self.threadStop)
        

    def threadStop(self):
        self.stopThread = True
        self.session = None


    def activate(self):
        #instantiate timer and pass in timerlbl
        self.timer = Timer(self.timelbl)
        
        #bind showInfo to each being
        lambda x: self.world.tag_bind(x.tag,"<ButtonPress-1>", x.showInfo), self.beings

        while self.stopThread == False:
            #move each being
            map(lambda x: self.move(x), self.beings)
           
            #predators hunt!
            for pred in self.predators:
                pred.hunt(self.prey, self.world)
                pred.kill(self.world, self.prey, self.deadPrey, self.beings) 
            
            #age the beings
            for being in self.beings:
                being.age(self)

            #update the clock
            self.timer.updateClock()

            #update being box
            self.bbox.delete(1.0, END)
            bboxstr = "Predators \n"
            for pred in self.predators:
                bboxstr += "tag-%s; vR-%s; kR-%s; kC-%s; lfe-%s\n" % (pred.tag, pred.visionRange, pred.killRange, pred.killCount, pred.curLife)
            bboxstr += "#pred-%s  #prey-%s #beings=%s\nDead Predators:\n" % (len(self.predators), len(self.prey), len(self.beings))
            for pred in self.deadPredators:
                bboxstr += "tag-%s; vR-%s, kR-%s; kC-%s\n" % (pred.tag, pred.visionRange, pred.killRange, pred.killCount)    
            self.bbox.insert("1.0", bboxstr)

            #check to ensure game is not over
            if len(self.predators) == 0 or len(self.prey) == 0:
                self.threadStop()

            #sleep to avoid stack overflow
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

        #move the being to the new coords
        if directionMap[being.direction] in ['N','S']:
           self.world.move(being.tag, 0, being.offset)
        elif directionMap[being.direction] in ['E','W']:
           self.world.move(being.tag, being.offset, 0)
        
        #randomize being vector if idle
        if being.state == 'idle':
            being.direction = np.random.randint(4)
        if being.type == 'prey':
            being.direction = np.random.randint(4)

    #take one step forward (in dev)
    def walk(self):
        for pred in self.predators:
            self.move(pred)
        for prey in self.prey:
            self.move(prey)
    

class Predator(object):
    def __init__(self, bbox1):
        '''
        Predator Being: speed, stamina, lifespan, state, direction attributes.
                        hunt, reproduce methods.
        '''
        self.type = 'predator'
        self.state = 'idle'
        self.bbox1 = bbox1
        self.generation = 1
        self.birthTime = time.strftime("%H:%M:%S")
        self.speed = np.random.randint(1,11)
        self.persistence = np.random.randint(21,51)
        self.curPersistence = self.persistence
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(30, 101)
        self.state = {'state':'idle'}
        self.curLife = self.lifespan
        self.direction = np.random.randint(4)
        self.visionRange = np.random.randint(21, 41)
        self.strength = np.random.randint(1, 11)
        self.killRange = np.random.randint(11,21)
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
        if self.target and self.target in beings and self.curPersistence > 0:
            return self.navToTarget(self.target, world)
        #if we have a target and the target is still in range
        elif self.target and self.target in range(int(self.target.curX - self.visionRange), int(self.target.curX + self.visionRange)) and self.curY in range(int(self.target.curY - self.visionRange), int(self.target.curY + self.visionRange)):
            return self.navToTarget(self.target, world)
        #if there isn't a target
        else:
            #try and find a target
            for being in beings:
                being.curX, being.curY = world.coords(being.tag)[0], world.coords(being.tag)[1]
                if being.curX in range(int(self.curX - self.visionRange), int(self.curX + self.visionRange)) and being.curY in range(int(self.curY - self.visionRange), int(self.curY + self.visionRange)):
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
        
        #update state to hunting so the direction doesn't get randomized next iteration
        self.state = 'hunting'

        #seek in each direction randomly
        searches = [self.navEast, self.navWest, self.navNorth, self.navSouth]
        i=0
        while i < 24:
            thisSearch = np.random.choice(searches)
            thisSearch(being, world)
            i += 1
        

    #if more east, move west
    def navEast(self, being, world):
        if self.curX < (being.curX-self.killRange) and self.curX < (being.curX+self.killRange):
            self.direction = 3
            return
    #if west, move east
    def navWest(self, being, world):
        if self.curX > (being.curX-self.killRange) and self.curX > (being.curX+self.killRange):
            self.direction = 2
            return
    #if north, move south
    def navSouth(self, being, world):
        if self.curY < (being.curY-self.killRange) and self.curY < (being.curY+self.killRange):
            self.direction = 1
            return
    #if south, move north
    def navNorth(self, being, world):
        if self.curY > (being.curY-self.killRange) and self.curY > (being.curY+self.killRange):
            self.direction = 0
            return


    def kill(self, world, prey, deadPrey, allBeings):
        self.curX, self.curY = world.coords(self.tag)[0], world.coords(self.tag)[1]
        for p in prey:
            p.curX, p.curY = world.coords(p.tag)[0], world.coords(p.tag)[1]
            if p.curX in range(int(self.curX - self.killRange), int(self.curX + self.killRange)) and p.curY in range(int(self.curY - self.killRange), int(self.curY + self.killRange)):
                try:
                    allBeings.pop(allBeings.index(p))
                    deadPrey.append(prey.pop(prey.index(p)))
                    world.delete(p.tag)
                    self.killCount += 1
                    self.target = None
                    self.curLife += 5
                    print '%s just KILLED %s!!!! while persistence=%s/%s and state=%s' % (self.tag, p.tag, self.curPersistence, self.persistence, self.state)
                    self.curPersistence = self.persistence
                except:
                    print 'kill exc?'
    
    def age(self, beingsObj):     
        # every 30 seconds the lifespan decreases by 1
        if ((datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(self.birthTime, "%H:%M:%S"))).seconds % 5 == 0:
            self.curLife -= .2

            #if no more life, die
            if self.curLife <= 0:
                beingsObj.beings.pop(beingsObj.beings.index(self))
                beingsObj.deadPredators.append(beingsObj.predators.pop(beingsObj.predators.index(self)))
                beingsObj.world.delete(self.tag)
                
    def showInfo(self, event):
        self.bbox1.delete(1.0, END)
        self.bbox1.insert("tag-%s curX-%s curY-%s\n clickX-%s clickY-%s" % (self.tag, self.curX, self.curY, event.x, event.y))
        print "%s,%s" % (event.x, event.y)


class Prey(object):
    def __init__(self, bbox1):
        '''
        Prey Being : speed, stamina, lifespan, state, direction attributes.
                     hunt, reporduce methods.

        '''
        self.type = 'prey'
        self.bbox1 = bbox1
        self.state = 'idle'
        self.generation = 1
        self.speed = np.random.randint(1, 11)
        self.birthTime = time.strftime("%H:%M:%S")
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(50, 201)
        self.visionRange = np.random.randint(1, 11)
        self.curLife = self.lifespan
        self.strength = np.random.randint(1, 11)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.genX = np.random.randint(18, 400)
        self.genY = np.random.randint(37, 400)
        self.curX = self.genX
        self.curY = self.genY
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])

        
    def age(self, beingsObj):
        if ((datetime.strptime(time.strftime("%H:%M:%S"), "%H:%M:%S") - datetime.strptime(self.birthTime, "%H:%M:%S"))).seconds % 5 == 0:
            self.curLife -= .2
            
            #if no more life, die
            if self.curLife <= 0:
                beingsObj.beings.pop(beingsObj.beings.index(self))
                beingsObj.deadPrey.append(beingsObj.prey.pop(beingsObj.prey.index(self)))
                beingsObj.world.delete(self.tag)
    
    def showInfo(self):
        self.bbox1.delete(1.0, END)
        self.bbox1.insert("tag-%s curX-%s curY-%s" % (self.tag, self.curX, self.curY))

