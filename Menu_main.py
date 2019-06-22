# Mama mIA aka MarIA Kart
# MAIN

# Gaspard Lauras - Thibaud Le Du
# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi

# Menu principal : choix entre entraîner l'IA et jouer [IA et Jeux]

import pygame
from pygame.locals import *
from Menu_train import choix_train
from Menu_Choix_Circuit import choix_circuit

pygame.init()
pygame.font.init()

##################################################
# Classe menu principal

class Menu:
	def __init__(self):

		ecran_menu = pygame.display.set_mode((600,400))
		ecran_menu.fill((0,0,0))

		pygame.display.flip()


		#########################################

		#TEXTS
		textFont = pygame.font.SysFont("comicsansms",60,True,False)
		titreFont = pygame.font.SysFont("comicsansms",80,True,False)



		#RENDERS
		text = textFont.render("PLAY", True, (0,0,0),(150,150,150))
		text_train = textFont.render("TRAIN", True, (0,0,0),(150,150,150))
		titreRouge = titreFont.render("MarIA Kart", True, (255,0,0),(0,0,0))
		titreVert = titreFont.render("MarIA Kart", True, (0,255,0),(0,0,0))


		#########################################

		#BOUCLE PRINCIPALE


		attente = True

		rouge = True
		cp = 0

		while attente:
			for event in pygame.event.get():

				#QUIT
				key = pygame.key.get_pressed()

				if key[pygame.K_ESCAPE]:
					attente =False

				if event.type == pygame.QUIT :
					attente = False


				#BOUTON DEMAREZ
				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 238 and event.pos[0] <= 396 and event.pos[1] >= 160 and event.pos[1] <= 256:
					pygame.quit()
					Next_menu = choix_circuit()
					attente = False

				#BOUTON TRAIN
				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 208 and event.pos[0] <= 420 and event.pos[1] >= 295 and event.pos[1] <= 385:
					pygame.quit()
					Train = choix_train()			
					attente = False


					
			#BOUTONS
			demarez = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))
			ecran_menu.blit(text, (240,165))

			train = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))#200 270 200 100
			ecran_menu.blit(text_train, (210,300))



			#ANIMATION TITRE
			pygame.display.flip()
			cp += 1
			if cp%20 == 0:
				rouge = not(rouge)

			if rouge:
				ecran_menu.blit(titreRouge,(100,25))
			else:
				ecran_menu.blit(titreVert,(100,25))

			
		pygame.quit()

Main = Menu()






