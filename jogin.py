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
 
size = wid, hei = 990, 590 # size obviously
back = 255, 255, 255 # background color RGB
screen = pygame.display 
screen.set_caption("Applet de Contracao de Comprimento")
screen = pygame.display.set_mode(size)
pygame.display.set_mode(size)
pygame.key.set_repeat(140,80)

from sys import stdout
from pygame.locals import *

# End of buffer musics


# Fonts
pygame.font.init()
calibri = pygame.font.SysFont("calibri", 32)
calibri_small = pygame.font.SysFont("calibri", 18)
#font_big = pygame.font.Font(None, 35)
font_medium = pygame.font.SysFont("calibri", 18)
#font_small = pygame.font.Font(None, 15)
# End Fonts

# Buffer image
images = {}
images["box_shadow"] = pygame.image.load("sombra_detalhes.png").convert_alpha()
images["eye"] = pygame.image.load("eye.png").convert_alpha()
images["blur"] = pygame.image.load("blur.png").convert_alpha()
images["sobre"] = pygame.image.load("sobre.png").convert_alpha()
images["shadow"] = pygame.image.load("shadow.png").convert_alpha()
# End of buffer image


# Set the mouse visibility
#pygame.mouse.set_visible(False)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (32, 0, 138)
VERMELHO = (138, 0, 0)
POSICAO_OLHO = (411, 433)
CINZA = (132, 122, 130)

""" Functions here"""
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
		self.length_relative = length

        def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length_relative, self.y), 3)
	
	def atualiza_velocidade(self, valor):
                self.velocidade = valor

        def move_right(self, velocidade):
                
		if self.x > 500:
			self.x += 1 * 4
			self.length_relative = self.length * math.sqrt( 1 - (velocidade)**2 )
		elif self.x > 200:
			self.x += 1 * 3
			#print self.length, self.length * (math.sqrt( 1 - (velocidade)**2 * ((self.x-200)/300.0)) )  , ((self.x-300)/200.0)
			self.length_relative = self.length * (math.sqrt( 1 - (velocidade)**2 * ((self.x-200)/300.0)) ) 
		else:
			self.x += 1
			
        def move_left(self):
                self.x -= 1 * int(math.ceil(self.velocidade))
                
        def exibe_reta_azul(self, retas):
            if not self.azul:
                tamanho_real = self.length
                retas.append(RetaDeExibicao((self.x, self.y), tamanho_real, AZUL))
                self.azul = True
        def exibe_reta_vermelha(self, retas, velocidade_atual):
            if not self.vermelha:
                tamanho_relativo = self.length_relative
                retas.append(RetaDeExibicao((self.x, self.y), tamanho_relativo, VERMELHO))
                self.vermelha = True

class RetaDeExibicao(Reta):
    def __init__(self, position_initial, length, color):
        Reta.__init__(self, position_initial, length, color)

    def draw(self, screen):
                pygame.draw.line(screen, self.color, (self.x, self.y), (self.x + self.length, self.y), 2)
                quantidade_de_tracos = 4
                tamanho_gap = int(self.length)/(quantidade_de_tracos - 1)
                adicional = 0 if (quantidade_de_tracos - 1) % 2 != 0 else tamanho_gap
                for i in range(self.x, int(math.ceil(self.x + self.length + adicional +1)), tamanho_gap):
                    pygame.draw.line(screen, self.color, (i, self.y), POSICAO_OLHO, 1)


class Botao:
    def __init__(self, nome, position):
        self.nome = nome
        self.x, self.y = position
        self.botao = pygame.Rect(self.x, self.y, 120, 50)
        self.apertado = False

    def draw(self, screen):
        text = calibri.render(self.nome.decode("utf8"), True,(255,255, 255))
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
tamanho_reta = 150
reta_principal = Reta((-100, 25), tamanho_reta, PRETO)
retas = [reta_principal]
def reset():
	global reta_principal
	reta_principal = Reta((-100, 25), tamanho_reta, PRETO)
	global retas
	retas = [reta_principal]
def abre_sobre():
        #while True:
                screen.blit(images["blur"], (0, 0))
                screen.blit(images["sobre"], (0, -80))
                #pygame.event.wait()
			             

botao = Botao("Iniciar", (480, 515))
sobre = Botao("Sobre", (630, 515))
regulador = Regulador((20, 530), 0.5, 0.9, 0.5)
barra_baixo = Rect(0, 485, 990, 115)
velocidade_escolhida = 0.5
exibe = True

while True:
	#os.system("clear")	
	"""
	Main loop :) 
	"""
	if exibe:
                calibri_small.set_bold(True)
                text = calibri_small.render(("Experimento de Contração de Comprimento").decode("utf8"), True,PRETO)
                screen.blit(text, (600, 440))
                calibri_small.set_bold(False)
                text = calibri_small.render(("Comprimento Inicial: %.1f m" % reta_principal.length).decode("utf8"), True,(255,255, 255))
                screen.blit(text, (10, 400))
                text = calibri_small.render(("Comprimento Atual: %.1f m" % reta_principal.length_relative).decode("utf8"), True,(255,255, 255))
                screen.blit(text, (10, 420))
                text = calibri_small.render(("Velocidade atingida: %.2fc" % velocidade_escolhida).decode("utf8"), True,(255,255, 255))
                screen.blit(text, (10, 440))
	# Background #
	pygame.display.flip()	
	screen.fill(back)
	screen.blit(images["eye"], (380, 400))
	
        #pygame.draw.rect(screen, CINZA, barra_baixo)
        screen.blit(images["box_shadow"], (-50, 350))
	#EXIT MODES
	if pygame.event.peek(pygame.QUIT): break
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
        # Press ESC and get out of here
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit()                                   
	
	if botao.apertou() and not regulador.mexendo:
		reset()
		velocidade_escolhida = regulador.valor_atual
		botao.desapertou()
	
                
        reta_principal.velocidade = 1 + velocidade_escolhida
        reta_principal.move_right(velocidade_escolhida)
        for reta in retas:
            reta.draw(screen)

	
        if reta_principal.x > 100:
            reta_principal.exibe_reta_azul(retas)
        if reta_principal.x > 700:
            reta_principal.exibe_reta_vermelha(retas, velocidade_escolhida)
	
	botao.draw(screen)
	sobre.draw(screen)
	regulador.draw(screen)
	regulador.apertou()
	if sobre.apertou() and not regulador.mexendo:
                abre_sobre()
                exibe = False
	
	
	
