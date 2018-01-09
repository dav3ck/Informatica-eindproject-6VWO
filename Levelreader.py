import pygame
pygame.init()
import math
import random
import classes 
from classes import *

width = 1280
height = 1024

#Dit script laat het Level in !!!

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



def readlines(file): #Dit leest de .txt file, en stops daarvan alle regels in de lines array
    lines = []
    with open(file, 'r') as lines:
        lines = lines.read()
        lines = [line.rstrip('\n') for line in open(file)]
        return lines

playercords = [[0,0],[0,0]] #coordinate waar player gespawned moet worden
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
    def __init__(self, row, colum, xsize, ysize, color): #DEZE CLASS IS VERHUISD NAAR classes.py FILE
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

def spawnlevel(Level, linenumber, blockvalue, lines): #Deze functie haalt de array cijfer voor cijfer uit elkaar, en stuurd deze gegevens door om verwerkt te worden -> blokken ingespawned
    movingblockcounter = 0 #Moving blockcounter word gereset 
    for y in range(21): #uit de y en de x Kun je weer de row/colum bepalen voor de locatie van inspawnen
        value = lines[y + 1 + (linenumber * 22)]
        for x in range(32):
            if value[x] == "6": #als de waarde 6 is:
                while value[x + 1] == "b": #zolang er hierna nog een b komt moet movingblockcounter met 1 verhoogd worden
                    x += 1
                    movingblockcounter += 1
                x = x - movingblockcounter #hier word de x weer terug gebracht naar originele staat.
                block = Block(x * 40,y * 40, movingblockcounter * 40, False, "Sprites/Blocks/Block1.png") #Hier word het blok ingespawned, de movingblockcoutner * 40 is de afstand die het blok moet gaan afleggen. False is of het breakable is of niet
                movingblockcounter = 0
            else:     #als de waarde niet 6 is gebeurd het zoals normaal
                blockvalue = value[x] #waarde uit de array bij getal x word opgeslagen in blockvalue
                spawnitems(y,x,blockvalue) #item word gespawned
            

def spawnitems(y,x, typ): #hier word de blockvalue vergelijken met alle andere waardes, en zo het toepasselijke object ingespawned.

    y = y * 40
    x = x * 40
    if typ == '1':#player
        if len(players) < 1:
            playercords[0][0] = x
            playercords[0][1] = y
        else:
            playercords[1][0] = x
            playercords[1][1] = y
    elif typ == '2':#ladder
        ladder = Ladder(x,y, "Sprites/Blocks/Block3.png" )   #ladder
    elif typ == '3':                                                            #Static platform
        block = Block(x,y,0,False, "Sprites/Blocks/Block1.png")
    elif typ == '4':                                                            #Breakable platform
        block = Block(x,y,0,False, "Sprites/Blocks/Block0.png")    #Wall                                          
    elif typ == '5':                                                            #vertical wall
        block = Block(x,y,0,True, "Sprites/Blocks/Block2.png") #Breakable                                           
    elif typ == '7':                                                            #small slime
        ball = Ball(4,x,y, True)
    elif typ == '8':                                                            #medium slime
        ball = Ball(2,x,y, True)
    elif typ == '9':                                                            #Big slime
        ball = Ball(1,x,y, True)


def levelreader(file, level): #Dit is de maingame loop (alweer in functie vorm ivm main menu)
    lines = readlines(file) # eerst readlines functie, de file kan of zijn alle zelf gemaakt levels (Levels.txt) of de campaign mode (Campaign.txt) met daarbij bij welk level de speler is. Deze informatie word opgehaald uit de file main.py
    xline = int(len(lines) / 22) #berekent hoeveel levels er in de file staan (alleen van belang bij Levels.txt)
    run = 1 #standaard run
    line = 0
    Level = []
    value = 0
    linenumber = 0
    
    blockvalue = 0
    levelname = True #variable die zegt of het keuze menu gelaad moet worden.
    

    if file == "Campaign.txt": #als het de campaign is moet er zonder een level select direct een level ingeladen worden.
        spawnlevel(Level, level, blockvalue, lines) #Spawnlevel functie aangeroepen
        levelname = False
        run = 0
        
    
    while run == 1: 
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit() #standaard quit game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #gebruikt om level te selecteren
                    print(Level) #debug tool
                    spawnlevel(Level, linenumber, blockvalue, lines) #geselecteerde level word ingespawned
                    levelname = False #keuze menu moet weg dus false.
                    run = 0 # run moet naar 0
                elif event.key == pygame.K_UP:
                    linenumber += 1 #bewegen door selectie menu
                elif event.key == pygame.K_DOWN:
                    linenumber -= 1 
                elif event.key == pygame.K_ESCAPE:
                    run = 0

        if linenumber >= xline: #deze functie zorgt ervoor dat je door alle levels kan scrollen, hoeveel het er ook zijn. in theory zit er geen limiet op hoeveelheid levels.
            linenumber = 0
        elif linenumber < 0:
            linenumber = xline - 1

        if levelname == True:

        #deze lines zorgen voor het scroll effect in het menu, Zoals je kan zien staan er geen vaste waardes in. Hier berekent hij welke line je moet nemen om de naam van het level te krijgen,
        #ook berekend hij het voor alle name van de 2 die ervoor waren en de 2 levels die er na komen -> scroll effect
            name0 = myfont.render( lines[((linenumber - 2) % xline) * 22], False, black) 
            name1 = myfont.render( lines[((linenumber - 1) % xline) * 22], False, black)
            name2 = myfont.render( lines[((linenumber - 0) % xline) * 22], False, green)
            name3 = myfont.render( lines[((linenumber + 1) % xline) * 22], False, black)
            name4 = myfont.render( lines[((linenumber + 2) % xline) * 22], False, black)




        everything.update()
      
        screen.blit(background,(0,0))
        
        everything.draw(screen)

        if levelname == True: #print alle names
            screen.blit(name0, (500, 100))
            screen.blit(name1, (500, 200))
            screen.blit(name2, (500, 300))
            screen.blit(name3, (500, 400))
            screen.blit(name4, (500, 500))



        pygame.display.flip()

        clock.tick(60)

    
    return playercords # als ej uit while loop bent -> return naar game met de playercords zodat deze terplekken ingespawned kunnen worden.
