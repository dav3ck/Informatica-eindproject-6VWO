import pygame
pygame.init()
import math

#Variable

width = 1280
height = 1024

xlines = 40
ylines = 40


name = ''
keyboard = 0

confirm = True



    #Variable Colors

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0,0,255)
yellow = (140, 0,140)
darkred = (139, 0,0) 

#Screen setup

screen = pygame.display.set_mode((width,height))
screen_rect=screen.get_rect()
pygame.display.set_caption('Level editor')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 32)
fontsmall = pygame.font.Font(None, 20)

background = pygame.image.load('Sprites/Extra/Background.png').convert()
editor = pygame.image.load('Sprites/Extra/Editor.png').convert()

#Level array setup
row = []
colum = []
Level = []
for y in range(21):
    for x in range(32):
        colum.append(0)
    row.append(colum)
    colum = []
Level.append(row)


  
#vakjes 40p x 40p dus 32 breed en 25 hoog

everything = pygame.sprite.Group() #list that will hold everything
blocks = pygame.sprite.Group()
popups = pygame.sprite.Group()

class parent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.xcord = 0
        self.ycord = 0
        self.xspeed = 0 #horizontal speed
        self.yspeed = 0 #vertical speed
        everything.add(self)

class Curser(parent):
    def __init__(self):
        super().__init__()
        self.xsize = 160
        self.ysize = 120
        self.color = green
        self.image = pygame.image.load("Sprites/Extra/CurserPlayer.png")
        self.rect = self.image.get_rect()
        self.colum = 0
        self.row = 0
        self.blockvalue = 1
        self.blocksize = True
        self.Error = False
        self.playercount = 0
        self.movingblockcord = 0
        self.sprite = ''
        self.row1 = 0
        self.colum1 = 0




    def update(self):


        #self.image = pygame.image.load(self.image)
            
        self.rect = self.image.get_rect()
        
        self.xcord = self.colum * 40
        self.ycord = self.row * 40

        self.rect.y = self.ycord
        self.rect.x = self.xcord
        


class Block(parent):
    def __init__(self, x, y, color, row, colum, sprite, row1, colum1, value):
        super().__init__()
        self.xsize = x
        self.ysize = y
        self.row = row
        self.sprite = sprite
        self.colum = colum
        self.color = color
        self.image = pygame.image.load(self.sprite)
        self.rect = self.image.get_rect()
        blocks.add(self)
        self.row1 = row1
        self.colum1 = colum1
        self.value = value


    def update(self):

        self.xcord = self.colum * 40
        self.ycord = self.row * 40 

        self.rect.y = self.ycord
        self.rect.x = self.xcord

class Popup(parent):
    def __init__(self):
        super().__init__()
        self.xcord = 500
        self.ycord = 300
        self.image = pygame.Surface([350,200])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.confirm = False
        self.text = ''
        popups.add(self)

    def update(self):
        self.rect.y = self.ycord
        self.rect.x = self.xcord

    
            
        

#functies

#Deze functie plaats de code
        
def writearray(value, row, colum):
 
    Level[0][row][colum] = value
    if value == 8:
        for x in range(2):
            for y in range(2):
                if x != 0 or y != 0:
                    Level[0][row + x][colum + y] = 'a'

    elif value == 9:
        for x in range(3):
            for y in range(4):
                if x != 0 or y != 0:
                    Level[0][row + x][colum + y] = 'a'

    elif value == 6:
        for x in range(curser.movingblockcord + 2 - colum):
            if x != 0:
                Level[0][row][colum + x] = 'b'

    elif value == 1:
        curser.playercount = curser.playercount + 1
            
#Deze functie verwijderd de code

def cleararray(row, colum):
    x = 1
    value = Level[0][row][colum]
    
    if type(value != float):
        if value != "b":
            Level[0][row][colum] = 0
    
        if value == 8:
            for x in range(2):
                for y in range(2):
                    if x != 0 or y != 0:
                        Level[0][row + x][colum + y] = 0

        elif value == 9:
            for x in range(3):
                for y in range(4):
                    if x != 0 or y != 0:
                        Level[0][row + x][colum + y] = 0

        elif value == 1:
            Level[0][row + 1][colum] = 0

        elif value == 6:
            while Level[0][row][colum + x] == "b":
                Level[0][row][colum + x] = 0
                x += 1
            
                    
#De check functie checked of iets geplaatst kan worden!

def check(value, row, colum):
    Error = False

    if value == 8:
        for x in range(2):
            for y in range(2):
                if row + x < 0 or colum + y > 31 or type(Level[0][row + x][colum + y]) is str or Level[0][row + x][colum + y] != 0 or Level[0][row + x][colum + y] == 9:
                    Error = True
                    
    elif value == 9:
        for x in range(3):
            for y in range(4):
                if row + x < 0 or colum + y > 31 or type(Level[0][row + x][colum + y]) is str or Level[0][row + x][colum + y] != 0 or Level[0][row + x][colum + y] == 9:
                    Error = True
    elif value == 1 and curser.playercount == 2:
        Error = True
    elif value == 6 and (Level[0][row][colum - 1] != 0):
        Error = True
    else:
        if Level[0][row][colum] != 0:
            Error = True
        
            
    return Error

def clearblock(row,colum):
    for block in blocks:
        if row == block.row1 and colum == block.colum1:
            pygame.sprite.Sprite.kill(block)
            
                    
                

            
            
    


def movement():
    curser.Error = False
    if curser.blockvalue == 8:
        curser.xsize = 80
        curser.ysize = 80
        curser.sprite = 'Sprites/balls/size1/type0/variation0/itteration0.png'
        curser.image = pygame.image.load("Sprites/Extra/Curser8.png")
    elif curser.blockvalue == 9:
        curser.xsize = 160
        curser.ysize = 120
        curser.sprite = 'Sprites/balls/size0/type0/variation0/itteration0.png'
        curser.image = pygame.image.load("Sprites/Extra/Curser7.png")
    elif curser.blockvalue == 1:
        curser.xsize = 40
        curser.ysize = 80
        curser.sprite = 'Sprites/Player/type0/var0/itteration0.png'
        curser.image = pygame.image.load("Sprites/Extra/CurserPlayer.png")
    elif curser.blockvalue == 7:
        curser.sprite = 'Sprites/balls/size2/type0/variation0/itteration0.png'
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")
    elif curser.blockvalue == 6:
        curser.sprite = "Sprites/Blocks/Block1.png"
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")
    elif curser.blockvalue == 5:
        curser.sprite = "Sprites/Blocks/Block2.png"
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")
    elif curser.blockvalue == 4:
        curser.sprite = "Sprites/Blocks/Block0.png"
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")
    elif curser.blockvalue == 3:
        curser.sprite = "Sprites/Blocks/Block1.png"
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")
    elif curser.blockvalue == 2:
        curser.sprite = "Sprites/Blocks/Block3.png"
        curser.xsize = 40
        curser.ysize = 40
        curser.image = pygame.image.load("Sprites/Extra/Curser.png")

    if curser.blockvalue >= 7 and curser.blockvalue <= 9:
        curser.color = green
    elif curser.blockvalue == 6:
        curser.color = white
    elif curser.blockvalue == 1:
        curser.color = green
    else:
        curser.color = yellow

    offscreen()
    curser.Error = check(curser.blockvalue, curser.row, curser.colum)
    
def offscreen():
    if curser.row > 21 - int(curser.ysize / 40) :
        curser.row = 0
    elif curser.row < 0:
        curser.row = 21 - int(curser.ysize / 40)
    if curser.colum > 32 - int(curser.xsize / 40):
        curser.colum = 0 
    elif curser.colum < 0:
        curser.colum = 32 - int(curser.xsize / 40)

def editor_value(editor_colum):
    if editor_colum != 0:
        curser.blockvalue = editor_colum

def keyboardpopup(text, editor_colum, name):
    confirm = False
    keyboardpopupvalue = 1
    for popup in popups:
        popup.text = text
    while keyboardpopupvalue == 1:
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for popup in popups:
                        popup.confirm = False
                elif event.key == pygame.K_RIGHT:
                    for popup in popups:
                        popup.confirm = True
                elif event.key == pygame.K_SPACE:
                    for popup in popups:
                        pygame.sprite.Sprite.kill(popup)
                    keyboardpopupvalue = 0
                    return popup.confirm
        screenmanage(40,40,1280,1024, editor_colum)


def screenmanage(xlines, ylines, width, height, editor_colum, name):
    everything.update()
    editor1 = pygame.image.load('Sprites/Extra/Editor.png')

    screen.fill(black)

        
    while xlines < width or ylines < (height - 184):
        pygame.draw.line(screen, white, (xlines, 0), (ylines, (height - 184)))
        if ylines <= 840:
            pygame.draw.line(screen, white, (0, ylines), (width, ylines))
        xlines += 40
        ylines += 40
    xlines = 40
    ylines = 40

    everything.draw(screen)

    pygame.draw.rect(screen, darkred, (0, 840,1280,184))
    if editor_colum == 0:
        pygame.draw.rect(screen,green, (120, 896,288,52))
    else:
        pygame.draw.rect(screen,green, (716 + (48 * editor_colum),896,52,52))
    screen.blit(editor1, (0,840))

    txt_surface = font.render(name, True, black)
    screen.blit(txt_surface, (128, 912))
    info = fontsmall.render("Press 'E' to open select menu  //  Press 'ENTER' to select object // Press 'SPACE' to place object //  Press 'R' to remove object // Press 'S' to Save & Quit ", True, black)
    screen.blit(info, (116, 974))
        
    if len(popups) > 0:
        for popup in popups:
            txt_text = font.render(str(popup.text), True, red)
            screen.blit(txt_text, (510, 350))
            txt_popup = font.render(str(popup.confirm), True, red)
            screen.blit(txt_popup, (650, 450))
            

        
    pygame.display.flip()
    

    

#Aanroepingen

curser = Curser()

        
#Echte spel

def editor():

    font = pygame.font.Font(None, 32)
    fontsmall = pygame.font.Font(None, 20)
    editor1 = pygame.image.load('Sprites/Extra/Editor.png')
    run = 1
    width = 1280
    height = 1024

    xlines = 40
    ylines = 40

    Error = pygame.mixer.Sound("Sounds/Error.wav")

    name = ''
    keyboard = 0
    editor_colum = 1

    confirm = True
    while run == 1:

        movement()

        if keyboard == 0:
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN: #handles all keypresses
                    if event.key == pygame.K_LEFT:
                        curser.colum -= 1
                    elif event.key == pygame.K_RIGHT:
                        curser.colum += 1
                    elif event.key == pygame.K_UP:
                        curser.row -= 1
                    elif event.key == pygame.K_DOWN:
                        curser.row += 1
                    elif event.key == pygame.K_SPACE:
                        print(curser.row, curser.colum)
                        if curser.Error != True:
                            if curser.blockvalue == 6:
                                keyboard = 2
                                block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, "b")
                                curser.colum -= 1
                                curser.movingblockcord = curser.colum
                            else:
                                writearray(curser.blockvalue, curser.row, curser.colum)
                                block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, 0)
                        else:
                            Error.play()
                    elif event.key == pygame.K_p:
                        print(curser.colum, curser.row)
                        print(curser.playercount)
                    elif event.key == pygame.K_c:
                        print(Level)
                    elif event.key == pygame.K_q:
                        curser.blockvalue += 1
                        print(curser.blockvalue)
                    elif event.key == pygame.K_e:
                        keyboard = 1
                        print(curser.blockvalue)
                    elif event.key == pygame.K_r:
                        clearblock(curser.row, curser.colum)
                        cleararray(curser.row, curser.colum)
                    elif event.key == pygame.K_s:
                        popup = Popup()
                        if keyboardpopup("Weet je zeker dat je klaar bent?", editor_colum, name) == True:
                            print("WE ARE THROUGH BOOIS")
                            with open('Levels.txt', 'a') as f:
                                f.write(name + "\n")
                                for x in range(21):
                                    for y in range(32):
                                        f.write(str(Level[0][x][y]))
                                    f.write("\n")
                            run = 0
                    elif event.key == pygame.K_ESCAPE:
                        run = 0
                                
                                
                            
        elif keyboard == 1:
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        keyboard = 0
                        editor_value(editor_colum)
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_LEFT:
                        editor_colum -= 1
                        if editor_colum < 0:
                            editor_colum = 9
                        print(editor_colum)
                    elif event.key == pygame.K_RIGHT:
                        editor_colum += 1
                        if editor_colum > 9:
                            editor_colum = 0
                        print(editor_colum)
                    else:
                        if len(name) < 20:
                            name += event.unicode

        elif keyboard == 2:
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and curser.Error != True:
                        if curser.colum != 0:
                            block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row1, curser.colum1, "b")
                            curser.colum -= 1
                    elif event.key == pygame.K_RIGHT:
                        if curser.colum < curser.movingblockcord:
                            curser.colum += 1
                            for block in blocks:
                                if block.colum == curser.colum and block.row == curser.row:
                                    pygame.sprite.Sprite.kill(block)
                        else:
                            for block in blocks:
                                if block.colum == curser.movingblockcord + 1:
                                    pygame.sprite.Sprite.kill(block)
                            curser.colum += 1
                            keyboard = 0
                    elif event.key == pygame.K_SPACE:
                        for block in blocks:
                            if block.value == "b":
                                block.colum1 = curser.colum
                                block.row1 = curser.row
                        block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, "b")
                        writearray(curser.blockvalue, curser.row, curser.colum)
                        keyboard = 0



        screenmanage(xlines, ylines, width, height, editor_colum, name)

        '''everything.update()
   

        screen.fill(black)

            
        while xlines < width or ylines < (height - 184):
            pygame.draw.line(screen, white, (xlines, 0), (ylines, (height - 184)))
            if ylines <= 840:
                pygame.draw.line(screen, white, (0, ylines), (width, ylines))
            xlines += 40
            ylines += 40
        xlines = 40
        ylines = 40

        everything.draw(screen)

        pygame.draw.rect(screen, darkred, (0, 840,1280,184))
        if editor_colum == 0:
            pygame.draw.rect(screen,green, (120, 896,288,52))
        else:
            pygame.draw.rect(screen,green, (716 + (48 * editor_colum),896,52,52))
        screen.blit(editor1, (0,840))

        txt_surface = font.render(name, True, black)
        screen.blit(txt_surface, (128, 912))
        info = fontsmall.render("Press 'E' to open select menu  //  Press 'ENTER' to select object // Press 'SPACE' to place object //  Press 'R' to remove object // Press 'S' to Save & Quit ", True, black)
        screen.blit(info, (116, 974))
            
        if len(popups) > 0:
            for popup in popups:
                txt_text = font.render(str(popup.text), True, red)
                screen.blit(txt_text, (510, 650))
                
        if len(popups) > 0:
            for popup in popups:
                txt_popup = font.render(str(popup.confirm), True, red)
            screen.blit(txt_popup, (510, 650))
            
        pygame.display.flip()'''
            
        
        

     
                     
    screen.fill(black)
    pygame.display.flip()
    return


    #Unimportant
    
    
