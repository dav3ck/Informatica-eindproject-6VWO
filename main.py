
#libraries management
import pygame
import math
import random
pygame.init()
from classes import * #imports all from classes, removes the need for "classes."prepend
from Levelreader import *
'''
black = (0, 0, 0) #defines the colour black
white = (255,255,255)

withd = 1280 #Breedte van scherm
height = 1024 #Hoogte van scherm

pygame.font.init()
myfont = pygame.font.Font('Sprites/Font/Arcade.ttf', 60)
myfontsmall = pygame.font.Font("Sprites/Font/Arcade.ttf", 40)

spawntimer = 0

globaltimer = 0

spawninterval = 0

gamestart = False

highscore = Highscore()

highscore2 = Highscore2()

playernum = 1


#window setup
screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
screen_rect=screen.get_rect()
pygame.display.set_caption('Sticky Icky beta')
clock = pygame.time.Clock()

background = pygame.image.load('Sprites/Extra/Background.png').convert()

pygame.mouse.set_visible(0) #Removed mouse


#creates play envoirment 
floor = Floor()
wall = Wall(0) #left wall
wall = Wall(1275) #right wall


flashart = Flashart("Sprites/Extra/Flash.png", 0, 0)

pygame.mixer.music.load("Theme.wav")
#pygame.mixer.music.play(loops=-1, start=0.0
'''

def kill():
    for sprite in everything:
        pygame.sprite.Sprite.kill(sprite)

#main game loop
def maingame(gametype):
    black = (0, 0, 0) #defines the colour black
    white = (255,255,255)

    withd = 1280 #Breedte van scherm
    height = 1024 #Hoogte van scherm

    pygame.font.init()
    myfont = pygame.font.Font('Sprites/Font/Arcade.ttf', 60)
    myfontsmall = pygame.font.Font("Sprites/Font/Arcade.ttf", 40)

    screen = pygame.display.set_mode((1280,1024))#, pygame.FULLSCREEN)
    screen_rect=screen.get_rect()
    clock = pygame.time.Clock()

    spawntimer = 0

    globaltimer = 0

    spawninterval = 0

    gamestart = False

    highscore = Highscore()
    highscores = []
    with open('highscores.txt', 'r') as r:
        for line in sorted(r):
            highscores.insert(0, line)

    highscores2 = []
    with open('highscores2.txt', 'r') as r:
        for line in sorted(r):
            highscores2.insert(0, line)

    highscore2 = Highscore2()
    

    playernum = 1

     #loading in level
    
    floor = Floor()
    wall = Wall(0) #left wall
    wall = Wall(1275) #right wall
    
    
    if gametype == "arcade":
        player = Player(600,800) #creates the player
        player2 = Player2(600,800)
    elif gametype == "Level":
        playercords = levelreader('Levels.txt', 0)
        player = Player(playercords[0][0], playercords[0][1])
        player2 = Player2(playercords[1][0], playercords[1][1])
    elif gametype == "Campaign":
        level = 0
        playercords = levelreader('Campaign.txt', level)
        player = Player(playercords[0][0], playercords[0][1])
        player2 = Player2(playercords[1][0], playercords[1][1])
            
    flashart = Flashart("Sprites/Extra/Flash.png", 0, 0)

    
    
    pygame.mixer.music.load("Theme.wav")

    background = pygame.image.load('Sprites/Extra/Background.png').convert()

    Grunt = pygame.mixer.Sound("Sounds/Grunt-3.wav")
    Keypress = pygame.mixer.Sound("Sounds/Keyboard-sound.wav")
    Plop = pygame.mixer.Sound("Sounds/Plop-sound.wav")
    Reload = pygame.mixer.Sound("Sounds/Reloading.wav")
    Schuiffluit = pygame.mixer.Sound("Sounds/Schuiffluit-goed.wav")
    Shot = pygame.mixer.Sound("Sounds/Shot goed.wav")
    Splat = pygame.mixer.Sound("Sounds/Slime-splat.wav")
    Deaththeme = pygame.mixer.Sound("Sounds/Ukulile-G-minor-down.wav")
    

    run = 1
             
    while run == 1:
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN: #handles all keypresses
                if event.key == pygame.K_LEFT: #move left
                    if player.alive == True and gamestart == True:
                        player.changespeed(-5)
                    elif len(keyboards) == 1:
                        keyboard.num -= 1
                elif event.key == pygame.K_RIGHT: #move right
                    if player.alive == True and gamestart == True:
                        player.changespeed(5)
                    elif len(keyboards) == 1:
                        keyboard.num += 1
                elif event.key == pygame.K_UP:
                    if player.alive == True:
                        player.changeyspeed(-5)
                    elif len(keyboards) == 1:
                        keyboard.num -= 10
                elif event.key == pygame.K_DOWN:
                    if player.alive == True:
                        player.changeyspeed(5)
                    elif len(keyboards) == 1:
                        keyboard.num += 10
                elif event.key == pygame.K_SPACE: #shoot button
                    if gamestart == False:
                        for ball in balls:
                            ball.freeze = False
                        gamestart = True
                        if gametype == "arcade":
                            ball = Ball(1,500,70, False)
                        pygame.sprite.Sprite.kill(flashart)
                        if playernum == 1:
                            pygame.sprite.Sprite.kill(player2)
                            player.lives = 3
                    if player2.alive == True and playernum == 2:
                        if player2.ammo > 0 and spawntimer > 0:
                            Shot.play()
                            bullet = Bullet(player2.xcord,player2.ycord)
                            player2.ammo -= 1
                            player2.fire = True
                elif event.key == pygame.K_RETURN:
                    if len(keyboards) == 1:
                        Keypress.play()
                        if textbox.ittnum < 5:
                            if (keyboard.capital == False and keyboard.num < 38): 
                                keyboard.name = keyboard.name + keyboard.alphabet[keyboard.num] #adds letter to list with name
                                letter = Letter(textbox.ittnum,keyboard.num,False)
                                textbox.ittnum += 1
                            elif keyboard.capital == True and keyboard.num < 38:
                                keyboard.name = keyboard.name + keyboard.alphabet[keyboard.num + 37] #adds Capital letter to name list
                                keyboard.capital = False  #Zet capital terug naar false > je print no longer Capitals
                                letter = Letter(textbox.ittnum,keyboard.num,True)
                                textbox.ittnum += 1
                        if keyboard.num == 38:
                            if keyboard.capital == False: #Zet capital naar true, tenzij het al true is, dan zet het het terug naar False
                                keyboard.capital = True
                            else:
                                keyboard.capital = False
                        elif keyboard.num == 39 and textbox.ittnum != 0: #Haalt een letter weg
                            keyboard.name = keyboard.name[:-1]
                            textbox.ittnum -= 1
                            for letter in letters:
                                if textbox.ittnum == letter.ittnum:
                                     pygame.sprite.Sprite.kill(letter)
                                if textbox.ittnum < 0:
                                    textbox.ittnum = 0
                        elif keyboard.num == 40: #submits score and resets game
                            if playernum == 1:
                                if len(keyboard.name) != 0:
                                    with open('highscores.txt','a') as f:
                                        f.write(scoredisp + " - " + keyboard.name + "\n")
                                highscores = []
                                with open('highscores.txt', 'r') as r:
                                    for line in sorted(r):
                                        highscores.insert(0, line)
                            else:
                                if len(keyboard.name) != 0:
                                    with open('highscores2.txt','a') as f:
                                        f.write(scoredisp + " - " + keyboard.name + "\n")
                                highscores2 = []
                                with open('highscores2.txt', 'r') as r:
                                    for line in sorted(r):
                                        highscores2.insert(0, line)
                            for sprite in everything:
                                pygame.sprite.Sprite.kill(sprite)
                            gamestart = False
                            player = Player(600,752)
                            player2 = Player2(600,752)
                            floor = Floor()
                            wall = Wall(0)
                            wall = Wall(1275)
                            highscore = Highscore()
                            highscore2 = Highscore2()
                            flashart = Flashart("Sprites/Extra/Flash.png", 0, 0)
                            player.lives = 6
                elif event.key == pygame.K_r: #reload
                    player2.reload()
                elif event.key == pygame.K_m:
                    screen = pygame.display.set_mode((1280,1024), pygame.FULLSCREEN)
                elif event.key == pygame.K_n:
                    screen = pygame.display.set_mode((1280,1024))
                    pygame.mouse.set_visible(1)
                elif event.key == pygame.K_KP0:
                    if player.alive == True:
                        if player.ammo > 0 and spawntimer > 0:
                            Shot.play()
                            bullet = Bullet(player.xcord,player.ycord)
                            player.ammo -= 1
                            player.fire = True
                elif event.key == pygame.K_KP1:
                    player.reload()
                elif event.key == pygame.K_a: #move left
                    if player2.alive == True and gamestart == True:
                        player2.changespeed(-5)
                elif event.key == pygame.K_d: #move right
                    if player2.alive == True and gamestart == True:
                        player2.changespeed(5)
                elif event.key == pygame.K_w:
                    if player.alive == True:
                        player2.changeyspeed(-5)
                elif event.key == pygame.K_s:
                    if player2.alive == True:
                        player2.changeyspeed(5)
                elif event.key == pygame.K_p and gamestart == False:
                    if gametype == "Level" or gametype == "arcade":
                        if playernum == 1:
                            playernum = 2
                        else:
                            playernum =1
                    elif gametype == "Campaign" and level == 0:
                        if playernum == 1:
                            playernum = 2
                        else:
                            playernum =1
                elif event.key == pygame.K_BACKSPACE:
                    print("Hello?")
                    run = 0
                    kill()
            elif event.type == pygame.KEYUP: #handles all key releases
                if event.key == pygame.K_LEFT: #left key release
                    if player.alive == True and gamestart == True:
                        player.changespeed(5)
                elif event.key == pygame.K_RIGHT: #right key release
                    if player.alive == True and gamestart == True:
                        player.changespeed(-5)
                elif event.key == pygame.K_UP:
                    if player.alive == True and gamestart == True:
                        player.changeyspeed(5)
                        player.ymove = False
                elif event.key == pygame.K_DOWN:
                    if player.alive == True and gamestart == True:
                        player.changeyspeed(-5)
                        player.ymove = False
                elif event.key == pygame.K_a:
                    if player2.alive == True and gamestart == True:
                        player2.changespeed(5)
                elif event.key == pygame.K_d:
                    if player2.alive == True and gamestart == True:
                        player2.changespeed(-5)
                elif event.key == pygame.K_w:
                    if player2.alive == True and gamestart == True:
                        player2.changeyspeed(5)
                        player2.ymove = False
                elif event.key == pygame.K_s:
                    if player2.alive == True and gamestart == True:
                        player2.changeyspeed(-5)
                        player2.ymove = False
                elif event.key == pygame.K_ESCAPE:
                    run = 0
            

        #GUI text
        if playernum == 1:
            prescore = str(int(player.killcount * 100))
            zeros = 6 - len(prescore)
            scoredisp = '0' * zeros + prescore
        else:
            prescore = str(int((player.killcount + player2.killcount)* 100))
            zeros = 6 - len(prescore)
            scoredisp = '0' * zeros + prescore        
        
        scoretext = myfont.render(scoredisp, False, black)
        ammotext = myfont.render(str(player.ammo), False, black)
        ammotext2 = myfont.render(str(player2.ammo), False, white)
        lifetext = myfont.render(str(player.lives), False, black)
        playertext = myfontsmall.render("Number of players: " + str(playernum)+ " (press P to change)", False, white)

        #Game logica
        spawntimer += 1

        globaltimer += 1

        if player.lives <= 0:
            player.alive = False
            player2.alive = False

        if player.alive == False and player.once == 1:
            flashart = Flashart("Sprites/Extra/GameOver.png", 414 , 50)
            player.deathtimer = 1
            Deaththeme.play()

        if player.alive == False and player.deathtimer > 180 and len(keyboards) == 0 and gametype == "arcade": #Dit load na 3 seconde textbox in
            keyboard = Keyboard()
            textbox = Textbox()
        elif gametype == "Level" and player.alive == False and player.deathtimer > 180:
            run = 0
        elif gametype == 'Campaign' and player.alive == False and player.deathtimer > 180:
            run = 0
            
        if player.ammo == 0: #reload mechanics
            Reload.play()
            Reload.set_volume(0.2)
            player.reducer = 0.5
            player.ammotimer += 1
            if player.ammotimer == 120:
                player.ammo = 10
                player.reducer = 1
                player.ammotimer = 0

        if player2.ammo == 0: #reload mechanics
            Reload.play()
            Reload.set_volume(0.2)
            player2.reducer = 0.5
            player2.ammotimer += 1
            if player2.ammotimer == 120:
                player2.ammo = 10
                player2.reducer = 1
                player2.ammotimer = 0
        if player.ammo > 0 and player.ammotimer > 0: #alowss abortion of reloading
            player.reducer = 1
            player.ammotimer = 0

        #colisions
        for ball in balls:
            hits = pygame.sprite.spritecollide(player, balls, False) #ball on player colisions
            for ball in hits:
                Grunt.play()
                if ball.typenum == 0:
                    ball.yspeed = 9.5
                if player.immune == False:
                    player.immune = True
                    player.lives -= 1
        
        for ball in balls:
            if globaltimer >= 1 and playernum == 2:
                hits = pygame.sprite.spritecollide(player2, balls, False) #ball on player colisions
                for ball in hits:
                    Grunt.play()
                    if ball.typenum == 0:
                        ball.yspeed = 9.5
                    if player2.immune == False:
                        player2.immune = True
                        player.lives -= 1
                    
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, balls, True) #bullet on ball collisions
            for ball in hits:
                Plop.play()
                if ball.ycord > 50:
                    pygame.sprite.Sprite.kill(bullet)
                    if ball.check == 1:
                        ball = Ball(2,ball.xcord,ball.ycord, False)
                        ball = Ball(3,ball.xcord,ball.ycord, False)
                        player.killcount += 1
                    elif ball.check == 2 or ball.check == 3:
                        ball = Ball(4,ball.xcord,ball.ycord, False)
                        ball = Ball(5,ball.xcord,ball.ycord, False)
                        player.killcount += 1
                    else:
                        player.killcount += 3
                    
        for ball in balls: #ball floor bouncing
            hits = pygame.sprite.spritecollide(floor, balls, False)
            for ball in hits:
                if ball.typenum == 0:
                    Splat.play()
                    ball.yspeed = 0
                    ball.xspeed /= 10000
                    ball.weight /= 10000
                    ball.typenum = 1
                    ball.ittnum = -1

        for ball in balls: #ball wall bouncing
            hits = pygame.sprite.spritecollide(ball, walls, False)
            for wall in hits:
                if ball.xspeed > 0 and ball.typenum == 1:
                    ball.xcord -= 10
                elif ball.xspeed < 0 and ball.typenum == 1:
                    ball.xcord += 10
                if player.alive == True:
                    ball.xspeed *= -1

        for upgrade in upgrades: #stops the upgrades on the floor
            hits = pygame.sprite.spritecollide(floor, upgrades, False)
            for upgrade in hits:
                if upgrade.type == 1:
                    upgrade.yspeed = 0
                    upgrade.detimer = 1
                    upgrade.ycord += 92
                    upgrade.type = 2

        for upgrade in upgrades: #shoot the upgrades down
            hits = pygame.sprite.spritecollide(upgrade, bullets, False)
            for bullet in hits:
                upgrade.yspeed = 5
                upgrade.xspeed = 0
                upgrade.type = 1
                pygame.sprite.Sprite.kill(bullet)

        for upgrade in upgrades: #runs the powerups
            hits = pygame.sprite.spritecollide(player, upgrades, False)
            for upgrade in hits:
                Schuiffluit.play()
                upgrade.yspeed = 0
                upgrade.powerup(player,ball,balls,player)
                player.killcount += 0.5

        for upgrade in upgrades: #runs the powerups
            hits = pygame.sprite.spritecollide(player2, upgrades, False)
            for upgrade in hits:
                Schuiffluit.play()
                upgrade.yspeed = 0
                upgrade.powerup(player2,ball,balls,player)
                player.killcount += 0.5
                                                    
        for upgrade in upgrades: #ends the powerups
            upgrade.powerdown(player,ball,balls)

        for upgrade in upgrades:
            upgrade.powerdown(player2,ball,balls)


        for ladder in ladders:
            hits = pygame.sprite.spritecollide(player, ladders, False)
            for ladder in hits:
                player.ladder = True
                player.ladderonce = 0
                

        for ladder in ladders:
            hits = pygame.sprite.spritecollide(player2, ladders, False)
            for ladder in hits:
                player2.ladder = True
                player2.ladderonce = 0        

        def blockhit(player):
            for block in blocks:
                hits = pygame.sprite.spritecollide(player, blocks, False)
                for block in hits:
                    for bullet in bullets:
                        if player == bullet and block.breakable == True:
                            pygame.sprite.Sprite.kill(block)
                            pygame.sprite.Sprite.kill(player)
                        if player == bullet:
                            pygame.sprite.Sprite.kill(player)
                    for ball in balls:
                        if player != ball:
                            if player.ycord < (block.ycord) and player.ycord > (block.ycord - 70): #left right collisions
                                if player.xcord < (block.xcord + 40) and player.xcord > (block.xcord + 20): #player colliding from right
                                    player.xcord = block.xcord + 40
                                elif player.xcord > (block.xcord - 56) and player.xcord < (block.xcord + 20): #player colliding from left            
                                    player.xcord = block.xcord - 56
                            elif player.xcord < (block.xcord + 40) or player.xcord > (block.xcord - 56): #up down collisions
                                if player.ycord < (block.ycord + 40) and player.ycord > (block.ycord + 20): #player colliding from down
                                    player.ycord = block.ycord + 40
                                if player.ycord > (block.ycord - 84) and player.ycord < (block.ycord + 20): #player colliding from up            
                                    player.ycord = block.ycord - 84
                        else:
                            if player.ycord < (block.ycord) and player.ycord > (block.ycord - 70): #left right collisions
                                if player.xcord < (block.xcord + 42) and player.xcord > (block.xcord + 20): #player colliding from right
                                    player.xspeed *= -1
                                elif player.xcord > (block.xcord - 56) and player.xcord < (block.xcord + 20): #player colliding from left            
                                    player.xspeed *= -1
                            elif player.xcord < (block.xcord + 40) or player.xcord > (block.xcord - 56): #up down collisions
                                if player.ycord < (block.ycord + 40) and player.ycord > (block.ycord + 20): #player colliding from down
                                    player.ycord = block.ycord + 42
                                elif player.ycord > (block.ycord - 84) and player.ycord < (block.ycord + 20): #player colliding from up            
                                    player.ycord = block.ycord - 86
                                    if player == ball:
                                        if ball.typenum == 0:
                                            ball.yspeed = 0
                                            ball.xspeed /= 10000
                                            ball.weight /= 10000
                                            ball.typenum = 1
                                            ball.ittnum = -1

        
        
        blockhit(player)
        blockhit(player2)



        for ball in balls:
            blockhit(ball)
        for bullet in bullets:
            blockhit(bullet)

        #spawning
        if gametype == "arcade":
            if globaltimer < 3600:
                spawninterval = int(-1 / 14400 * math.pow(globaltimer, 2) + 1800)
            else:
                spawninterval = 900

            if ((player.killcount > 12 and len(balls) < 2) or spawntimer == spawninterval): #auto spawns balls
                ball = Ball(1,500,70,False)
                spawntimer = 0

            if globaltimer % 900 == 0: 
                if globaltimer % 2700 == 0:
                    upgrade = Upgrade(random.randrange(3,6))
                else:
                    upgrade = Upgrade(random.randrange(3))

        elif len(balls) == 0 and gametype == "Level":
            run = 0
        elif len(balls) == 0 and gametype == "Campaign" and level < 9:
            kill()
            level += 1
            gamestart = False
            floor = Floor()
            wall = Wall(0)
            wall = Wall(1275)
            player.lives = 6
            playercords = levelreader('Campaign.txt', level)        #Spawned volgende level
            player = Player(playercords[0][0], playercords[0][1])
            player2 = Player2(playercords[1][0], playercords[1][1])
        elif len(balls) == 0 and gametype == "Campaign" and level == 9:
            run = 0

            
                
                
            
            

        everything.update()
        
        #Screen management

        if player.xcord > (withd - 50):
            player.xcord = (withd - 50)
        elif player.xcord < 0:
            player.xcord = 0

        if player2.xcord > (withd - 50):
            player2.xcord = (withd - 50)
        elif player2.xcord < 0:
            player2.xcord = 0
            
        screen.blit(background,(0,0))
        
        everything.draw(screen)

        #Display tekst    

        screen.blit(scoretext,(880,950))
        screen.blit(ammotext, (380, 950))
        screen.blit(lifetext, (205, 950))
        if gamestart == False:
            screen.blit(playertext, (10, 10))
        if playernum == 2:
            screen.blit(ammotext2, (500, 950))
        
        if player.alive == False and player.once > 2:
            globaltimer = 0
            spawntimer = 0    
        if gamestart == False and playernum == 1:
            globaltimer = 0
            spawntimer = 0
            for i in range(10):
                screen.blit(myfontsmall.render(str(i + 1) + ". " + str(highscores[i]).replace("\n",""), False, black), (highscore.xcord, highscore.tempy))
                highscore.tempy += 40
        elif gamestart == False and playernum == 2:
            globaltimer = 0
            spawntimer = 0
            for i in range(10):
                screen.blit(myfontsmall.render(str(i + 1) + ". " + str(highscores2[i]).replace("\n",""), False, black), (highscore2.xcord, highscore2.tempy))
                highscore2.tempy += 40        
                
        #Flip
        
        pygame.display.flip()
        
        #sets max fps
        clock.tick(60)
    
    screen.fill(black)
    kill()
    pygame.display.flip()
    return

        

