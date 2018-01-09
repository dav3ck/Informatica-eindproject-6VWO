import pygame
import math
import random
pygame.init()
from main import * #imports all from classes, removes the need for "classes."prepend
from Leveleditor import *
from Settings import *

#Dit script is het main selectie menu van eht spel, dit is ook het script wat je opent als je het spel opent, dit script bied je alle keuzes aan

black = (0, 0, 0) #defines the colour black
white = (255,255,255)
red = (255, 0, 0)
darkred = (139, 0,0) 

color = [white,white,white,white,white]

withd = 1280 #Breedte van scherm
height = 1024 #Hoogte van scherm

pygame.font.init()
myfont = pygame.font.Font('Sprites/Font/Arcade.ttf', 60)
myfontsmall = pygame.font.Font("Sprites/Font/Arcade.ttf", 40)


#window setup, zit is normale Screen setup
screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
screen_rect=screen.get_rect()
pygame.display.set_caption('Sticky Icky beta')
clock = pygame.time.Clock()

pygame.mouse.set_visible(0) #Removed mouse

windownum = 0 #Variable die bij houd welke optie je hebt geselecteerd


pygame.mixer.music.load("Theme.wav")
#pygame.mixer.music.play(loops=-1, start=0.0)

#Arcade
#Campaign
#Level
#LevelEditor
#Settings

#main game loop
def choice (windownum):
    if windownum == 0:
        maingame("arcade") #functue die main game load in arcade, de "arcade" is om te zeggen dat het arcade mode is ipv level of campaign.
    elif windownum == 1:
        editor()            #functie die editor load
    elif windownum == 2:
        maingame("Level")   #functie die main game load met levels 
    elif windownum == 3:
        maingame("Campaign")    #funtie dat main game load met campaign 
    elif windownum == 4:
        settings()

while True:
    for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    #dit is om door het menu te navigaten, als je pijltje omhoog drukt gaat waarde van var windownum omhoog -> andere optie geselecteerd
                    windownum -= 1
                elif event.key == pygame.K_DOWN:
                    windownum += 1
                elif event.key == pygame.K_SPACE:
                    choice(windownum) #dit roept de functie hierboven aan, en deze functie stuurt je door naar de geselecteerde gamemdoe

    if windownum < 0:   #deze regels zorgen ervoor dat je binnen de beperkingen van het menu blijft, als je windownum groter dan 4 worden, aangezien er maar 5 mogelijkheden zijn, word deze waarde terug gezet naar 0
        windownum = 4
    elif windownum > 4:
        windownum = 0

    color = [white,white,white,white,white] #Array waar de kleuren voor de opties inzitten
    color[windownum] = red #de waarde van windownum in de array word rood gekleurd, zodat de geselecteerde optie rood word.

    screen.fill(black) #Standaard schermopruiming

    option0 = myfont.render("Arcade", False, color[0])      #dit zijn alle opties die gerender'd worden
    option1 = myfont.render("Leveleditor", False, color[1])
    option2 = myfont.render("Levels", False, color[2])
    option3 = myfont.render("Campaign", False, color[3])
    option4 = myfont.render("Controls", False, color[4])
    
    screen.blit(option0, (500, 300))                        #Hier worden de opties op het scherm neer gezet
    screen.blit(option1, (500, 400))
    screen.blit(option2, (500, 500))
    screen.blit(option3, (500, 600))
    screen.blit(option4, (500, 700))
    
    pygame.display.flip()                                   #standaard flip

    clock.tick(60)                                          #Frames per seconde (hoe vak het door het script heen gaat per seconden.                
