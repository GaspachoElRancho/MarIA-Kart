# Mama mIA aka MarIA Kart

# AI Training (3/3)
# model : objet voiture du jeu simulé  
# Issu du Notebook3

# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi
# Thibaud Le Du - Gaspard Lauras

import pygame, random, sys 
from pygame.locals import *
from pygame.transform import scale
import pygame.surfarray as surfarray
import numpy as np
import math
import random
import numpy as np
import time

class Model:
     
    def init(self,nomFond):
        # Partie
        self.fond = nomFond
        self.done = False
        fond = pygame.image.load(self.fond)
        # Temps
        self.tps = time.clock()
        self.r = 0
        self.bonus1 = 10000
        self.bonus2 = 100000
        self.resetTime = True
        # Polygône
        
        if nomFond == "CIRCUIT11.png" :
            self.FL = np.array((90,250))   
            self.FR = np.array((105,250)) 
            self.BL = np.array((90,275))
            self.BR = np.array((105,275)) 
            self.Sensor_Middle = np.array((90 + int((105-90)/2), 250))
            self.Cx, self.Cy = [round(90+(105-90)/2),round(250+(275-250)/2)]
        if nomFond == "Sircuibo.png" :
            self.FL = np.array((100,275))
            self.FR = np.array((115,275)) 
            self.BL = np.array((100,300))
            self.BR = np.array((115,300)) 
            self.Sensor_Middle = np.array((100 + int((115-100)/2), 275))
            self.Cx, self.Cy = [round(100+(115-100)/2),round(275+(300-275)/2)]
        self.State = [0,0,0,0,0]
        self.t = 0
        self.canIncrement = True
        # Mouvement
        self.forward = True       
        self.left = False
        self.right = False
        self.angle = 0
        self.angle2 = 0
        self.turn_speed = 1
        self.top_speed = 4
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.current_speed = 0
        self.move_x = 0
        self.move_y = 0
        self.Score = 0
        self.xM = self.Sensor_Middle[0]
        self.yM = self.Sensor_Middle[1]
        self.k = [0,0,0,0,0]
        # Checkpoints
        if nomFond == "CIRCUIT11.png":
            self.CP1 = pygame.Rect(180,60,10,80)
            self.CP2 = pygame.Rect(470,60,10,80)
            self.CP3 = pygame.Rect(750,60,10,80)
            self.CP4 = pygame.Rect(852,200,72,10)
            self.CP5 = pygame.Rect(852,400,72,10)               
            self.CP6 = pygame.Rect(750,460,10,73)
            self.CP7 = pygame.Rect(500,460,10,73)
            self.CP8 = pygame.Rect(250,460,10,73)               
            self.CP9 = pygame.Rect(70,200,72,10)
            self.CP10 = pygame.Rect(70,250,72,10)
            self.CP11 = pygame.Rect(70,400,72,10)
        elif nomFond == "Sircuibo.png":
            self.CP1 = pygame.Rect(180,157,10,67)
            self.CP2 = pygame.Rect(338,132,105,10)
            self.CP3 = pygame.Rect(512,37,10,66)
            self.CP4 = pygame.Rect(740,37,10,66)
            self.CP5 = pygame.Rect(855,140,94,10)
            self.CP6 = pygame.Rect(855,327,94,10)
            self.CP7 = pygame.Rect(782,395,10,78)
            self.CP8 = pygame.Rect(651,299,78,10)
            self.CP9 = pygame.Rect(477,297,10,80)
            self.CP10 = pygame.Rect(71,283,74,14)
            self.CP11 = pygame.Rect(221,397,10,64)
        # Collision
        self.collision = False                                                     
    
    def seed(self, seed = 42) :
        random.seed(seed)
    
    def game_over(self):
        return self.done
        
    # Mise à jour de l'état des capteurs           
    def sensors(self):                                                          
        self.State[0] = self.k[0]
        self.State[1] = self.k[1]
        self.State[2] = self.k[2]
        self.State[3] = self.k[3]
        self.State[4] = self.k[4]
        
    def state(self):
        self.sensors()
        return    self.State                                            
    
    # Actionne en fonction de la valeur de "a" le mouvement correspondant
    # Virer à gauche, virer à droite, poursuivre tout droit 
    def act(self, a):
        """ 
         0 - Keep Forward
         1 - Move Left
         2 - Move Right
        """
        if a == 1:
            self.right = False
            self.left = True
        elif a == 2:   
            self.left = False
            self.right = True
        else :
            self.right = False
            self.left = False
    
    # Mécanique de la voiture 
    # Rotation
    def rotate(self):                                                           
        if self.left:                          
            self.angle += self.turn_speed * self.current_speed
            self.angle2 -= self.turn_speed * self.current_speed
        elif self.right:                          
            self.angle -= self.turn_speed * self.current_speed
            self.angle2 += self.turn_speed * self.current_speed
        self.angle =  self.angle % 360
        angle_rad = math.radians(self.angle2)
        
        #Update  
        xFL, yFL = self.FL[0] - self.Cx, self.FL[1] - self.Cy
        xFR, yFR = self.FR[0] - self.Cx, self.FR[1] - self.Cy
        xBR, yBR = self.BR[0] - self.Cx, self.BR[1] - self.Cy
        xBL, yBL = self.BL[0] - self.Cx, self.BL[1] - self.Cy
        xSM, ySM = self.Sensor_Middle[0] - self.Cx, self.Sensor_Middle[1] - self.Cy

        xFL, yFL  = xFL * math.cos(angle_rad) - yFL * math.sin(angle_rad), xFL * math.sin(angle_rad) + yFL* math.cos(angle_rad)
        xFR, yFR = xFR * math.cos(angle_rad) - yFR * math.sin(angle_rad), xFR * math.sin(angle_rad) + yFR * math.cos(angle_rad)
        xBR, yBR = xBR * math.cos(angle_rad) - yBR * math.sin(angle_rad), xBR * math.sin(angle_rad) + yBR * math.cos(angle_rad)
        xBL, yBL = xBL * math.cos(angle_rad) - yBL * math.sin(angle_rad), xBL * math.sin(angle_rad) + yBL * math.cos(angle_rad)
        xSM, ySM = xSM * math.cos(angle_rad) - ySM * math.sin(angle_rad), xSM * math.sin(angle_rad) + ySM * math.cos(angle_rad)
        
        xFL, yFL  = xFL + self.Cx, yFL + self.Cy
        xFR, yFR  = xFR + self.Cx, yFR + self.Cy
        xBR, yBR  = xBR + self.Cx, yBR + self.Cy
        xBL, yBL  = xBL + self.Cx, yBL + self.Cy
        xSM, ySM  = xSM + self.Cx, ySM + self.Cy
        
        self.FL = [xFL, yFL]
        self.FR = [xFR, yFR]
        self.BR = [xBR, yBR]
        self.BL = [xBL, yBL]
        self.Sensor_Middle = [xSM, ySM] 
    
    # Translation    
    def move(self):                                                             
        if self.forward:
            if self.current_speed < self.top_speed:
                self.current_speed += self.acceleration
        else:
            if self.current_speed > 0:
                self.current_speed -= self.deceleration
            else:
                self.current_speed = 0
        
        angle_rad = math.radians(self.angle)
        self.move_x = - self.current_speed * math.sin(angle_rad)
        self.move_y = - self.current_speed * math.cos(angle_rad)

        #Update 
        self.FL[0] += self.move_x
        self.FL[1] += self.move_y
        self.FR[0] += self.move_x
        self.FR[1] += self.move_y
        self.BR[0] += self.move_x
        self.BR[1] += self.move_y
        self.BL[0] += self.move_x
        self.BL[1] += self.move_y
        self.Sensor_Middle[0] += self.move_x 
        self.Sensor_Middle[1] += self.move_y
    
    def calculate_center(self): 
        moyenneSommets_x = (self.FL[0] + self.FR[0] + self.BR[0] + self.BL[0]) / 4
        moyenneSommets_y = (self.FL[1] + self.FR[1] + self.BR[1] + self.BL[1]) / 4
        self.Cx = round(moyenneSommets_x)
        self.Cy = round(moyenneSommets_y)
    
    # Reset les données à la fin de chaque coup    
    def reset_data(self): 
        self.angle2 = 0
        self.left = False
        self.right = False
        self.forward = True   
    
    # Calcul du score en fonction du checkpoint traversé et du temps mis
    def checkScore(self):
        if self.resetTime == True :
            self.r = time.clock()
            self.resetTime = False
            
        self.tps = (time.clock() - self.r )
        if ((self.canIncrement) and (self.CP1.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP2.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP3.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP4.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP5.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP6.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP7.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP8.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP9.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP11.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + (self.bonus1/(self.tps - self.t)))
            self.t = self.tps
        elif ((self.canIncrement) and (self.CP10.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]))) :
            self.canIncrement = False
            self.Score = int(self.Score + self.bonus2/(self.tps - self.t))
            self.t = self.tps
            self.done = True                                                    # FIN DE LA PARTIE (WIN)
        else :
            canIncrement = True
    
    # Vérification de passage de checkpoint ou de collision ou de victoire          
    def reward(self) :     
        self.checkScore() 
        if self.collision :
                self.done = True                                                # FIN DE LA PARTIE (LOSE)
                self.resetTime = True
                #self.respawn()  
        elif self.CP10.collidepoint(self.Sensor_Middle[0], self.Sensor_Middle[1]):
                self.done = True                                                # FIN DE LA PARTIE (WIN)
        return self.Score
    
    # Exécution d'un tour de jeu    
    def update(self):                                                           
        self.move_x = 0                                  
        self.move_y = 0
        self.rotate()
        self.move()
        self.calculate_center()
        self.sensors() 
        self.reset_data()
        return self.reward()
        