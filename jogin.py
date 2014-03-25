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
screen.set_caption("Txu ru ru")
screen = pygame.display.set_mode(size)
pygame.display.set_mode(size)
pygame.key.set_repeat(140,80)

from sys import stdout
from pygame.locals import *
import pygame.scrap as scrap  
import popen2
scrap.init()
scrap.set_mode(SCRAP_CLIPBOARD)
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
images["pharight"] = pygame.image.load("monstrinhoright.png").convert_alpha()
images["phaleft"] = pygame.image.load("monstrinholeft.png").convert_alpha()
images["phadown"] = pygame.image.load("monstrinhodown.png").convert_alpha()
images["phaup"] = pygame.image.load("monstrinhoup.png").convert_alpha()
# End of buffer image


# Set the mouse visibility
#pygame.mouse.set_visible(False)



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








class Form(pygame.Rect,object):
	
    def __init__(self,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),curscolor=(0xff0000),maxlines=0):
        if not font: self.FONT = pygame.font.Font(pygame.font.match_font('mono',1),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = font
        self.BG = bg
        self.FGCOLOR = fgcolor
        self.HLCOLOR = hlcolor
        self.CURSCOLOR = curscolor
        self._line = 0
        self._index = 0
        self.MAXLINES = maxlines
        self._splitted = ['']
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self.TAB = 4
        self._adjust()
        self._cursor = True

    @property   
    def CURSOR(self):
        return self._cursor
    @CURSOR.setter
    def CURSOR(self,value):
        self._cursor = value
    
    @property
    def HLCOLOR(self):
        return None
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)
    
    @property
    def OUTPUT(self):
        return '\n'.join(self._splitted)
    @OUTPUT.setter
    def OUTPUT(self,string):
        self._splitted = string.split('\n')
    
    @property
    def FONT(self):
        return self._font
    @FONT.setter
    def FONT(self,font):
        self._font = font
        self._w,self._h = self._font.size(' ')
    
    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i) for i in self._splitted[:p2[0]]]
            return self.OUTPUT[sum(selection[:p1[0]]) + p1[0] + p1[1]:sum(selection) + p2[0] + p2[1]:]
        return ''
                
    def _adjust(self):
        if self._index < len(self._splitted[self._line]):
            rcurs = pygame.Rect(self._x+self._index*self._w,self._y+self._line*self._h,self._w,self._h)
        else:
            rcurs = pygame.Rect(self._x+len(self._splitted[self._line])*self._w,self._y+self._line*self._h,1,self._h)
        
        self._rcursor = rcurs.clamp(self)
        self._x += self._rcursor.x - rcurs.x
        self._y += self._rcursor.y - rcurs.y
    
    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)
        
        start = (self.top - self._y) / self._h
        end = (self.bottom - self._y) / self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x+5,y+5))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x+5,y+5))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x+5,y+5))
                x += self._w
            y += self._h
        if self._cursor:
            pygame.draw.line(self._src,self.CURSCOLOR,(self._rcursor.topleft[0]+5, self._rcursor.topleft[1]+5),(self._rcursor.bottomleft[0]+5, self._rcursor.bottomleft[1]+5),1)
        self._src.set_clip(clip)
    
    def show(self):
        self.screen()
        pygame.display.update(self)
        
    def wakeup(self,ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: pyca.focus(self)
        self.update(ev)
            
    def update(self,ev):
        
        line,index = self._line,self._index
        shift = pygame.key.get_pressed()
        shift = shift[pygame.K_RSHIFT]|shift[pygame.K_LSHIFT]
        ctrl = pygame.key.get_pressed()
        ctrl = ctrl[pygame.K_RCTRL]|ctrl[pygame.K_LCTRL]

        def clear():
            p1,p2 = sorted(((self._line,self._index),self._select))
            if p1 != p2:
                selection = [len(i) for i in self._splitted[:p2[0]]]
                self.OUTPUT = self.OUTPUT[:sum(selection[:p1[0]]) + p1[0] + p1[1]] + self.OUTPUT[sum(selection[:p2[0]]) + p2[0] + p2[1]:]
                self._select = self._line,self._index = p1

     

        
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                if self._index < len(self._splitted[self._line]):
                    self._index += 1
                elif self._line < len(self._splitted)-1:
                    self._index = 0
                    self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_LEFT:
                if self._index > len(self._splitted[self._line]):
                    self._index = len(self._splitted[self._line])
                if self._index:
                    self._index -= 1
                elif self._line:
                    self._line -= 1
                    self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
            
            elif ev.key == pygame.K_UP:
                if self._line: self._line -= 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DOWN:
                if self._line < len(self._splitted)-1: self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DELETE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]):
                        self._index = len(self._splitted[self._line])
                        self._select = self._line + 1,0
                    else:
                        self._select = self._line,self._index + 1
                clear()
                
            elif ev.key == pygame.K_END:
                self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_HOME:
                self._index = 0
                if not pygame.mouse.get_pressed()[0] and not shift and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_BACKSPACE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                    if self._index == 0:
                        if self._line: self._select = self._line - 1,len(self._splitted[self._line - 1])
                    else: self._select = self._line,self._index - 1
                clear()

            elif ev.key == pygame.K_TAB:
                clear()
                sp = self.TAB-self._index%self.TAB
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ' '*sp + self._splitted[self._line][self._index:]
                self._index += sp
                self._select = self._line,self._index

            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER or ev.unicode == '\n':
                clear()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + '\n' + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._line += 1
                    self._index = 0
                    self._select = self._line,self._index
            elif ctrl and ev.key == pygame.K_v:
            	types = pygame.scrap.get_types()
    		for t in range(len(types)):
      			if "TEXT" in types[t]:
      	 			index = t
          	for i in range(len(scrap.get(types[index]).split("\n"))):
          		clear()
          		self._splitted[self._line] = self._splitted[self._line][:self._index] + scrap.get(types[index]).split("\n")[i] + "\n" + self._splitted[self._line][self._index:]
   			self.OUTPUT = self.OUTPUT
   			self._line += 1 
   			self._index = 0
            	self._index += len(scrap.get(types[index]).split("\n")[-1])
            	self._select = self._line,self._index
            elif ctrl and ev.key == pygame.K_c:
    		pygame.scrap.put (SCRAP_TEXT, self.SELECTION)
            elif ctrl and ev.key == pygame.K_a:
		self._line = 0
		self._index = 0
		self._select = (len(self._splitted)-1,len(self._splitted[len(self._splitted)-1]))
		
            elif ev.unicode:
                clear()
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ev.unicode + self._splitted[self._line][self._index:]
                self._index += 1
                self._select = self._line,self._index
                
        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button < 3:
                self._line = (ev.pos[1] - self._y) / self._h
                self._index = (ev.pos[0] - self._x) / self._w
                if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line])
                if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                if ev.button == 2:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + self.SELECTION + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._index += len(self.SELECTION)
                
                self._select = self._line,self._index
                
            
            elif ev.button == 4:
                y = self._y
                if self._y + self._h*3 > self.top: self._y = self.top
                else: self._y += self._h*3
                self._rcursor.move_ip(0,self._y-y)
                return
                
            elif ev.button == 5:
                y = self._y
                h = len(self._splitted) * self._h
                if h > self.height:
                    if self._y - self._h*3 < self.bottom - h: self._y = self.bottom - h
                    else: self._y -= self._h*3
                    self._rcursor.move_ip(0,self._y-y)
                return
        
        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) / self._h
            self._index = (ev.pos[0] - self._x) / self._w
            if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line])
            if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])

        if (line,index) != (self._line,self._index):
            self._adjust()



























class Board:
	"""
	Class to set board
	Gets Size of squares, How many squares horizontally and How many squares vertically
	"""
	def __init__(self, size_of_squares, x_many, y_many, radius):
                self.squares = [[ pygame.Rect(5+(size_of_squares-1)*i+i,5+ (size_of_squares-1)*j+j, (size_of_squares-1), (size_of_squares-1)) for i in range(x_many)] for j in range(y_many)]
		self.matrix = [[" "]*x_many for i in range(y_many)]
		self.matrix[0][0] = "X" # Initial position
		self.radius = radius
		
		
	def draw(self, screen, x_position, y_position):
		for i in range(len(self.squares)):
	                  for j in range(len(self.squares[i])):
	                           if i in range(x_position-self.radius,x_position+self.radius+1) and j in range(y_position-self.radius,y_position+self.radius+1):
	                                    if (i,j) == (x_position,y_position):
	                                    	pygame.draw.rect(screen, (205,10,10), self.squares[i][j], 0) # at point
	                                    else:
	                                    	pygame.draw.rect(screen, (205,205,205), self.squares[i][j], 0) # Color inside radius	
	                           else:
	                                    pygame.draw.rect(screen, (235,235,235), self.squares[i][j], 0) # Color outside radius
	                                                   
	                           
		
	
	
	
class Person:
	""" 
	Class to create persons
	"""
	def __init__(self, size, position_initial, color):
		self.x, self.y = position_initial
		self.size = size
		self.color = color
		self.rot = {"right":0,"left":0,"down":0,"up":0 } 
		self.image = images["pharight"]
	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))
		#baku = pygame.Rect(self.x, self.y, 25, 25)
		#pygame.draw.rect(screen, self.color, baku, 0)
	def move_right(self):
		if self.rot["right"]:
			self.x+=1
		else:
			self.rot["right"] = 50
		self.image = images["pharight"]
	def move_left(self):
		if self.rot["left"]:
			self.x-=1
		else:
			self.rot["left"] = 50
		self.image = images["phaleft"]
	def move_up(self):
		if self.rot["up"]:
			self.y-=1
		else:
			self.rot["up"] = 50
		self.image = images["phaup"]
	def move_down(self):
		if self.rot["down"]:
			self.y+=1
		else:
			self.rot["down"] = 50
		self.image = images["phadown"]
	
""" END of Classes """


tab = Board(49, 20, 10, 2)
players = []
player_one = Person(32, (6+5,11+5), (150,40,0))

txt = Form((5,500),830,fontsize=13,height=86,bg=(230,230,230),fgcolor=(100,50,100),hlcolor=(250,190,150,100),curscolor=(190,0,10))
txt.OUTPUT = unicode("""player_one.move_right()""","utf8")
#txt.show()
player_id = 0
turn = 1 # start from 1
flow = [{"t":0,"j":1,"c":"player_one.move_right()","s":0}] # The atributes are, respectivily, turn, player, command and status (executed or not). 
run = 0
while True:
	#os.system("clear")	
	"""
	Main loop :) 
	"""
	# Background #
	pygame.display.flip()	
	screen.fill(back)	
	# Background #
	evs = pygame.event.get()
	if pygame.event.peek(pygame.QUIT): break
       	if evs:
            for ev in evs:
                txt.update(ev)
	
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
         # Press ESC and get out of here
	if pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit()                                   
	
	
	#xlocal,ylocal = ymouse/50, xmouse/50
	
	#if pygame.key.get_pressed()[pygame.K_SPACE]:
	tab.draw(screen, (player_one.y+int(player_one.size/2.))/50, (player_one.x+int(player_one.size/2.))/50)
	player_one.draw(screen)
	
	
	
	#for line in tab.matrix:
		#print line	
	
	tab.matrix[(player_one.y+int(player_one.size/2.))/50][ (player_one.x+int(player_one.size/2.))/50] = "X"
	
	if player_one.rot["right"]:
		player_one.move_right()
		player_one.rot["right"]-=1
	if player_one.rot["left"]:
		player_one.move_left()
		player_one.rot["left"]-=1
	if player_one.rot["down"]:
		player_one.move_down()
		player_one.rot["down"]-=1
	if player_one.rot["up"]:
		player_one.move_up()
		player_one.rot["up"]-=1
	
	
	# (56,16,230) cor legal pra o outro person
	txt.show()	
	mouse = pygame.mouse.get_pos()
	
	text = font_big.render(u'Execute!'.decode("utf8"), True,(255,255, 255))
	
	botao = pygame.Rect(850, 520, 120, 50)
	pygame.draw.rect(screen, (56,16,30), botao, 0)
	screen.blit(text, (860,530))
	
	if botao.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
		#try:
		 i =0
		 linhas = txt.OUTPUT.split("\n")
		 while i < len(linhas):
		         linex = i
		         for j in range(i, len(linhas)):
				if linhas[j][0]==" ":
					linex = j
				elif j!=i:
					break
		         com = "\n".join(linhas[i:linex+1])
		         flow.append({"t":turn,"j": player_id,"c": com ,"s":0 })
		         i+= len(linhas[i:linex+1])
		#except: txt.OUTPUT = "This can't be executed, seu jumento!"
		 sleep(1)
	
	for command in flow:
		if command["t"]==turn and command["s"]==0 and not run:
			try:
				exec(command["c"])
			except:txt.OUTPUT = "This line has an error and couldn't be executed.\n>>> "+command["c"]
			command["s"]=1
			run = 50	
			break
	
	if run:
		run-=1
		
	#TODO make the exec works with multiline instructions, like for's, while's ...	
	#TODO put a second player	
		
		
		
		
		
	# Bliting text >>>
	#text = font_big.render(u'Example!'.decode("utf8"), True,(255,255, 255))
	#screen.blit(text, POSITION)
	# Bliting Images >>>
	#screen.blit(images["nameofimage"], POSITION)
	
	# Get mouse position		
	#mouse = pygame.mouse.get_pos()
