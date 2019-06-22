# Mama mIA aka MarIA Kart
# Sous-menu (2/2): gestion de partie

# Gaspard Lauras - Thibaud Le Du
# Luc Meunier - Thibault Dos Santos - Lilian De Conti - Jérôme Kacimi

# Choix de la partie entre les deux circuits

import pygame
from Game import Principale

##################################################
# Classe menu du choix de circuit pour jouer

class choix_circuit:

	def __init__(self):


		pygame.init()
		pygame.font.init()

		width = 600
		heigth = 400

		ecran_menu = pygame.display.set_mode((width,heigth))
		ecran_menu.fill((0,0,0))

		#TEXTS
		text = pygame.font.SysFont("comicsansms",30,True,False)


		titre_circuit11 = text.render("EASY",True,(0,0,0),(150,150,150))
		titre_Sircuibo = text.render("HARDCORE",True,(0,0,0),(150,150,150))

		#IMAGE
		x = 250
		y = int(0.6*x)

		image_Circuit11 = pygame.transform.scale(pygame.image.load("CIRCUIT11.png"),(x,y))
		image_Sircuibo = pygame.transform.scale(pygame.image.load("Sircuibo.png"),(x,y))


		pygame.display.flip()

		attente = True
		C_red = True
		cp = 0

		while attente:

			#ANIMATION
			cp += 1
			if cp%20 == 0:
				C_red = not(C_red)

			if C_red:
				color = (255,0,0)
			else:
				color = (0,255,0)


			#ACTIONS (QUIT OU CLIQUE)
			for event in pygame.event.get():
				if event.type == pygame.QUIT :
					attente = False


				key = pygame.key.get_pressed()

				if key[pygame.K_ESCAPE]:
					attente =False

				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 50 and event.pos[0] <= 250 and event.pos[1] >= 300 and event.pos[1] <= 350:
					pygame.quit()
					Joueur_Circuit11 = Principale("CIRCUIT11.png")

				if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] >= 350 and event.pos[0] <= 550 and event.pos[1] >= 300 and event.pos[1] <= 350:
					pygame.quit()
					Joueur_Sircuibo = Principale("Sircuibo.png")




			#BOUTONS
			CIRCUIT11 = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))
			ecran_menu.blit(titre_circuit11, (80,315))

			Sircuibo = pygame.draw.rect(ecran_menu,(150,150,150),(0,0,0,0))
			ecran_menu.blit(titre_Sircuibo, (380,315))

			

			#IMAGES
			pygame.draw.rect(ecran_menu, color, (20,95,x+10,y+10),10)
			pygame.draw.rect(ecran_menu, color, (320,95,x+10,y+10),10)
			pygame.draw.rect(ecran_menu, color, (620,95,x+10,y+10),10)

			ecran_menu.blit(image_Circuit11,(25,100))
			ecran_menu.blit(image_Sircuibo,(325,100))
			

			pygame.display.flip()




		pygame.quit()



