import sklearn as skl
import numpy as np
from time import sleep
import time
from datetime import datetime
from threading import Thread, Event
#for debug
import sys
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

        self.predators = [Predator(world, bbox1) for i in range(predCount)]
        self.prey = [Prey(world, bbox1) for i in range(preyCount)]

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
                pred.hunt(self.prey, self.world, self)
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
                if pred.target:
                    bboxstr += "tag-%s; vR-%s; kR-%s; kC-%s; lfe-%s tgt-%s\n" % (pred.tag, pred.visionRange, pred.killRange, pred.killCount, pred.curLife, pred.target.tag) 
                else:
                    bboxstr += "tag-%s; vR-%s; kR-%s; kC-%s; lfe-%s tgt-%s\n" % (pred.tag, pred.visionRange, pred.killRange, pred.killCount, pred.curLife, "None")
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
        #refresh being coors
        being.curX0, being.curY0, being.curX1, being.curY1 = self.world.coords(being.tag)[0], self.world.coords(being.tag)[1], self.world.coords(being.tag)[2], self.world.coords(being.tag)[3]

        #if N, decrease Y by speed coef and ensure being isn't above N world boundary
        if directionMap[being.direction] == 'N':
            being.curY = self.world.coords(being.tag)[1]
            being.offset = -1 * (being.speed)
            if being.curY < 35:
                being.offset = (being.speed) / 2 # being.genY + (being.genY - self.world.winfo_height())
        #if S, increase Y by speed coef and check to see if it is below the bottom world boudary 
        elif directionMap[being.direction] == 'S':
            being.curY = self.world.coords(being.tag)[1]
            being.offset = being.speed 
            if being.curY > self.world.winfo_height()-5:
                being.offset = (-1 * (being.speed))/2 #being.genY - (self.world.winfo_height()-being.genY)
        #if E decrease X by speed coef and ensure not outside E world boundary
        elif directionMap[being.direction] == 'E':
            being.curX = self.world.coords(being.tag)[0]
            being.offset = being.speed
            if being.curX > self.world.winfo_width()-5:
                being.offset = (-1 * (being.speed) / 2)
        #if W increase X by speed coef and ensure not outside W world boundary
        elif directionMap[being.direction] == 'W':
            being.curX = self.world.coords(being.tag)[0]
            being.offset = -1 * (being.speed)
            if being.curX < 15:
                being.offset = (being.speed) / 2 # being.genX + (being.genX - self.world.winfo_width())

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
        if being.type =='predator':
            if being.target == None:
                being.direction = np.random.randint(4)

    #take one step forward (in dev)
    def walk(self):
        for pred in self.predators:
            self.move(pred)
        for prey in self.prey:
            self.move(prey)
    

class Predator(object):
    def __init__(self,world, bbox1):
        '''
        Predator Being: speed, stamina, lifespan, state, direction attributes.
                        hunt, reproduce methods.
        '''
        self.type = 'predator'
        self.state = 'idle'
        self.bbox1 = bbox1
        self.generation = 1
        self.birthTime = time.strftime("%H:%M:%S")
        self.speed = np.random.randint(3,7)
        self.persistence = np.random.randint(21,51)
        self.curPersistence = self.persistence
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(75, 200)
        self.state = {'state':'idle'}
        self.curLife = self.lifespan/2
        self.foodEfficiency = np.random.randint(30,100)
        self.direction = np.random.randint(4)
        self.visionRange = np.random.randint(50,101)
        self.strength = np.random.randint(1, 31)
        self.killRange = np.random.randint(2,8)
        self.genX = np.random.randint(18, 600)
        self.genY = np.random.randint(37, 600)
        self.curX = self.genX
        self.curY = self.genY
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])
        self.killCount = 0 
        self.target = None
        self.litterSize = np.random.randint(1,4)
        self.reproductiveAge = self.lifespan - np.random.randint(1, 5)
        self.preyDensityLimit = np.random.randint(4)
        self.reproduceFlag = True
        self.speciesPopulationMax = np.random.randint(100,300)
        self.genVar = np.random.randint(-99, 99)*.01
        self.timeAlive = 0

    def newGenVar(self):
        return  np.random.randint(-99, 99)*.01

    def refreshCoords(self, being, world):
        being.curX, being.curY = world.coords(being.tag[0]), world.coords(being.tag)[1]

    def hunt(self, prey, world, beingObj):
        '''
        
        '''
        #if hunter has a target and it is still persisting, keep hunting it
        if self.target and self.curPersistence > 0:
            self.navToTarget(self.target, world)
            return

        #refresh the coordinates
        lambda x: self.refreshCoords(x, world), prey

        #get a handy vision range
        xVR = range(int(world.coords(self.tag)[0]-self.visionRange), int(world.coords(self.tag)[2]+self.visionRange))
        yVR = range(int(world.coords(self.tag)[1]-self.visionRange), int(world.coords(self.tag)[3]+self.visionRange))
    
        #isolate targets if there are any
        targets = [p for p in prey if p.curX in xVR and p.curY in yVR]

        if len(targets) >= self.preyDensityLimit:
            self.reproduceFlag == False
        else: self.reproduceFlag == True
        
        #jump out if there aren't any and wander around idle
        if len(targets) == 0:
            self.curPersistence = self.persistence
            self.target = None
            self.state = 'idle'
            return
        elif len(targets) == 1:
            self.target = targets[0]
            self.navToTarget(self.target, world)
        elif len(targets) > 1:
            #get closer to current direction
            self.target = reduce(lambda a, x: a if abs(world.coords(a.tag)[self.direction]-world.coords(self.tag)[self.direction]) < abs(world.coords(x.tag)[self.direction]-world.coords(self.tag)[self.direction]) else x, targets)
            self.navToTarget(self.target, world)    


    def navToTarget(self, target, world):
        '''
            discern where the target is in relation to the hunter and set the vector in that direction
        '''
        #decrease persistence and update state to hunting
        self.curPersistence -= 1
        self.state = 'hunting'
        dirs = []
        x0kr, y0kr, x1kr, y1kr = world.coords(self.tag)[0] - self.killRange, world.coords(self.tag)[1] - self.killRange, world.coords(self.tag)[2] + self.killRange, world.coords(self.tag)[3] + self.killRange
        xkr, ykr = range(int(x0kr), int(x1kr)), range(int(y0kr), int(y1kr))

        xdir = [3 if (int((target.curX0+target.curX1)/2)) not in xkr and int(((target.curX0+target.curX1)/2)) - x0kr < 0 else 2]
        ydir = [0 if (int((target.curY0+target.curY1)/2)) not in ykr and int(((target.curY0+target.curY1)/2)) - y0kr < 0 else 1]
       
        lambda x: dirs.append(x)

        self.direction = np.random.choice(zip(xdir,ydir)[0])


    def kill(self, world, prey, deadPrey, allBeings):
        x0kr, y0kr, x1kr, y1kr = world.coords(self.tag)[0] - self.killRange, world.coords(self.tag)[1] - self.killRange, world.coords(self.tag)[2] + self.killRange, world.coords(self.tag)[3] + self.killRange
        xkr, ykr = range(int(x0kr), int(x1kr)), range(int(y0kr), int(y1kr))
        
        xKR = range(int(self.curX0 - self.killRange), int(self.curX1 - self.killRange))
        yKR = range(int(self.curY0 - self.killRange), int(self.curY1 + self.killRange))
        for p in prey:
            if (int((p.curX0+p.curX1)/2)) in xkr and (int((p.curY0+p.curY1)/2)) in ykr:
                try:
                    #pdb.set_trace()
                    allBeings.pop(allBeings.index(p))
                    deadPrey.append(prey.pop(prey.index(p)))
                    world.delete(p.tag)
                    self.killCount += 1
                    self.target = None
                    self.curLife  += 15
                    if self.curLife > self.lifespan:
                        self.curLife = self.lifespan
                    print '%s just KILLED %s!!!! while persistence=%s/%s and state=%s' % (self.tag, p.tag, self.curPersistence, self.persistence, self.state)
                    self.curPersistence = self.persistence
                except:
                    print sys.exc_info() 

    def age(self, beingsObj):     
        # every second decrease the lifespan decreases by 1
        if self.timeAlive % 2 == 0:
            self.curLife -= 1

            #if no more life, die
            if self.curLife <= 0:
                beingsObj.beings.pop(beingsObj.beings.index(self))
                beingsObj.deadPredators.append(beingsObj.predators.pop(beingsObj.predators.index(self)))
                beingsObj.world.delete(self.tag)

        self.timeAlive += 1
        if self.reproduceFlag == True and self.curLife > self.reproductiveAge and  len([p for p in beingsObj.predators if p.color == self.color])< self.speciesPopulationMax:
            if len([p for p in beingsObj.predators if p.color == self.color]) > 100:
                pass #pdb.set_trace()
            self.reproductiveAge += 1
            self.reproduce(beingsObj.world, beingsObj)
       
        if self.reproduceFlag == True and self.curLife > self.reproductiveAge and self.timeAlive % 50 == 0:
            self.reproductiveAge -= 1

    def reproduce(self, world, beingsObj):
        #instantiate new beings in a litter the size of the being
        offspring = [Predator(world, beingsObj.bbox) for p in range(int(self.litterSize))]
        
        #set attributes of offspring to parents, randomizing for genVar

        for kid in offspring:
            kid.generation = self.generation + 1
            kid.speed = self.speed + self.genVar 
            kid.persistence = self.persistence + self.genVar
            kid.lifespan = self.lifespan + self.genVar
            kid.curLife = .3 * self.curLife
            kid.killRange = self.killRange + self.genVar
            kid.visionRange = self.visionRange + self.genVar
            kid.litterSize = self.litterSize + self.genVar
            kid.genVar = self.newGenVar()
            kid.color = self.color
            kid.tag = world.create_rectangle(self.curX-4, self.curY-4, self.curX-14, self.curY-14, fill=self.color)
            beingsObj.predators.append(kid)
            beingsObj.beings.append(kid)

        self.curLife -= .1 * self.curLife
        


    def showInfo(self, event):
        self.bbox1.delete(1.0, END)
        self.bbox1.insert("tag-%s curX-%s curY-%s\n clickX-%s clickY-%s" % (self.tag, self.curX, self.curY, event.x, event.y))
        print "%s,%s" % (event.x, event.y)


class Prey(object):
    def __init__(self, world, bbox1):
        '''
        Prey Being : speed, stamina, lifespan, state, direction attributes.
                     hunt, reporduce methods.

        '''
        self.type = 'prey'
        self.bbox1 = bbox1
        self.state = 'idle'
        self.generation = 1
        self.speed = np.random.randint(3, 11)
        self.birthTime = time.strftime("%H:%M:%S")
        self.stamina = np.random.randint(1, 11)
        self.lifespan = np.random.randint(35, 120)
        self.visionRange = np.random.randint(5, 31)
        self.curLife = self.lifespan
        self.strength = np.random.randint(1, 11)
        self.state = {'state':'idle'}
        self.direction = np.random.randint(4)
        self.genX = np.random.randint(18, 500)
        self.genY = np.random.randint(37, 500)
        self.curX = self.genX
        self.curY = self.genY
        self.color = '#'+''.join([np.random.choice('0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()) for x in range(6)])
        self.litterSize = np.random.randint(1,6)
        self.genVar = float("%02d" % (np.random.randint(-99, 99)*.01))
        self.timeAlive = 0
        
    def age(self, beingsObj):
        if self.timeAlive % 2 == 0:
            self.curLife -= 1
            
            #if no more life, die
            if self.curLife <= 0:
                beingsObj.beings.pop(beingsObj.beings.index(self))
                beingsObj.deadPrey.append(beingsObj.prey.pop(beingsObj.prey.index(self)))
                beingsObj.world.delete(self.tag)
        
        self.timeAlive += 1

        if self.generation == 1 and self.timeAlive == 10:
            self.reproduce(beingsObj.world, beingsObj)

        if self.timeAlive == 100 or  self.timeAlive > 150 and self.timeAlive % 100 == 0:
            self.reproduce(beingsObj.world, beingsObj)
    
    def reproduce(self, world, beingsObj):
        #instantiate new beings in a litter the size of the being
        offspring = [Prey(world, beingsObj.bbox) for p in range(int(self.litterSize))]
        
        #set attributes of offspring to parents, randomizing for genVar

        for kid in offspring:
            kid.generation = self.generation + 1
            kid.speed = self.speed + self.genVar
            kid.lifespan = self.lifespan + self.genVar
            kid.visionRange = self.visionRange + self.genVar
            kid.litterSize = self.litterSize + self.genVar
            kid.genVar = self.genVar + self.genVar
            kid.color = self.color
            kid.tag = world.create_oval(self.curX-4, self.curY-4, self.curX-14, self.curY-14, fill=self.color)
            beingsObj.prey.append(kid)
            beingsObj.beings.append(kid)

        self.curLife -= self.litterSize
        
    
    def showInfo(self):
        self.bbox1.delete(1.0, END)
        self.bbox1.insert("tag-%s curX-%s curY-%s" % (self.tag, self.curX, self.curY))

