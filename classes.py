import pygame
import random

#colour variables
black = (0, 0, 0)
white = (255, 255, 255)

#lists
bullets = pygame.sprite.Group() #list that will hold all the bullets
balls = pygame.sprite.Group() #list that will hold all ze balls
lines = pygame.sprite.Group() #list that holds all the lines in editor mode
everything = pygame.sprite.Group() #list that will hold everything
walls = pygame.sprite.Group() #lits that will hold all the floors and walls etc
players = pygame.sprite.Group()
upgrades = pygame.sprite.Group()
floors = pygame.sprite.Group()
letters = pygame.sprite.Group()
keyboards = pygame.sprite.Group()
ladders = pygame.sprite.Group()
blocks = pygame.sprite.Group()


#highscores
highscores = []
with open('highscores.txt', 'r') as r:
    for line in sorted(r):
        highscores.insert(0, line)

highscores2 = []
with open('highscores2.txt', 'r') as r:
    for line in sorted(r):
        highscores2.insert(0, line)

#sprite lists
ballanimation = [] #[size[type[variation[itteration]]]]
l1 = []
k1 = []
j1 = []

for i in range (3): #size of the ball size 0 = big, 1 = medium, 2 = small
    legacy0 = "Sprites/balls/size" + str(i)
    for j in range (2): #where the ball is in its bounce (type) 0 = in motion, 1 = on the ground
        legacy1 = legacy0 + "/type" + str(j)
        for k in range (3): #wich variation it is
            legacy2 = legacy1 + "/variation" + str(k)
            for l in range (5): #what exact sprite it is (itteration)
                legacy3 = legacy2 + "/itteration" + str(l) +".png"
                l1.append(legacy3)
            k1.append(l1)
            l1 = []
        j1.append(k1)
        k1 = []
    ballanimation.append(j1)
    j1 = []

#Player animation
playeranimation = []

for i in range(3):
    legacy0 = "Sprites/Player/type" + str(i)
    for k in range (2):
        legacy1 = legacy0 + "/var" + str(k)
        for j in range (6):
            legacy2 = legacy1 + "/itteration" + str(j) + ".png"
            j1.append(legacy2)
        k1.append(j1)
        j1 = []
    playeranimation.append(k1)
    k1 = []

#upgrade animation

upgradeanimation = []

for i in range(3):
    legacy0 = "Sprites/Upgrade/type" + str(i)
    for k in range (2):
        legacy1 = legacy0 + "/var" + str(k)
        for j in range (8):
            legacy2 = legacy1 + "/itteration" + str(j) + ".png"
            j1.append(legacy2)
        k1.append(j1)
        j1 = []
    upgradeanimation.append(k1)
    k1 = []

#keyboard animation

keyboardanimation = [] #Array met alle Keyboard sprites erin

for i in range(81): #Zelfde als voor slime animatie sprites alleen dit keer kleiner
    legacy0 = "Sprites/Keyboard/Itteration" + str(i) + ".png"
    keyboardanimation.append(legacy0)

#floor animation

groundanimation = [] #Array met alle ground sprites

for i in range(5): #Zelfde als voor slime animatie sprites alleen dit keer kleiner
    legacy0 = "Sprites/Ground/itteration" + str(i) + ".png"
    groundanimation.append(legacy0)

#Textbox animation

textboxanimation = [] #Array met alle ground sprites

for i in range(7): #Zelfde als voor slime animatie sprites alleen dit keer kleiner
    legacy0 = "Sprites/Textbox/itteration" + str(i) + ".png"
    textboxanimation.append(legacy0)

#letter annimation
letteranimation = []

for i in range (64):
    legacy0 = "Sprites/letters/l0_letter" + str(i) + ".png"
    letteranimation.append(legacy0)


#class defenitions
class parent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xcord = 0
        self.ycord = 0
        self.xspeed = 0 #horizontal speed
        self.yspeed = 0 #vertical speed
        self.timer = 0 #timer to alternate bitmaps
        everything.add(self)

class Ball(parent):
    def __init__(self,check,x,y,freeze):
        super().__init__()
        self.xcord = x
        self.ycord = y
        self.dia = 0 #diameter of the ball
        self.weight = 0 #size of the parabole bigger number smaller parabole
        self.check = check #checks ball type
        self.sizenum = 0 #ball size number for animation
        self.typenum = 0 #the type of the ball
        self.ittnum = 0 #what itteration ball animation is on
        self.launch = 10
        self.stop = False #Gebruikt bij stop upgrade
        self.freeze = freeze
        if check == 1: #biggest ball
            self.xspeed = -2
            self.dia = 160
            self.weight = 0.1
            self.image = pygame.image.load("Sprites/balls/size0/type0/variation0/itteration0.png")
        elif check == 2: #medium ball right
            self.xspeed = 3
            self.dia = 80
            self.weight = 0.2
            self.sizenum = 1
            self.image = pygame.image.load("Sprites/balls/size1/type0/variation0/itteration0.png")
        elif check == 3: #medium ball left
            self.xspeed = -3
            self.dia = 80
            self.weight = 0.2
            self.sizenum = 1
            self.image = pygame.image.load("Sprites/balls/size1/type0/variation0/itteration0.png")
        elif check == 4: #small ball right
            self.xspeed = 5
            self.dia = 40
            self.weight = 0.3
            self.sizenum = 2
            self.image = pygame.image.load("Sprites/balls/size2/type0/variation0/itteration0.png")
        elif check == 5: #small ball left
            self.xspeed = -5
            self.dia = 40
            self.weight = 0.3
            self.sizenum = 2
            self.image = pygame.image.load("Sprites/balls/size2/type0/variation0/itteration0.png")

        self.rect = self.image.get_rect()
        balls.add(self)


    def update(self):
        if self.freeze == False:
            self.xcord += self.xspeed #handles ball horizontal movement

        self.timer += 1
        if self.timer > 30 and self.typenum == 0:
            self.ittnum += 1
            self.timer = 0
            if self.ittnum > 4:
                self.ittnum = -1
        if self.timer > 3 and self.typenum == 1:
            self.ittnum += 1
            self.timer = 0
            if self.ittnum == 4:
                self.yspeed = self.launch
                self.xspeed *= 10000
                self.weight *= 10000
                self.ittnum = -1
                self.typenum = 0

        self.yspeed -= self.weight #handles ball bouncing
        self.ycord -= self.yspeed

        self.image = pygame.image.load(ballanimation[self.sizenum][self.typenum][0][self.ittnum])
        self.rect = self.image.get_rect()
        self.rect.x = self.xcord
        self.rect.y = self.ycord

class Wall(parent):
    def __init__(self, x):
        super().__init__()
        self.xcord = x
        self.image = pygame.Surface([5,1024])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        walls.add(self)

class Player(parent):
    def __init__(self,x,y):
        super().__init__()
        self.reducer = 1
        self.reducerup = 1
        self.xcord = 640 #x coördinate
        self.ycord = 752 #y coördinate
        self.ammo = 10
        self.killcount = 0
        self.timer = 0
        self.ammotimer = 0
        self.immune = False
        self.immunetimer = 0
        self.alive = True
        self.once = 0 #this is there to make sure it only adds score once, remove this with menues and such
        self.image = pygame.image.load(playeranimation[0][0][0])
        self.rect = self.image.get_rect()
        self.shooter = False # auto shooter
        self.fire = False #kijkt of player schiet
        self.firetimer = 0
        self.ittnum = 0
        self.ittnumtimer = 0
        self.immune1 = 0 #1 of 0 waarde als iets immune is
        players.add(self)
        self.deathtimer = 0
        self.lives = 6
        self.ladder = False
        self.yspeed = 3
        self.ymove = False

    def changespeed(self,x):
        self.xspeed += x

    def changeyspeed(self,y):
        self.yspeed += y
        self.ymove = True


    def reload(self):
        self.ammo = 0
        print("reloading")

    def update(self):
        if self.immune == True:
            self.immunetimer += 1
            self.immune1 = 1
            if self.immunetimer > 120:
                self.immune = False
                self.immunetimer = 0

        else:
            self.immune1 = 0

        if self.alive == False:
            self.xspeed = 0
            self.yspeed = 0
            self.once += 1


        if self.shooter == True and self.timer % 5 == 0:
            bullet = Bullet(self.xcord, self.ycord)


        if self.alive == False:
            self.image = pygame.image.load("Sprites/Extra/Death.png")
        elif self.fire == True and self.xspeed == 0:
            self.firetimer += 1
            self.image = pygame.image.load(playeranimation[0][self.immune1][1])
            if self.firetimer > 16:
                self.firetimer = 0
                self.fire = False
        elif self.xspeed > 0:
            self.fire = False
            self.image = pygame.image.load(playeranimation[1][self.immune1][self.ittnum])
            if self.ittnumtimer % 5 == 0:
                self.ittnum += 1
        elif self.xspeed < 0:
            self.fire = False
            self.image = pygame.image.load(playeranimation[2][self.immune1][self.ittnum])
            if self.ittnumtimer % 5 == 0:
                self.ittnum += 1
        else:
            self.image = pygame.image.load(playeranimation[0][self.immune1][0])
            self.ittnum = 0
            self.ittnumtimer = 0

        if self.ittnum > 5:
            self.ittnum = 0

        self.rect = self.image.get_rect()

        self.xcord += (self.xspeed * (self.reducer * self.reducerup)) #basic player movement

        if self.ladder == True and self.yspeed == 3:
            self.yspeed = 0

        self.ycord += self.yspeed

            
        if self.ycord > 752:
            self.ycord = 752

        if self.ymove == False:
            self.yspeed = 3

        self.ladder = False
        
        self.rect.x = self.xcord
        self.rect.y = self.ycord

        self.timer += 1
        self.ittnumtimer += 1
        if self.deathtimer > 0:
            self.deathtimer += 1
            

class Player2(parent):
    def __init__(self,x,y):
        super().__init__()
        self.reducer = 1
        self.reducerup = 1
        self.xcord = 640 #x coördinate
        self.ycord = 752 #y coördinate
        self.ammo = 10
        self.killcount = 0
        self.timer = 0
        self.ammotimer = 0
        self.immune = True
        self.immunetimer = 100
        self.alive = True
        self.once = 0 #this is there to make sure it only adds score once, remove this with menues and such
        self.image = pygame.image.load(playeranimation[0][0][0])
        self.rect = self.image.get_rect()
        self.shooter = False # auto shooter
        self.fire = False #kijkt of player schiet
        self.firetimer = 0
        self.ittnum = 0
        self.ittnumtimer = 0
        self.immune1 = 1 #1 of 0 waarde als iets immune is
        players.add(self)
        self.deathtimer = 0
        self.ladder = False
        self.weight = 0.7
        self.yspeed = 0

    def changespeed(self,x):
        self.xspeed += x


    def reload(self):
        self.ammo = 0
        print("reloading")

    def update(self):
        if self.immune == True:
            self.immunetimer += 1
            self.immune1 = 1
            if self.immunetimer > 120:
                self.immune = False
                self.immunetimer = 0

        else:
            self.immune1 = 0

        if self.alive == False:
            self.xspeed = 0
            self.yspeed = 0
            self.once += 1


        if self.shooter == True and self.timer % 5 == 0:
            bullet = Bullet(self.xcord, self.ycord)


        if self.alive == False:
            self.image = pygame.image.load("Sprites/Extra/Death.png")
        elif self.fire == True and self.xspeed == 0:
            self.firetimer += 1
            self.image = pygame.image.load(playeranimation[0][self.immune1][1])
            if self.firetimer > 16:
                self.firetimer = 0
                self.fire = False
        elif self.xspeed > 0:
            self.fire = False
            self.image = pygame.image.load(playeranimation[1][self.immune1][self.ittnum])
            if self.ittnumtimer % 5 == 0:
                self.ittnum += 1
        elif self.xspeed < 0:
            self.fire = False
            self.image = pygame.image.load(playeranimation[2][self.immune1][self.ittnum])
            if self.ittnumtimer % 5 == 0:
                self.ittnum += 1
        else:
            self.image = pygame.image.load(playeranimation[0][self.immune1][0])
            self.ittnum = 0
            self.ittnumtimer = 0

        if self.ittnum > 5:
            self.ittnum = 0



        self.rect = self.image.get_rect()

        self.xcord += (self.xspeed * (self.reducer * self.reducerup)) #basic player movement

        self.yspeed += self.weight
        self.ycord += self.yspeed
        self.weight = 0.7

        self.rect.x = self.xcord
        self.rect.y = self.ycord

        self.timer += 1
        self.ittnumtimer += 1
        if self.deathtimer > 0:
            self.deathtimer += 1









class Bullet(parent):
    def __init__(self, x,y):
        super().__init__()
        self.xcord = x + 40
        self.ycord = y
        self.yspeed = 10
        self.image = pygame.image.load("Sprites/Extra/Bullet.png").convert()
        self.rect = self.image.get_rect()
        bullets.add(self)


    def update(self):
        self.ycord -= self.yspeed #moving the ball up
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        if self.ycord < -10:
            pygame.sprite.Sprite.kill(self)
        if self.ycord > 820:
            self.yspeed = 0

class Floor(parent):
    def __init__(self):
        super().__init__()
        self.ycord = 824
        self.image = pygame.image.load("Sprites/Ground/itteration0.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.timer = 0
        self.ittnum = 0
        floors.add(self)

    def update(self):
        self.timer += 1
        self.rect = self.image.get_rect()

        self.rect.y = self.ycord
        self.rect.x = self.xcord

        if self.ittnum == 4:
            self.ittnum = 0



#Powerups

class Upgrade(parent):
    def __init__(self,check):
        super().__init__()
        self.ycord = random.randrange(20,400)
        self.despawn = 0 # These two are for
        self.detimer = 0 # despawning on the floor
        self.active = False
        if random.randrange(2) == 1:
            self.xcord = 1280
            self.xspeed = -1
        else:
            self.xcord = -50
            self.xspeed = 1
        self.timer = 0
        self.check = check
        upgrades.add(self)

        self.type = 0 #welke animatie
        self.ittnum = 0
        self.var = 0

        self.image = pygame.image.load(upgradeanimation[0][self.var][self.ittnum])
        self.rect = self.image.get_rect()


    def powerup(self,player,ball,balls,playercheck):
        self.detimer = 0
        self.active = True
        #zwakke powerups
        if self.check == 0: #extera ammo
            player.ammo += 20
            pygame.sprite.Sprite.kill(self)
        elif self.check == 1: #speed up
            player.reducerup = 1.5
            self.timer = 0
            self.vanish()
        elif self.check == 2: #extera life
            playercheck.lives += 1
            pygame.sprite.Sprite.kill(self)

        #sterke powerups
        elif self.check == 3: #slimes slow
            for ball in balls:
                if ball.ycord < 650:
                    ball.stop = True
                    ball.xspeed /= 10000
                    ball.yspeed = 0
                    ball.weight /= 10000
                    ball.launch = 0
                    self.timer = 0
            self.vanish()
        elif self.check == 4: #auto fire
            player.shooter = True
            self.timer = 0
            self.vanish()
        elif self.check == 5: #super extera life
            playercheck.lives += 3
            pygame.sprite.Sprite.kill(self)


    def powerdown(self,player,ball,balls):
        if self.active == True:
            if self.timer > 600 and self.check ==1:
                player.reducerup = 1
                pygame.sprite.Sprite.kill(self)
            elif self.timer > 600 and self.check == 3: #1800
                for ball in balls:
                    if ball.stop == True:
                        ball.xspeed *= 10000
                        ball.weight *= 10000
                        ball.launch = 10
                        ball.stop = False
                        pygame.sprite.Sprite.kill(self)
            elif self.timer > 300 and self.check == 4:
                player.shooter = False
                pygame.sprite.Sprite.kill(self)

    def vanish(self):
        self.image = pygame.Surface([0,0])
        self.xcord = -100
        self.ycord = -100

    def update(self):
        self.timer += 1


        if self.type == 0 and self.timer % 6 == 0:
            self.image = pygame.image.load(upgradeanimation[self.type][self.var][self.ittnum])
            self.ittnum += 1
            if self.ittnum == 8:
                self.ittnum = 0
        elif self.type == 1:
            self.image = pygame.image.load(upgradeanimation[self.type][self.var][0])
        elif self.type == 2:
            self.image = pygame.image.load(upgradeanimation[self.type][0][self.check])

        self.rect = self.image.get_rect()

        self.despawn += self.detimer
        self.xcord += self.xspeed
        self.ycord += self.yspeed
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        if self.xcord < -100 or self.xcord > 1340 or self.despawn > 300:
            pygame.sprite.Sprite.kill(self)



class Keyboard(parent): #Keyboard class
    def __init__(self):
        super().__init__()
        self.xcord = 414
        self.ycord = 400
        self.num = 0
        self.image = pygame.image.load(keyboardanimation[1])
        self.rect = self.image.get_rect()
        self.capital = False
        self.name = ""
        self.alphabet = (" ","1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y" , "z", " ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ")
        keyboards.add(self)

    def update(self):
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        if self.num > 40: #Zorgt ervoor dat het tussen de 1 tm 40 blijft
            self.num = self.num - 40
        elif self.num < 1:
            self.num = 40 + self.num
        if self.capital == False:
            self.image = pygame.image.load(keyboardanimation[self.num])
        elif self.capital == True:
            self.image = pygame.image.load(keyboardanimation[self.num + 40])

class Textbox(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 512
        self.ycord = 300
        self.ittnum = 0
        self.image = pygame.image.load(textboxanimation[self.ittnum])
        self.rect = self.image.get_rect()

    def update(self):
        self.timer += 1
        if self.timer % 30 == 0:
            self.image = pygame.image.load(textboxanimation[self.ittnum])
        elif self.timer % 15 == 0:
            self.image = pygame.image.load(textboxanimation[5])
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord


class Letter(parent):
    def __init__(self, ittnum, num, capital):
        super().__init__()
        self.ittnum = ittnum
        self.xcord = 536 + self.ittnum * 44
        self.ycord = 330
        self.charnum = self.ittnum
        self.capital = capital
        self.num = num
        if self.num == 37:
            self.image = pygame.image.load(letteranimation[63])
        elif self.capital == True and self.num > 11:
            self.image = pygame.image.load(letteranimation[self.num + 26])
        else:
            self.image = pygame.image.load(letteranimation[self.num])
        letters.add(self)

    def update(self):

        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord


class Flashart(parent):
    def __init__(self, image, x, y):
        super().__init__()
        self.xcord = x
        self.ycord = y
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord

class Highscore(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 110
        self.ycord = 315
        self.tempy = 200 #temporary y cord for progressing
        self.image = pygame.Surface([0,0])
        self.rect = self.image.get_rect()

    def update(self):
        self.tempy = self.ycord
        if self.ycord < -1000:
            pygame.sprite.Sprite.kill(self)
            highscore = Highscore()

class Highscore2(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 110
        self.ycord = 315
        self.tempy = 200 #temporary y cord for progressing
        self.image = pygame.Surface([0,0])
        self.rect = self.image.get_rect()

    def update(self):
        self.tempy = self.ycord
        if self.ycord < -1000:
            pygame.sprite.Sprite.kill(self)
            highscore2 = Highscore2()
'''class Block(parent):
    def __init__(self, row, colum, xsize, ysize, color):
        super().__init__()
        self.row = row
        self.xsize = xsize * 40
        self.ysize = ysize * 40
        self.colum = colum
        self.color = color
        self.image = pygame.Surface([self.xsize,self.ysize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()'''

class Ladder(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 500
        self.ycord = 800
        self.image = pygame.Surface([40,40])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        ladders.add(self)

class Block(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 500
        self.ycord = 700
        self.xspeed = 3
        self.yspeed = 0
        self.xleft = 400
        self.xright = 600
        self.yup = 100
        self.ydown = 200
        self.breakable = False
        self.image = pygame.Surface([40,40])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord
        blocks.add(self)

    def update(self):
        self.xcord += self.xspeed
        self.ycord += self.yspeed
        if self.xcord < self.xleft or self.xcord > self.xright:
            self.xspeed *= -1
        if self.ycord < self.yup or self.ycord > self.ydown:
            self.yspeed *= -1
        self.rect = self.image.get_rect()
        self.rect.y = self.ycord
        self.rect.x = self.xcord
