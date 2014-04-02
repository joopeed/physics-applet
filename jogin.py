# -*- coding: utf-8 -*-
"""

Development by
João Pedro Ferreira de Melo Leôncio
Leticia Farias Wanderley
Maysa Macedo
Fellype Cavalcante
Ana Luiza Motta Gomes

"""

import sys, pygame, random, os, urllib, math
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
images["eye"] = pygame.image.load("eye.png").convert_alpha()
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
POSICAO_OLHO = (411, 433)

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
		self.velocidade = 0.5

        def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length, self.y), 3)

        def move_right(self):
                self.x += 1 * int(math.ceil(self.velocidade))
        def move_left(self):
                self.x -= 1 * int(math.ceil(self.velocidade))
                
        def exibe_reta_azul(self, retas):
            if not self.azul:
                retas.append(RetaDeExibicao((self.x, self.y), self.length, AZUL))
                self.azul = True
        def exibe_reta_vermelha(self, retas):
            if not self.vermelha:
                retas.append(RetaDeExibicao((self.x, self.y), self.length, VERMELHO))
                self.vermelha = True

class RetaDeExibicao(Reta):
    def __init__(self, position_initial, length, color):
        Reta.__init__(self, position_initial, length, color)

    def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length, self.y), 2)
                quantidade_de_tracos = 4
                tamanho_gap = self.length/(quantidade_de_tracos - 1)
                adicional = 0 if (quantidade_de_tracos - 1) % 2 != 0 else tamanho_gap
                for i in range(self.x, self.x + self.length + adicional, tamanho_gap):
                    pygame.draw.line(screen, self.color, (i, self.y), POSICAO_OLHO, 1)


class Botao:
    def __init__(self, nome, position):
        self.nome = nome
        self.x, self.y = position
        self.botao = pygame.Rect(self.x, self.y, 120, 50)
        self.apertado = False

    def draw(self, screen):
        text = font_big.render(self.nome.decode("utf8"), True,(255,255, 255))
	pygame.draw.rect(screen, (56,16,30), self.botao, 0)
	screen.blit(text, (self.x + 20, self.y + 10))

    def apertou(self):
        if not self.apertado:
            self.apertado = self.botao.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
        return self.apertado
    
    def desapertou(self):
	self.apertado = False


class Regulador:
    def __init__(self, position, inicio, fim, inicial):
        self.x, self.y = position
        self.inicio = inicio
        self.fim = fim
        self.valor_atual = inicial
        self.mexendo = False


    def draw(self, screen):
        sub_parte = 4
        inicio = int(self.inicio*100)
        fim = int(self.fim*100)
        atual = int(self.valor_atual*100)
        porcentagem = (100.0 / (fim-inicio)) * (atual - inicio)
        barra = Rect(self.x, self.y, 400, 20)
        pygame.draw.rect(screen, BRANCO, barra)
        local = Rect(self.x + porcentagem * sub_parte , self.y - 10, 10, 40)
        pygame.draw.rect(screen, AZUL, local)
	text = font_medium.render(("%.2fc" % self.valor_atual).decode("utf8"), True,(255,255, 255))
	screen.blit(text, (self.x + porcentagem * sub_parte -10, self.y + 30))
        
    def apertou(self):
        sub_parte = 4
        inicio = int(self.inicio*100)
        fim = int(self.fim*100)
        atual = int(self.valor_atual*100)
        porcentagem = (100.0 / (fim-inicio)) * (atual - inicio)
        local = Rect(self.x + porcentagem * sub_parte , self.y - 10, 10, 40)
        if pygame.mouse.get_pressed()[0] and local.collidepoint(pygame.mouse.get_pos()):
            self.mexendo = True
        if self.mexendo:
            if not pygame.mouse.get_pressed()[0]: self.mexendo = False
            porcentagem_atual = (pygame.mouse.get_pos()[0] - self.x) / sub_parte
            print self.valor_atual
            if self.inicio <= self.inicio + (self.fim - self.inicio) * porcentagem_atual/100. <= self.fim:
                self.valor_atual = self.inicio + (self.fim - self.inicio) * porcentagem_atual/100. 
        

    

	
""" END of Classes """
reta_principal = Reta((-100, 25), 80, BRANCO)
retas = [reta_principal]
def reset():
	global reta_principal
	reta_principal = Reta((-100, 25), 80, BRANCO)
	global retas
	retas = [reta_principal]
botao = Botao("Iniciar", (600, 515))
regulador = Regulador((100, 530), 0.1, 0.9, 0.5)
while True:
	#os.system("clear")	
	"""
	Main loop :) 
	"""

	
	if reta_principal.x > 400:
		reta_principal.velocidade = 1 + regulador.valor_atual

	
	
	# Background #
	pygame.display.flip()	
	screen.fill(back)
	screen.blit(images["eye"], (380, 400)) 
	#EXIT MODES
	if pygame.event.peek(pygame.QUIT): break
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
        # Press ESC and get out of here
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit()                                   
	
	if botao.apertou():
		reset()
		botao.desapertou()
        reta_principal.move_right()
        for reta in retas:
            reta.draw(screen)

	
        if reta_principal.x > 100:
            reta_principal.exibe_reta_azul(retas)
        if reta_principal.x > 700:
            reta_principal.exibe_reta_vermelha(retas)
	
	botao.draw(screen)
	regulador.draw(screen)
	regulador.apertou()
	
	
	
