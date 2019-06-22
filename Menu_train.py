# Mama mIA aka MarIA Kart
# Sous-menu (1/2): gestion de l'entraînement de l'IA 

# Gaspard Lauras - Thibaud Le Du
# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi

# Choix de la map à entraîner [renouvellement du fichier contenant les meilleurs params]

import pygame
from pygame.locals import *
from Execution_CarRace import Execute

##################################################
# Classe menu de l'entraînement de l'IA

class choix_train:

	def __init__(self):


		pygame.init()
		pygame.font.init()

		width = 600
		heigth = 400

		ecran_menu = pygame.display.set_mode((width,heigth))
		ecran_menu.fill((0,0,0))

		#TEXTS
		text = pygame.font.SysFont("comicsansms",30,True,False)
		titreFont = pygame.font.SysFont("comicsansms",50,True,False)

		titre_circuit11 = text.render("EASY",True,(0,0,0),(150,150,150))
		titre_Sircuibo = text.render("HARDCORE",True,(0,0,0),(150,150,150))
		titre_retour = text.render("< RETOUR",True,(0,0,0),(150,150,150))
		
		text_epoch = pygame.font.SysFont("comicsansms",30,True,False)
		titre_epoch =text_epoch.render("Entrez votre nombre de simulations:",True,(255,255,255),(0,0,0))
		text_epoch_conseilles = pygame.font.SysFont("comicsansms",30,True,False)       
		titre_epoch_conseilles = text_epoch.render("EASY : 40 minimum      HARDCORE : 60 minimum",True,(255,255,255),(0,0,0))
		titre_red = titreFont.render("TRAIN",True,(255,0,0),(0,0,0))
		titre_vert = titreFont.render("TRAIN",True,(0,255,0),(0,0,0))

		#IMAGE
		x = 250
		y = int(0.6*x)

		image_Circuit11 = pygame.transform.scale(pygame.image.load("CIRCUIT11.png"),(x,y))
		image_Sircuibo = pygame.transform.scale(pygame.image.load("Sircuibo.png"),(x,y))


		pygame.display.flip()

		attente = True
		C_red = True
		cp = 0

		#ACTIONS (QUIT OU CLIQUE)
		font = pygame.font.Font(None, 50)
		number = ""
		nbSimulations = ""
		saisie = True
		while saisie :
			for evt in pygame.event.get():
				if evt.type == KEYDOWN:
					if evt.unicode.isdigit():
						number += evt.unicode
					elif evt.key == K_BACKSPACE:
						number = number[:-1]
					elif evt.key == K_RETURN:
						nbSimulations = number
						number = ""
						saisie = False 
						break
				elif evt.type == QUIT:
					return
			ecran_menu.fill ((0, 0, 0))
			ecran_menu.blit(titre_epoch,(10,15))
			ecran_menu.blit(titre_epoch_conseilles,(10,50))
			block = font.render(number, True, (255, 255, 255))
			rect = block.get_rect()
			rect.center = ecran_menu.get_rect().center
			ecran_menu.blit(block, rect)
			pygame.display.flip()
		
		ecran_menu.fill ((0, 0, 0))
				
		while attente:

			#ANIMATION
			cp += 1
			if cp%15 == 0:
				C_red = not(C_red)

			if C_red:
				color = (255,0,0)
				ecran_menu.blit(titre_vert,(214,15))
			else:
				color = (0,255,0)
				ecran_menu.blit(titre_red,(214,15))

			for event in pygame.event.get():
				if event.type == pygame.QUIT :
					attente = False


				key = pygame.key.get_pressed()

				if key[pygame.K_ESCAPE]:
					attente =False

				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 50 and event.pos[0] <= 250 and event.pos[1] >= 300 and event.pos[1] <= 350:
					pygame.quit()
					train_Circuit11 = Execute("CIRCUIT11.png", epochs = int(nbSimulations))
					

				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 350 and event.pos[0] <= 550 and event.pos[1] >= 300 and event.pos[1] <= 350:
					pygame.quit()
					train_Sircuibo = Execute("Sircuibo.png", epochs = int(nbSimulations))
					
			#BOUTONS
			CIRCUIT11 = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))
			ecran_menu.blit(titre_circuit11, (80,315))

			Sircuibo = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))
			ecran_menu.blit(titre_Sircuibo, (390,315))
			
			
			
					# Epochs = pygame.draw.rect(ecran_menu,(150,150,150),(350,300,200,50))
					# ecran_menu.blit(titre_Epochs, (390,315))			
# def name():
#     pygame.init()
#     screen = pygame.display.set_mode((480, 360))
#     name = ""
#     font = pygame.font.Font(None, 50)
#     while True:
#         for evt in pygame.event.get():
#             if evt.type == KEYDOWN:
#                 if evt.unicode.isalpha():
#                     name += evt.unicode
#                 elif evt.key == K_BACKSPACE:
#                     name = name[:-1]
#                 elif evt.key == K_RETURN:
#                     print(name)
#                     name = ""
#             elif evt.type == QUIT:
#                 return
#         screen.fill ((0, 0, 0))
#         block = font.render(name, True, (255, 255, 255))
#         rect = block.get_rect()
#         rect.center = screen.get_rect().center
#         screen.blit(block, rect)
#         pygame.display.flip()

			#IMAGES
			pygame.draw.rect(ecran_menu, color, (20,95,x+10,y+10),10)
			pygame.draw.rect(ecran_menu, color, (320,95,x+10,y+10),10)

			ecran_menu.blit(image_Circuit11,(25,100))
			ecran_menu.blit(image_Sircuibo,(325,100))
			

			pygame.display.flip()

			




		pygame.quit()


