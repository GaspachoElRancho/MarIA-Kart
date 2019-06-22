# Mama mIA aka MarIA Kart

# AI Training (2/3)
# render : affichage du jeu simulé  
# Issu du Notebook3

# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi
# Thibaud Le Du - Gaspard Lauras

import pygame
import pygame.locals                                                          
import pygame.gfxdraw
import numpy as np
import math
from model import Model
import os, inspect

FPS = 60                                                                 
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 600
BORDER = 15
RADIUS = 10

RED = (255, 0, 0)
WHITE = (255, 255, 255)

##
scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) 
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"Images")
## 

class Rendering:                               
    
    def __init__(self, model):
        self.model = model
        pygame.display.init()
        self.clock = pygame.time.Clock()
        self.fond = self.model.fond
        
    def init(self):
        self.quit = False
        self._display()
        self.render()
        
    def render(self):
        self._process_events()
        fond = pygame.image.load( self.fond).convert()
        self.screen.blit(fond, (0,0))
        self.drawCheckpoints()
        self.drawCar()
        self.checkCollision()
        self.checkSensors()
        pygame.display.flip()
        self.clock.tick(FPS)
        return self._screenshot()
    
    def checkCollision (self):
        
        x1 = int(self.model.FL[0])
        y1 = int(self.model.FL[1])
        x2 = int(self.model.FR[0])
        y2 = int(self.model.FR[1])
        
        if self.checkcolor(x1, y1, 51,51,51) == True or self.checkcolor(x2, y2, 51,51,51) == True:
            self.model.collision = True
    
    def checkSensors(self) :
        angle_rad = math.radians(self.model.angle)
        k1 = 0
        k2 = 0
        k3 = 0
        k4 = 0
        k5 = 0
        
        self.model.xM = self.model.Sensor_Middle[0]
        self.model.yM = self.model.Sensor_Middle[1]
        
        while (self.checkcolor(int(self.model.xM), int(self.model.yM), 51,51,51)==False and self.model.xM>0 and self.model.yM>0) :
            self.model.xM = self.model.Sensor_Middle[0] + self.model.move_x*k1
            self.model.yM = self.model.Sensor_Middle[1] + self.model.move_y*k1
            k1 +=1 
            
        self.model.xM = self.model.Sensor_Middle[0]
        self.model.yM = self.model.Sensor_Middle[1]
        
        while (self.checkcolor(int(self.model.xM), int(self.model.yM), 51,51,51)==False and self.model.xM>0 and self.model.yM>0):
            self.model.xM = self.model.Sensor_Middle[0] + self.model.move_x*k2 * math.cos(math.pi /6) - self.model.move_y*k2 * math.sin(math.pi /6)
            self.model.yM = self.model.Sensor_Middle[1] + self.model.move_x*k2 * math.sin(math.pi /6) + self.model.move_y*k2 * math.cos(math.pi /6)
            k2 += 1
            
        self.model.xM = self.model.Sensor_Middle[0]
        self.model.yM = self.model.Sensor_Middle[1]
        
        while (self.checkcolor(int(self.model.xM), int(self.model.yM), 51,51,51)== False and self.model.xM>0 and self.model.yM>0):
            self.model.xM = self.model.Sensor_Middle[0] + self.model.move_x*k3 * math.cos(-math.pi /6) - self.model.move_y*k3 * math.sin(-math.pi /6)
            self.model.yM = self.model.Sensor_Middle[1] + self.model.move_x*k3 * math.sin(-math.pi /6) + self.model.move_y*k3 * math.cos(-math.pi /6)
            k3 += 1
            
        self.model.xM = self.model.Sensor_Middle[0]
        self.model.yM = self.model.Sensor_Middle[1]
        
        while (self.checkcolor(int(self.model.xM), int(self.model.yM) , 51,51,51)== False and self.model.xM >0 and self.model.yM >0):
            self.model.xM = self.model.Sensor_Middle[0] + self.model.move_x*k4 * math.cos(math.pi /3) - self.model.move_y*k4 * math.sin(math.pi /3)
            self.model.yM = self.model.Sensor_Middle[1] + self.model.move_x*k4 * math.sin(math.pi /3) + self.model.move_y*k4 * math.cos(math.pi /3)
            k4 += 1
            
        self.model.xM = self.model.Sensor_Middle[0]
        self.model.yM = self.model.Sensor_Middle[1]
        
        while (self.checkcolor(int(self.model.xM), int(self.model.yM), 51,51,51)== False and self.model.xM >10 and self.model.yM >0 ):
            self.model.xM = self.model.Sensor_Middle[0] + self.model.move_x*k5 * math.cos(-math.pi /3) - self.model.move_y*k5 * math.sin(-math.pi /3)
            self.model.yM = self.model.Sensor_Middle[1] + self.model.move_x*k5 * math.sin(-math.pi /3) + self.model.move_y*k5 * math.cos(-math.pi /3)
            k5 += 1
            
        self.model.k = [k1, k2, k3, k4, k5] 
        
                  
    def close(self):
        pygame.display.quit()
    
    def checkcolor(self, x, y, a, b, c): 
        if self.screen.get_at((x, y)) == (a, b, c, 255):
            return True
        else:
            return False

    def drawCheckpoints(self) :                                                
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP1)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP2)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP3)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP4)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP5) 
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP6)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP7)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP8)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP9)
        pygame.draw.rect(self.screen,[255,255,0],self.model.CP10)
        pygame.draw.rect(self.screen,[0,0,255],self.model.CP11)
        
    def drawCar(self) :                                                        
        pygame.draw.polygon(self.screen, WHITE, [np.around(self.model.FL), np.around(self.model.FR), np.around(self.model.BR),     np.around(self.model.BL)])
    
    def _display(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        
    def _screenshot(self):
        img = pygame.surfarray.array3d(pygame.display.get_surface()).astype(np.uint8)
        return np.fliplr(np.rot90(img,3))
        
    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True    
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_LEFT]:
            self.action = 1
        elif keys[pygame.locals.K_RIGHT]:
            self.action = 2
        else:
            self.action = 0