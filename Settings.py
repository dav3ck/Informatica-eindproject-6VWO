import pygame

#Dit script laat het plaatje in waar de controlls weergegeven staan

screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
screen_rect=screen.get_rect()
pygame.display.set_caption('Sticky Icky beta')
clock = pygame.time.Clock()

#slaat het control plaatje op in de variable backgorund, plaatje is layout.png. Convert functie helpt bij het inladen van plaatje
background = pygame.image.load('Sprites/Extra/layout.png').convert() 

pygame.mouse.set_visible(0) #Removed mouse
black = (0,0,0) #kleur zwart

#Dit script doet niet veel behalven het plaatje laten zien, daarom heeft het maar 1 knop, wat terug is. met gebruik van de return functie

def settings():
    while True:
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                    

        screen.fill(black)
        screen.blit(background,(250,300)) #print het plaatje

        pygame.display.flip()

        clock.tick(60)
