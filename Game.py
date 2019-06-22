# Mama mIA aka MarIA Kart
# Game

# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi
# Thibaud Le Du - Gaspard Lauras 

# Jeu final : Opposition entre le joueur humain et l'IA (qui utilise le fichier 
#             de type BestParams.npy pour jouer)

# Règles du jeu : Atteindre la ligne d'arrivée en premier, 
#                 en évitant de heurter les rebords du circuit

# Joueur humain : appuyer sur les flèches "gauche" et "droite" pour jouer
# Appuyer sur "espace" pour quitter

## Imports
import numpy as np
import matplotlib as plt

import pygame, random, sys ,os,time
from pygame.locals import *
import os, inspect                                     
from pygame.transform import scale
import pygame.surfarray as surfarray
import math
import random
import time



class Principale:
    def __init__(self,nomFond):
        ## Conditions initiales 

        paramsFile = ""

        if nomFond == "Sircuibo.png" :
            paramsFile = 'BestParamsSircuibo.npy'
        elif nomFond == "CIRCUIT11.png" :
            paramsFile = 'BestParamsCIRCUIT11.npy'                                                    

        fond = pygame.image.load(nomFond)
        pygame.font.init()
        FPS = 60

        clock = pygame.time.Clock()
        font = pygame.font.SysFont("", 20)
        tps = time.clock()
        pygame.init()

        width = 1000
        height = 600

        Timer = True
        temporise = 180

        main_s = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
        if nomFond == "Sircuibo.png":
            arrivee = pygame.Rect(70,300,72,10)
        elif nomFond == "CIRCUIT11.png":
            arrivee = pygame.Rect(70,270,72,10)
            ligne = pygame.Rect(70,250,72,10)
                    
        ## Fonctions utiles
        def checkcolor(x, y, a, b, c):
            if main_s.get_at((x, y)) == (a, b, c, 255):
                return True
            else:
                return False

        def timeclock(temporise):
            if temporise > 0:
                minutes, secondes = divmod(temporise,60)
                hours, minutes    = divmod(minutes, 60)
                time_left = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(secondes).zfill(2)
                temporise -= 1
                return temporise , time_left
                
        def display_all(main_surface, display_list, text_list):
            if nomFond == "CIRCUIT11.png" : 
                pygame.draw.rect(main_s,[255,255,255],ligne)
            for element in display_list:
                element.display(main_surface)
            for element_val in range(0, len(text_list)):
                main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (800, 555 + (10 * element_val)))

        def update_all(update_list):
            for element in update_list:
                element.update()

        ## Class Player
        class Player :
            def __init__(self, NomFichier,nomFond):
                
                # Polygône
                if nomFond == "CIRCUIT11.png" :
                    self.FL = np.array((90,250))   
                    self.FR = np.array((105,250)) 
                    self.BL = np.array((90,275))
                    self.BR = np.array((105,275)) 
                    self.Cx, self.Cy = [round(90+(105-90)/2),round(250+(275-250)/2)]
                if nomFond == "Sircuibo.png" :
                    self.FL = np.array((100,275))
                    self.FR = np.array((115,275)) 
                    self.BL = np.array((100,300))
                    self.BR = np.array((115,300)) 
                    self.Cx, self.Cy = [round(100+(115-100)/2),round(275+(300-275)/2)]

                # Sprite
                self.CorpsImage = pygame.image.load(NomFichier)

                # Mouvement
                self.forward = True        
                self.left = False
                self.right = False
                self.angle = 0
                self.angle2 = 0
                
                # Caractéristiques
                self.turn_speed = 1 
                self.top_speed = 4
                self.acceleration = 0.2
                self.deceleration = 0.1
                self.current_speed = 0
                self.move_x = 0
                self.move_y = 0
                self.winPlayer = False
                # Respawn checkpoints               
                if nomFond == "CIRCUIT11.png" :
                    self.CP1 = pygame.Rect(70,250,72,10)
                    self.CP2 = pygame.Rect(500,60,10,80)
                    self.CP3 = pygame.Rect(850,300,72,10)
                    self.CP4 = pygame.Rect(500,460,10,73)
                    self.respwn = 0   
                if nomFond == "Sircuibo.png"  :
                    self.CP1 = pygame.Rect(71,283,74,14)
                    self.CP2 = pygame.Rect(512,37,10,66)
                    self.CP3 = pygame.Rect(855,327,94,10)
                    self.CP4 = pygame.Rect(477,297,10,69)
                    self.respwn = 0
            
            # Vérification partie gagnée par le joueur
            def CheckWinPlayer(self):
                    if arrivee.collidepoint(self.Cx,self.Cy):
                        self.winPlayer = True
                    else :
                        self.winPlayer = False
            
                    return self.winPlayer
            
            # Vérification de collision contre les bordures du circuit
            def checkCollision (self) :     
                if(checkcolor(int(self.FL[0]), int(self.FL[1]) , 51 , 51 , 51) or checkcolor(int(self.FR[0]), int(self.FR[1]) , 51, 51,51)):
                    self.respawn() 
                    
            # Réapparition en cas de choc contre les bordures                
            def checkRespawn(self):

                if ((self.CP1.collidepoint(self.Cx,self.Cy)) and self.respwn == 3) :
                    self.respwn = 4
                    
                elif (((self.CP2.collidepoint(self.Cx,self.Cy)))) :
                    self.respwn= 1
                    
                elif ((self.CP3.collidepoint(self.Cx,self.Cy))) :
                    self.respwn = 2
                    
                elif ((self.CP4.collidepoint(self.Cx,self.Cy))) :
                    self.respwn = 3 

            def respawn(self):

                if nomFond == "CIRCUIT11.png" :
                    ###CIRCUI11.png
                    if self.respwn == 0:
                        self.FL = np.array((90,250))   
                        self.FR = np.array((105,250)) 
                        self.BL = np.array((90,275))
                        self.BR = np.array((105,275)) 
                        self.Cx, self.Cy = [round(90+(105-90)/2),round(250+(275-250)/2)]
                        self.angle = 0
                        self.angle2 = 0
                        
                    elif self.respwn == 1 :
                        self.FL = np.array((525,90))   
                        self.FR = np.array((525,105)) 
                        self.BL = np.array((500,90))
                        self.BR = np.array((500,105)) 
                        self.Cx, self.Cy = [round(500+(525-500)/2),round(90+(105-90)/2)]
                        self.angle = 270
                        self.angle2 = 0
                        
                    elif self.respwn == 2 :
                        self.FL = np.array((895,325))   
                        self.FR = np.array((880,325)) 
                        self.BL = np.array((895,300))
                        self.BR = np.array((880,300)) 
                        self.Cx, self.Cy = [round(880+(895-880)/2),round(300+(325-300)/2)]
                        self.angle = 180
                        self.angle2 = 0
                        
                    elif self.respwn == 3 :
                        self.FL = np.array((475,505))   
                        self.FR = np.array((475,490)) 
                        self.BL = np.array((500,505))
                        self.BR = np.array((500,490)) 
                        self.Cx, self.Cy = [round(475+(500-475)/2),round(490+(505-490)/2)]
                        self.angle = 90
                        self.angle2 = 0
                
                elif nomFond == "Sircuibo.png" :
                    ###Sircuibo.png
                    if self.respwn == 0:
                        self.FL = np.array((100,275))
                        self.FR = np.array((115,275)) 
                        self.BL = np.array((100,300))
                        self.BR = np.array((115,300)) 
                        self.Cx, self.Cy = [round(100+(115-100)/2),round(275+(300-275)/2)]
                        self.angle = 0
                        self.angle2 = 0

                    elif self.respwn == 1 :
                        self.FL = np.array((537,67))
                        self.FR = np.array((537,82)) 
                        self.BL = np.array((512,67))
                        self.BR = np.array((512,82)) 
                        self.Cx, self.Cy = [round(512+(537-512)/2),round(67+(82-67)/2)]
                        self.angle = 270 #droite
                        self.angle2 = 0

                    elif self.respwn == 2 :
                        self.FL = np.array((895,325))
                        self.FR = np.array((880,325)) 
                        self.BL = np.array((895,300))
                        self.BR = np.array((880,300)) 
                        self.Cx, self.Cy = [round(880+(895-880)/2),round(300+(325-300)/2)]
                        self.angle = 180 #en bas
                        self.angle2 = 0

                    elif self.respwn == 3 :
                        self.FL = np.array((452,342))                           #477,297
                        self.FR = np.array((452,327)) 
                        self.BL = np.array((477,342))
                        self.BR = np.array((477,327)) 
                        self.Cx, self.Cy = [round(452+(477-452)/2),round(327+(342-327)/2)]
                        self.angle = 110 #a gauche
                        self.angle2 = 0
                        
            # Réinitialisation des données après chaque coup                
            def reset_data(self): 
                self.angle2 = 0
                self.left = False
                self.right = False
                self.forward = True       
                if self.respwn == 4 :
                    self.forward = False
             
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

                xFL, yFL  = xFL * math.cos(angle_rad) - yFL * math.sin(angle_rad), xFL * math.sin(angle_rad) + yFL* math.cos(angle_rad)
                xFR, yFR = xFR * math.cos(angle_rad) - yFR * math.sin(angle_rad), xFR * math.sin(angle_rad) + yFR * math.cos(angle_rad)
                xBR, yBR = xBR * math.cos(angle_rad) - yBR * math.sin(angle_rad), xBR * math.sin(angle_rad) + yBR * math.cos(angle_rad)
                xBL, yBL = xBL * math.cos(angle_rad) - yBL * math.sin(angle_rad), xBL * math.sin(angle_rad) + yBL * math.cos(angle_rad)
                
                xFL, yFL  = xFL + self.Cx, yFL + self.Cy
                xFR, yFR  = xFR + self.Cx, yFR + self.Cy
                xBR, yBR  = xBR + self.Cx, yBR + self.Cy
                xBL, yBL  = xBL + self.Cx, yBL + self.Cy
                
                self.FL = [xFL, yFL]
                self.FR = [xFR, yFR]
                self.BR = [xBR, yBR]
                self.BL = [xBL, yBL]
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
            # Déterminer le point milieu de la voiture
            def calculate_center(self): 
                moyenneSommets_x = (self.FL[0] + self.FR[0] + self.BR[0] + self.BL[0]) / 4
                moyenneSommets_y = (self.FL[1] + self.FR[1] + self.BR[1] + self.BL[1]) / 4
                self.Cx = round(moyenneSommets_x)
                self.Cy = round(moyenneSommets_y)
                    
            # Affichage de la voiture
            def display(self, main_surface):      
                # Polygône
                pygame.draw.polygon(main_surface, (0,0,255), [np.around(self.FL), np.around(self.FR), np.around(self.BR), np.around(self.BL)])

                # Sprite
                temp_image = pygame.transform.rotate(self.CorpsImage, self.angle)

                ImaX = temp_image.get_width()/2
                ImaY = temp_image.get_height()/2

                # Coordonées du milieu de l'image
                CImX = ImaX + self.FL[0]
                CimY = ImaY + self.FL[1]

                # Décalage entre le centre de l'image et le centre de la voiture
                diffX = CImX - self.Cx
                diffy = CimY - self.Cy

                main_surface.blit(temp_image, (self.FL[0] - diffX,self.FL[1] - diffy))
         
            # Coup joué à chaque frame
            def update(self):
                self.move_x = 0
                self.move_y = 0
                self.rotate()
                self.move()
                self.calculate_center()
                self.reset_data()
                self.CheckWinPlayer()
                self.checkRespawn()
                self.checkCollision()

        ## Class AI
        class AI:
             
            def __init__(self):
                # Params (poids)
                self.params = np.load(paramsFile)
                self.w = np.reshape(self.params,(11, 17)) 
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
                # Sprite
                self.CorpsImage = pygame.image.load('IA.png')
                # Mouvement
                self.angle = 0
                self.forward = True       
                self.left = False
                self.right = False
                self.action = 0
                self.angle2 = 0
                # Propriétés réseau de neurones
                self.hidden = 10
                self.output = 3
                # Caractéristiques
                self.turn_speed = 1
                self.top_speed = 4
                self.acceleration = 0.2
                self.deceleration = 0.1
                self.current_speed = 0
                self.move_x = 0
                self.move_y = 0
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                # Etat de jeu
                self.cmp = 0
                self.winIA = False                                                  
            
            # Vérification de collision contre les bordures du circuit
            def checkCollision (self) :     
                if(checkcolor(int(self.FL[0]), int(self.FL[1]) , 51 , 51 , 51) or checkcolor(int(self.FR[0]), int(self.FR[1]) , 51, 51,51)):
                        self.respawn()  
            
            # Réapparition depuis le début en cas de choc 
            # (Sécurité : même si l'IA est normalement suffisamment entraînée pour ne pas mourir)
            def respawn(self):
                if nomFond == "CIRCUIT11.png" :
                    self.FL = np.array((90,250))   
                    self.FR = np.array((105,250)) 
                    self.BL = np.array((90,275))
                    self.BR = np.array((105,275)) 
                    self.Sensor_Middle = np.array((90 + int((105-90)/2), 250))
                    self.Cx, self.Cy = [round(90+(105-90)/2),round(250+(275-250)/2)]
                    self.State = [0,0,0,0,0]
                    self.angle = 0            
                if nomFond == "Sircuibo.png" :
                    self.FL = np.array((100,275))
                    self.FR = np.array((115,275)) 
                    self.BL = np.array((100,300))
                    self.BR = np.array((115,300))
                    self.Sensor_Middle = np.array((100 + int((115-100)/2), 275))
                    self.Cx, self.Cy = [round(100+(115-100)/2),round(275+(300-275)/2)]
                    self.State = [0,0,0,0,0]
                    self.angle = 0
                          
            # Vérification partie gagnée par l'IA
            def CheckWinIA(self):
                if arrivee.collidepoint(self.Cx,self.Cy):
                    self.winIA = True
                    self.cmp = 1
                else : 
                    self.winIA = False

                return self.winIA
            
            # Cerveau de l'IA :
            # Détermination des distances calculées à partir des capteurs
            def checkSensors(self) :
                angle_rad = math.radians(self.angle)
                
                k1 = 0
                k2 = 0
                k3 = 0
                k4 = 0
                k5 = 0
                
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                
                while (checkcolor(int(self.xM), int(self.yM), 51,51,51)==False and self.xM>0 and self.yM>0) :
                    self.xM = self.Sensor_Middle[0] + self.move_x*k1
                    self.yM = self.Sensor_Middle[1] + self.move_y*k1
                    k1 +=1 
                    
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                
                while (checkcolor(int(self.xM), int(self.yM), 51,51,51)==False and self.xM>0 and self.yM>0):
                    self.xM = self.Sensor_Middle[0] + self.move_x*k2 * math.cos(math.pi /6) - self.move_y*k2 * math.sin(math.pi /6)
                    self.yM = self.Sensor_Middle[1] + self.move_x*k2 * math.sin(math.pi /6) + self.move_y*k2 * math.cos(math.pi /6)
                    k2 += 1
                    
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                
                while (checkcolor(int(self.xM), int(self.yM), 51,51,51)== False and self.xM>0 and self.yM>0):
                    self.xM = self.Sensor_Middle[0] + self.move_x*k3 * math.cos(-math.pi /6) - self.move_y*k3 * math.sin(-math.pi /6)
                    self.yM = self.Sensor_Middle[1] + self.move_x*k3 * math.sin(-math.pi /6) + self.move_y*k3 * math.cos(-math.pi /6)
                    k3 += 1
                    
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                
                while (checkcolor(int(self.xM), int(self.yM) , 51,51,51)== False and self.xM >0 and self.yM >0):
                    self.xM = self.Sensor_Middle[0] + self.move_x*k4 * math.cos(math.pi /3) - self.move_y*k4 * math.sin(math.pi /3)
                    self.yM = self.Sensor_Middle[1] + self.move_x*k4 * math.sin(math.pi /3) + self.move_y*k4 * math.cos(math.pi /3)
                    k4 += 1
                    
                self.xM = self.Sensor_Middle[0]
                self.yM = self.Sensor_Middle[1]
                
                while (checkcolor(int(self.xM), int(self.yM), 51,51,51)== False and self.xM >10 and self.yM >0 ):
                    self.xM = self.Sensor_Middle[0] + self.move_x*k5 * math.cos(-math.pi /3) - self.move_y*k5 * math.sin(-math.pi /3)
                    self.yM = self.Sensor_Middle[1] + self.move_x*k5 * math.sin(-math.pi /3) + self.move_y*k5 * math.cos(-math.pi /3)
                    k5 += 1

                self.State[0] = k1
                self.State[1] = k2
                self.State[2] = k3
                self.State[3] = k4
                self.State[4] = k5                                           
            # Calcul du coup à jouer à partir des données renvoyées par les capteurs
            def calculation (self):
                # States
                sensor_mid = self.State[0]
                sensor_r = self.State[1]
                sensor_l = self.State[2]
                sensor_ff = self.State[3]
                sensor_ll = self.State[4]

                tab_z = []                                                             
                tab_y = []                             
                
                for x in range (0, self.hidden) :
                    op = self.w[x,0]+ self.w[x,1]*sensor_mid+ self.w[x,2]*sensor_r+ self.w[x,3]*sensor_l + self.w[x,4]*sensor_ff+ self.w[x,5]*sensor_ll                           
                    z = np.tanh(op) 
                    tab_z.append(z)
                                                                                       
                for k in range (0, self.output) :                                     
                    y = self.w[k,6] + self.w[k,7]*tab_z[0]+ self.w[k,8]*tab_z[1] + self.w[k,9]*tab_z[2] + self.w[k,10]*tab_z[3]+ self.w[k,11]*tab_z[4] + self.w[k,12]*tab_z[5] + self.w[k,13]*tab_z[6]+ self.w[k,14]*tab_z[7]+ self.w[k,15]*tab_z[8] + self.w[k,16]*tab_z[9]  
                    tab_y.append(y)        

                self.action = np.argmax(tab_y)                         
            # Exécution du coup déterminé à l'issue du calcul
            def act(self):
                """ 
                 0 - Keep Forward
                 1 - Move Left
                 2 - Move Right
                """
                if self.action == 1:
                    self.right = False
                    self.left = True
                elif self.action == 2:   
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
            # Calcul du point milieu de la voiture
            def calculate_center(self): 
                moyenneSommets_x = (self.FL[0] + self.FR[0] + self.BR[0] + self.BL[0]) / 4
                moyenneSommets_y = (self.FL[1] + self.FR[1] + self.BR[1] + self.BL[1]) / 4
                self.Cx = round(moyenneSommets_x)
                self.Cy = round(moyenneSommets_y)    
            
            # Réinitialisation des données après chaque coup    
            def reset_data(self): 
                self.angle2 = 0
                self.forward = True
                
                if self.cmp == 1 : 
                    self.forward = False       
            
            # Affichage de la voiture
            def display(self, main_surface):           
                #Polygône
                pygame.draw.polygon(main_surface, (0,0,255), [np.around(self.FL), np.around(self.FR), np.around(self.BR), np.around(self.BL)])

                #IMAGE
                temp_image = pygame.transform.rotate(self.CorpsImage, self.angle)

                ImaX = temp_image.get_width()/2
                ImaY = temp_image.get_height()/2

                #Coordonées du milieu de l'image
                CImX = ImaX + self.FL[0]
                CimY = ImaY + self.FL[1]

                #Décalage entre le centre de l'image et le centre de la voiture
                diffX = CImX - self.Cx
                diffy = CimY - self.Cy

                main_surface.blit(temp_image, (self.FL[0] - diffX,self.FL[1] - diffy))
            
            # Coup joué à chaque frame    
            def update(self):                                                         
                self.move_x = 0                                  
                self.move_y = 0
                #AI moving
                self.rotate()
                self.move()
                self.calculate_center() 
                #AI thinking
                self.calculation()
                self.act()
                self.checkSensors()
                #Reset and checking
                self.reset_data()
                self.CheckWinIA()
                self.checkCollision()

        ## Boucle de jeu
        # Déclaration des voitures
        vehiclePlayer = Player('Joueur.png',nomFond)
        vehicleAI = AI()
        # Caractéristiques de jeu
        running = True
        canIncrement = True
        # Booléens d'arrêt
        StopIA = False
        StopPlayer = False
        # Boucle de jeu
        while running :
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    None
            
            if Timer == True :
                temporise, time_left = timeclock(temporise)
                       
            main_s.blit(fond,(0,0))
            tps  = time.clock()
            key = pygame.key.get_pressed()
            
            #Quitter 
            if key[pygame.K_SPACE]:                                                     #Press "space" to quit the game
                running = False
                
            #Actions Player
            if key[pygame.K_LEFT]:
                vehiclePlayer.left = True

            if key[pygame.K_RIGHT]:
                vehiclePlayer.right = True
            
            if key[pygame.K_UP]:
                vehiclePlayer.forward = True

            if key[pygame.K_r]:
                vehiclePlayer.FL = np.array((505,250))   
                vehiclePlayer.FR = np.array((530,250)) 
                vehiclePlayer.BL = np.array((505,300))
                vehiclePlayer.BR = np.array((530,300)) 
                vehiclePlayer.Sensor_Middle = np.array((505 + int((530-505)/2), 250))
                vehiclePlayer.angle = 0
              
            #Mettre à jour
            to_update = [vehicleAI, vehiclePlayer]
            to_display = [vehicleAI, vehiclePlayer]
            
            if Timer == False : 
                tps  = float(time.clock() -t) 
                tpscourse = round(tps,3)
                update_all(to_update)
                police = pygame.font.Font(None, 30)
                txt = police.render(str("Timer : "+str(tpscourse)), 1, (255, 255, 255))
                main_s.blit(txt, (850, 565))
                

                police = pygame.font.Font(None, 30)
                txt = police.render(str("Respawn point : "+str(vehiclePlayer.respwn)), 1, (255, 255, 255))

                main_s.blit(txt, (400, 565))
                
                
           
            to_text = [""]        
            display_all(main_s, to_display, to_text) 
            
            
            police = pygame.font.Font(None, 30)
            txt = police.render(str("Press space to quit"), 1, (255, 255, 255))
            main_s.blit(txt, (20, 565))
            
            
            if Timer == True :
                police = pygame.font.Font(None, 80)
                txt = police.render(str(time_left), 1 , (255, 255, 255))
                main_s.blit(txt, (400, 275))
                if temporise ==0:
                    Timer = False
                    t  = time.clock()
            
            if vehicleAI.winIA == True :
                StopIA = True
            
            if StopIA == True:
                if vehicleAI.current_speed > 0.5:
                    police = pygame.font.Font(None, 120)
                    txt = police.render(str("GAME OVER"), 1, (255, 255, 255))
                    main_s.blit(txt, (275, 250))
                    vehiclePlayer.current_speed = 0
                else :
                    time.sleep(2)
                    running = False

            if vehiclePlayer.winPlayer == True:
                StopPlayer = True

            if StopPlayer == True :
                if  vehiclePlayer.current_speed >0.5:
                    police = pygame.font.Font(None, 120)
                    txt = police.render(str("YOU WIN"), 1, (255, 255, 255))
                    main_s.blit(txt, (325, 250))
                    vehicleAI.current_speed = 0
                else :
                    time.sleep(2)
                    running = False
                            
            pygame.display.flip()
            
            main_s.blit(fond,(0,0))

        # Close the window and quit    
        pygame.quit()


