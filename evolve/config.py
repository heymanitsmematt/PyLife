import numpy as np
from Tkinter import *

class WorldConfiguration:
    
    '''
        predator configuration settings (and also preycount)
    '''
     
    def __init__(self):
        self.predCount = 7 
        self.preyCount = 10
        
        self.predSpeedMin = 3
        self.predSpeedMax = 7
        self.predSpeed = np.random.randint(self.predSpeedMin, self.predSpeedMax)

        self.predPersistMin = 3       
        self.predPersistMax = 7
        self.predPersistance = np.random.randint(self.predPersistMin, self.predPersistMax)

        self.predLifespanMin = 75
        self.predLifespanMax = 200
        self.predLifespan = np.random.randint(self.predLifespanMin, self.predLifespanMax)

        self.predVisionRangeMin =3
        self.predVisionRangeMax = 31
        self.predVisionRange = np.random.randint(self.predVisionRangeMin ,self.predVisionRangeMax)

        self.predKillRangeMin = 2
        self.predKillRangeMax = 8
        self.predKillRange = np.random.randint(self.predKillRangeMin, self.predKillRangeMax)

        self.predLitterSizeMin =1
        self.predLitterSizeMax = 4 
        self.predLitterSize = np.random.randint(self.predLitterSizeMin, self.predLitterSizeMax)

        self.predReproductiveAgeMin = 1
        self.predReproductiveAgeMax = 5
        self.predReproductiveAge = np.random.randint(self.predReproductiveAgeMin, self.predReproductiveAgeMax)

        self.predDensityLimit = np.random.randint(4)
       
        '''
            Prey settings
        '''
        self.preySpeedMin = 3
        self.preySpeedMax = 11
        self.preyLifespanMin = 35
        self.preyLifespanMax = 120
        self.preyLitterSizeMin = 1
        self.preyLitterSizeMax = 6

    def reconfigure(self, main):
        #predLabel, Prey label
        predLbl = Label(main.conf, text="Predators")
        predLbl.grid(row=1, column=1, columnspan=2, padx=55, pady=5)
        
        
        preyLbl = Label(main.conf, text="Prey")
        preyLbl.grid(row=1, column=3, columnspan=2, padx=55, pady=5)
        
        #predCount
        self.predCountScale = Scale(main.conf, from_=1, to=20, orient=HORIZONTAL, label="Count", command=self.updatePredCount)
        self.predCountScale.set(5)
        self.predCountScale.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        self.predCount = self.predCountScale.get()
        
        #preyCount
        self.preyCountScale = Scale(main.conf, from_=1, to=100, orient=HORIZONTAL, label="Count", command=self.updatePreyCount)
        self.preyCountScale.set(50)
        self.preyCountScale.grid(row=2, column=3, columnspan=2, padx=5, pady=5)
        self.predCount = self.predCountScale.get()
        
        #predSpeedMin
        self.predSpeedMinScale = Scale(main.conf, from_=1, to=10, orient=HORIZONTAL, label="Speed Min.")
        self.predSpeedMinScale.set(3)
        self.predSpeedMinScale.grid(row=3, column=1, padx=5, pady=5)
        self.predSpeedMin = self.predSpeedMinScale.get()

        #predSpeedMax
        self.predSpeedMaxScale = Scale(main.conf, from_=1, to=20, orient=HORIZONTAL, label="Speed Max")
        self.predSpeedMaxScale.set(7)
        self.predSpeedMaxScale.grid(row=3, column=2, padx=5, pady=5)
        self.predSpeedMax = self.predSpeedMaxScale.get()

        self.predSpeedMinScale.config(command=self.updatePredSpeed)
        self.predSpeedMaxScale.config(command=self.updatePredSpeed)

        #predPersistMin
        self.predPersistMinScale = Scale(main.conf, from_=1, to=10, orient=HORIZONTAL, label="Persist Min")
        self.predPersistMinScale.set(3)
        self.predPersistMinScale.grid(row=4, column=1, padx=5, pady=5)
        self.predPersistMin = self.predPersistMinScale.get()
        
        #predPersistMax
        self.predPersistMaxScale = Scale(main.conf, from_=1, to=20, orient=HORIZONTAL, label="Persist Max")
        self.predPersistMaxScale.set(7)
        self.predPersistMaxScale.grid(row=4, column=2, padx=5, pady=5)
        self.predPersistMax = self.predPersistMaxScale.get()

        self.predPersistMinScale.config(command=self.updatePredPersist)
        self.predPersistMaxScale.config(command=self.updatePredPersist)

        #predlifespanMin
        self.predLifespanMinScale = Scale(main.conf, from_=50, to=175, orient=HORIZONTAL, label="Lifespan Min")
        self.predLifespanMinScale.set(75)
        self.predLifespanMinScale.grid(row=5, column=1, padx=5, pady=5)
        self.predLifespanMin = self.predLifespanMinScale.get()

        #predLifespanMax
        self.predLifespanMaxScale = Scale(main.conf, from_=175, to=400, orient=HORIZONTAL, label="Lifespan Max")
        self.predLifespanMaxScale.set(200)
        self.predLifespanMaxScale.grid(row=5, column=2, padx=5, pady=5)
        self.predLifespanMax = self.predLifespanMaxScale.get()

        self.predLifespanMinScale.config(command=self.updatePredLifespan)
        self.predLifespanMaxScale.config(command=self.updatePredLifespan)

        #predVisionRangeMax
        self.predVisionRangeMinScale = Scale(main.conf, from_=1, to=10, orient=HORIZONTAL, label="VisRange Max")
        self.predVisionRangeMinScale.set(3)
        self.predVisionRangeMinScale.grid(row=6, column=1, padx=5, pady=5)
        self.predVisionRangeMin = self.predVisionRangeMinScale.get()

        #predVisionRangeMax
        self.predVisionRangeMaxScale = Scale(main.conf, from_=10, to=50, orient=HORIZONTAL, label="VisRange Max")
        self.predVisionRangeMaxScale.set(31)
        self.predVisionRangeMaxScale.grid(row=6, column=2, padx=5, pady=5)
        self.predVisionRange = self.predVisionRangeMaxScale.get()

        self.predVisionRangeMinScale.config(command=self.updatePredVisionRange)
        self.predVisionRangeMaxScale.config(command=self.updatePredVisionRange)

        #predkillRangeMin
        self.predKillRangeMinScale = Scale(main.conf, from_=1, to=5, orient=HORIZONTAL, label="KillRange Max")
        self.predKillRangeMinScale.set(2)
        self.predKillRangeMinScale.grid(row=7, column=1, padx=5, pady=5)
        self.predKillRangeMin = self.predKillRangeMinScale.get()

        #predKillRangeMax
        self.predKillRangeMaxScale = Scale(main.conf, from_=5, to=15, orient=HORIZONTAL, label="KillRange Max")
        self.predKillRangeMaxScale.set(8)
        self.predKillRangeMaxScale.grid(row=7, column=2, padx=5, pady=5)
        self.predKillRangeMax = self.predKillRangeMaxScale.get()

        self.predKillRangeMinScale.config(command=self.updatePredKillRange)
        self.predKillRangeMaxScale.config(command=self.updatePredKillRange)


        #predLittersizeMin
        self.predLitterSizeMinScale = Scale(main.conf, from_=1, to=3, orient=HORIZONTAL, label="Littersize Min")
        self.predLitterSizeMinScale.set(1)
        self.predLitterSizeMinScale.grid(row=8, column=1, padx=5, pady=5)
        self.predLitterSizeMin = self.predLitterSizeMinScale.get()

        #predLittersizeMax
        self.predLitterSizeMaxScale = Scale(main.conf, from_=3, to=6, orient=HORIZONTAL, label="Littersize Max")
        self.predLitterSizeMaxScale.set(4)
        self.predLitterSizeMaxScale.grid(row=8, column=2, padx=5, pady=5)
        self.predLitterSizemax = self.predLitterSizeMaxScale.get()

        self.predLitterSizeMinScale.config(command=self.updatePredLitterSize)
        self.predLitterSizeMaxScale.config(command=self.updatePredLitterSize)

        #predReproductiveAgeMin
        self.predReproductiveAgeMinScale = Scale(main.conf, from_=1, to=3, orient=HORIZONTAL, label="Spawn Age Min")
        self.predReproductiveAgeMinScale.set(1)
        self.predReproductiveAgeMinScale.grid(row=9, column=1, padx=5, pady=5)
        self.predReproductiveAgeMin = self.predReproductiveAgeMinScale.get()

        #predReproductive
        self.predReproductiveAgeMaxScale = Scale(main.conf, from_=3, to=7, orient=HORIZONTAL, label="Spawn Age Max")
        self.predReproductiveAgeMaxScale.set(5)
        self.predReproductiveAgeMaxScale.grid(row=9, column=2, padx=5, pady=5)
        self.predReproductiveAgeMax = self.predReproductiveAgeMaxScale.get()

        self.predReproductiveAgeMinScale.config(command=self.updatePredReproductiveAge)
        self.predReproductiveAgeMaxScale.config(command=self.updatePredReproductiveAge)
        
        #predDensityLimitMax
        self.predDensityLimitMaxScale = Scale(main.conf, from_=1, to=7, orient=HORIZONTAL, label="Density Limit", command=self.updatePredDensityLimit)
        self.predDensityLimitMaxScale.set(1)
        self.predDensityLimitMaxScale.grid(row=10, column=1, columnspan=2, padx=5, pady=5)
        self.predDensityLimitMax = self.predDensityLimitMaxScale.get()

        '''
            Prey settings
        '''

        
        #preySpeedMin
        self.preySpeedMinScale = Scale(main.conf, from_=1, to=10, orient=HORIZONTAL, label="Speed Min.")
        self.preySpeedMinScale.set(3)
        self.preySpeedMinScale.grid(row=3, column=3, padx=5, pady=5)
        self.preySpeedMin = self.preySpeedMinScale.get()

        #preySpeedMax
        self.preySpeedMaxScale = Scale(main.conf, from_=1, to=20, orient=HORIZONTAL, label="Speed Max")
        self.preySpeedMaxScale.set(11)
        self.preySpeedMaxScale.grid(row=3, column=4, padx=5, pady=5)
        self.preySpeedMax = self.preySpeedMaxScale.get()

        self.preySpeedMinScale.config(command=self.updatePreySpeed)
        self.preySpeedMaxScale.config(command=self.updatePreySpeed)
       
        #preylifespanMin
        self.preyLifespanMinScale = Scale(main.conf, from_=10, to=75, orient=HORIZONTAL, label="Lifespan Min")
        self.preyLifespanMinScale.set(35)
        self.preyLifespanMinScale.grid(row=5, column=3, padx=5, pady=5)
        self.preyLifespanMin = self.preyLifespanMinScale.get()

        #preyLifespanMax
        self.preyLifespanMaxScale = Scale(main.conf, from_=75, to=200, orient=HORIZONTAL, label="Lifespan Max")
        self.preyLifespanMaxScale.set(120)
        self.preyLifespanMaxScale.grid(row=5, column=4, padx=5, pady=5)
        self.preyLifespanMax = self.preyLifespanMaxScale.get()

        self.preyLifespanMinScale.config(command=self.updatePreyLifespan)
        self.preyLifespanMaxScale.config(command=self.updatePreyLifespan)

        #preyLittersizeMin
        self.preyLitterSizeMinScale = Scale(main.conf, from_=1, to=3, orient=HORIZONTAL, label="VisionRange Min")
        self.preyLitterSizeMinScale.set(1)
        self.preyLitterSizeMinScale.grid(row=6, column=3, padx=5, pady=5)
        self.preyLitterSizeMin = self.preyLitterSizeMinScale.get()

        #preyLittersizeMax
        self.preyLitterSizeMaxScale = Scale(main.conf, from_=3, to=10, orient=HORIZONTAL, label="VisionRange Max")
        self.preyLitterSizeMaxScale.set(6)
        self.preyLitterSizeMaxScale.grid(row=6, column=4, padx=5, pady=5)
        self.preyLitterSizeMax = self.preyLitterSizeMaxScale.get()

        self.preyLitterSizeMinScale.config(command=self.updatePreyLitterSize)
        self.preyLitterSizeMaxScale.config(command=self.updatePreyLitterSize)

    def updatePredCount(self, event):
        self.predCount = self.predCountScale.get()

    def updatePreyCount(self, event):
        self.preyCount = self.preyCountScale.get()

    def updatePredSpeed(self, event):
        self.predSpeed = np.random.randint(self.predSpeedMinScale.get(), self.predSpeedMaxScale.get()) 

    def updatePredPersist(self, event):
        self.predPersist = np.random.randint(self.predPersistMinScale.get(), self.predPersistMaxScale.get())

    def updatePredLifespan(self, event):
        self.predLifespan = np.random.randint(self.predLifespanMinScale.get(), self.predLifespanMaxScale.get())
    
    def updatePredVisionRange(self, event):
        self.predVisionRange = np.random.randint(self.predVisionRangeMinScale.get(), self.predVisionRangeMaxScale.get())

    def updatePredKillRange(self, event):
        self.predKillRange = np.random.randint(self.predKillRangeMinScale.get(), self.predKillRangeMaxScale.get())

    def updatePredLitterSize(self, event):
        self.predLitterSize = np.random.randint(self.predLitterSizeMinScale.get(), self.predLitterSizeMaxScale.get())

    def updatePredReproductiveAge(self, event):
        self.predReproductiveAge = np.random.randint(self.predReproductiveAgeMinScale.get(), self.predReproductiveAgeMaxScale.get())

    def updatePredDensityLimit(self, event):
        self.predDensityLimitMax = np.random.randint(self.predDensityLimitMaxScale.get())

    def updatePreySpeed(self, event):
        self.preySpeed = np.random.randint(self.preySpeedMinScale.get(), self.preySpeedMaxScale.get())

    def updatePreyLifespan(self, event):
        self.preyLifespan = np.random.randint(self.preyLifespanMinScale.get(), self.preyLifespanMaxScale.get())

    def updatePreyLitterSize(self, event):
        self.preyLitterSize = np.random.randint(self.preyLitterSizeMinScale.get(), self.preyLitterSizeMaxScale.get())




















