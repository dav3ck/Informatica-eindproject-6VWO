import pygame

screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
screen_rect=screen.get_rect()
pygame.display.set_caption('Sticky Icky beta')
clock = pygame.time.Clock()

background = pygame.image.load('Sprites/Extra/layout.png').convert()

pygame.mouse.set_visible(0) #Removed mouse
black = (0,0,0)

def settings():
    while True:
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                    

        screen.fill(black)
        screen.blit(background,(250,300))

        pygame.display.flip()

        clock.tick(60)
