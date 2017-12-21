import pygame
import math
import random
pygame.init()
from main import * #imports all from classes, removes the need for "classes."prepend
from Leveleditor import *

black = (0, 0, 0) #defines the colour black
white = (255,255,255)

withd = 1280 #Breedte van scherm
height = 1024 #Hoogte van scherm

pygame.font.init()
myfont = pygame.font.Font('Sprites/Font/Arcade.ttf', 60)
myfontsmall = pygame.font.Font("Sprites/Font/Arcade.ttf", 40)


#window setup
screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
screen_rect=screen.get_rect()
pygame.display.set_caption('Sticky Icky beta')
clock = pygame.time.Clock()

pygame.mouse.set_visible(0) #Removed mouse

windownum = 0 


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
        maingame("arcade")
    elif windownum == 1:
        editor()
    elif windownum == 2:
        print("ok")
    elif windownum == 3:
        print("ok")
    elif windownum == 4:
        print("ok")

while True:
    for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    windownum -= 1
                elif event.key == pygame.K_DOWN:
                    windownum += 1
                elif event.key == pygame.K_SPACE:
                    print("Kek")
                    choice(windownum)

    if windownum < 0:
        windownum = 4
    elif windownum > 4:
        windownum = 0

    screen.fill(black)
                
