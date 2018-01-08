import pygame
pygame.init()
import math
import random
import classes 
from classes import *

width = 1280
height = 1024



    #Variable Colors

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0,0,255)
yellow = (140, 0,140)

#font setup

pygame.font.init()
myfont = pygame.font.Font('Sprites/Font/Arcade.ttf', 60)

#Screen setup
#line = 0

'''Level = []
value = 0
blockvalue = 0
linenumber = 0
levelname = True'''

screen = pygame.display.set_mode((width,height))
screen_rect=screen.get_rect()
pygame.display.set_caption('Level reader')
clock = pygame.time.Clock()

background = pygame.image.load('Sprites/Extra/Background.png').convert()

#everything = pygame.sprite.Group()

'''floor = Floor()
wall = Wall(0) #left wall
wall = Wall(1275) #right wall'''



def readlines(file):
    lines = []
    with open(file, 'r') as lines:
        lines = lines.read()
        lines = [line.rstrip('\n') for line in open(file)]
        return lines

playercords = [[0,0],[0,0]]
movingblockcounter = 0
'''class parent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xcord = 0
        self.ycord = 0
        self.xspeed = 0 #horizontal speed
        self.yspeed = 0 #vertical speed
        everything.add(self)

class Block(parent):
    def __init__(self, row, colum, xsize, ysize, color):
        super().__init__()
        self.row = row
        self.xsize = xsize
        self.ysize = ysize
        self.colum = colum
        self.image = pygame.Surface([40 * xsize,40 * ysize])
        self.image.fill(green)
        self.rect = self.image.get_rect()

    def update(self):

        self.xcord = self.colum * 40
        self.ycord = self.row * 40 

        self.rect.y = self.ycord
        self.rect.x = self.xcord'''

def spawnlevel(Level, linenumber, blockvalue, lines):
    movingblockcounter = 0
    for y in range(21):
        value = lines[y + 1 + (linenumber * 22)]
        for x in range(32):
            if value[x] == "6":
                print(x)
                while value[x + 1] == "b":
                    x += 1
                    movingblockcounter += 1
                    
                x = x - movingblockcounter
                block = Block(x * 40,y * 40, movingblockcounter * 40, False)
                movingblockcounter = 0
            else:     
                blockvalue = value[x]
                spawnitems(y,x,blockvalue)
            

def spawnitems(y,x, typ):

    y = y * 40
    x = x * 40
    if typ == '1':#player
        if len(players) < 1:
            playercords[0][0] = x
            playercords[0][1] = y
            #player = Player(x,y)
            #print("done")
        else:
            playercords[1][0] = x
            playercords[1][1] = y
            #player2 = Player2(x,y)
            #print("k")
    elif typ == '2':#ladder
        ladder = Ladder(x,y)   #ladder
    elif typ == '3':                                                            #Static platform
        block = Block(x,y,0,False)
    elif typ == '4':                                                            #Breakable platform
        block = Block(x,y,0,False)    #Wall                                          
    elif typ == '5':                                                            #vertical wall
        block = Block(x,y,0,True) #Breakable                                           
    elif typ == '7':                                                            #small slime
        ball = Ball(4,x,y, True)
    elif typ == '8':                                                            #medium slime
        ball = Ball(2,x,y, True)
    elif typ == '9':                                                            #Big slime
        ball = Ball(1,x,y, True)


def levelreader(file, level):
    lines = readlines(file)
    xline = int(len(lines) / 22)
    run = 1
    line = 0
    Level = []
    value = 0
    linenumber = 0
    
    blockvalue = 0
    levelname = True

    if file == "Campaign.txt":
        spawnlevel(Level, level, blockvalue, lines)
        levelname = False
        run = 0
        
    
    while run == 1: 
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(Level)
                    spawnlevel(Level, linenumber, blockvalue, lines)
                    levelname = False
                    run = 0
                elif event.key == pygame.K_UP:
                    linenumber += 1
                elif event.key == pygame.K_DOWN:
                    linenumber -= 1
                elif event.key == pygame.K_ESCAPE:
                    run = 0

        if linenumber >= xline:
            linenumber = 0
        elif linenumber < 0:
            linenumber = xline - 1

        if levelname == True:

        
            name0 = myfont.render( lines[((linenumber - 2) % xline) * 22], False, black)
            name1 = myfont.render( lines[((linenumber - 1) % xline) * 22], False, black)
            name2 = myfont.render( lines[((linenumber - 0) % xline) * 22], False, green)
            name3 = myfont.render( lines[((linenumber + 1) % xline) * 22], False, black)
            name4 = myfont.render( lines[((linenumber + 2) % xline) * 22], False, black)



                  

        print(xline)

        everything.update()
      
        screen.blit(background,(0,0))
        
        everything.draw(screen)

        if levelname == True:
            screen.blit(name0, (500, 100))
            screen.blit(name1, (500, 200))
            screen.blit(name2, (500, 300))
            screen.blit(name3, (500, 400))
            screen.blit(name4, (500, 500))



        pygame.display.flip()

        clock.tick(60)

    
    return playercords
