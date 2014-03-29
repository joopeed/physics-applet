# -*- coding: utf-8 -*-
"""

Development by
João Pedro Ferreira de Melo Leôncio
Gustavo Henrique Queiroz
Franco Stefano Baroni

"""

import sys, pygame, random, os, urllib
from time import *
pygame.init()
 
size = wid, hei = 990, 590 # size obviously ## pensei em aumentar o tamanho!!
back = 132, 122, 130 # background color RGB
screen = pygame.display 
screen.set_caption("Applet de Fisica")
screen = pygame.display.set_mode(size)
pygame.display.set_mode(size)
pygame.key.set_repeat(140,80)

from sys import stdout
from pygame.locals import *
#import pygame.scrap as scrap  
#import popen2
#scrap.init()
#scrap.set_mode(SCRAP_CLIPBOARD)
# Buffer musics
#pygame.mixer.music.load("musics/quebranozes.mp3") tem de ser uma musiquinha de tensão

# End of buffer musics


# Fonts
pygame.font.init()
font_big = pygame.font.Font(None, 35)
font_medium = pygame.font.Font(None, 22)
font_small = pygame.font.Font(None, 15)
# End Fonts

# Buffer image
images = {}
#images["pharight"] = pygame.image.load("monstrinhoright.png").convert_alpha()
#images["phaleft"] = pygame.image.load("monstrinholeft.png").convert_alpha()
#images["phadown"] = pygame.image.load("monstrinhodown.png").convert_alpha()
#images["phaup"] = pygame.image.load("monstrinhoup.png").convert_alpha()
# End of buffer image


# Set the mouse visibility
#pygame.mouse.set_visible(False)

BRANCO = (255, 255, 255)
AZUL = (32, 0, 138)
VERMELHO = (138, 0, 0)
POSICAO_OLHO = (400, 500)

""" Functions here"""

def GetPosition(board):
	"""
	Get the position of X in the matrix
	"""
	for i in range(len(board.matrix)):
		for j in range(len(board.matrix[i])):
			if board.matrix[i][j]=="X":
				return i,j

""" END of Functions """
""" Classes here """
class Reta:
        def __init__(self, position_initial, length, color):
                self.x, self.y = position_initial
                self.color = color
                self.length = length
                self.azul = False
                self.vermelha = False

        def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length, self.y), 3)

        def move_right(self):
                self.x += 1
        def move_left(self):
                self.x -= 1
                
        def exibe_reta_azul(self, retas):
            if not self.azul:
                retas.append(RetaDeExibicao((self.x, self.y - 5), self.length, AZUL))
                self.azul = True
        def exibe_reta_vermelha(self, retas):
            if not self.vermelha:
                retas.append(RetaDeExibicao((self.x, self.y - 5), self.length, VERMELHO))
                self.vermelha = True

class RetaDeExibicao(Reta):
    def __init__(self, position_initial, length, color):
        Reta.__init__(self, position_initial, length, color)

    def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length, self.y), 2)
                quantidade_de_tracos = 4
                tamanho_gap = self.length/quantidade_de_tracos
                for i in range(self.x, self.x + self.length + tamanho_gap, tamanho_gap):
                    pygame.draw.line(screen, self.color, (i, self.y), POSICAO_OLHO, 1)



	
""" END of Classes """

reta_principal = Reta((25, 25), 80, BRANCO)
retas = [reta_principal]
run = 0
velocidade = 1

while True:
	#os.system("clear")	
	"""
	Main loop :) 
	"""

        velocidade += 0.1
	
	reta_principal.move_right()
	
	# Background #
	pygame.display.flip()	
	screen.fill(back)

	#EXIT MODES
	if pygame.event.peek(pygame.QUIT): break
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
        # Press ESC and get out of here
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit()                                   
	
	
	#if pygame.key.get_pressed()[pygame.K_SPACE]:
	for reta in retas:
            reta.draw(screen)

        if reta_principal.x > 300:
            reta_principal.exibe_reta_azul(retas)
        if reta_principal.x > 500:
            reta_principal.exibe_reta_vermelha(retas)
	
	#for line in tab.matrix:
		#print line	
	
	
	
	
	# (56,16,230) cor legal pra o outro person
		
	mouse = pygame.mouse.get_pos()
	
	text = font_big.render(u'Execute!'.decode("utf8"), True,(255,255, 255))
	
	botao = pygame.Rect(850, 520, 120, 50)
	pygame.draw.rect(screen, (56,16,30), botao, 0)
	screen.blit(text, (860,530))
	
	
	
	if run:
		run-=1
		
	
