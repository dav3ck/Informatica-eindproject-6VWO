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

#Lettertypes

font = pygame.font.Font(None, 32)
fontsmall = pygame.font.Font(None, 20)

#plaatjes (onderkant/ niet gebruikte achtergrond)

background = pygame.image.load('Sprites/Extra/Background.png').convert()
editor = pygame.image.load('Sprites/Extra/Editor.png').convert()

#Level array setup // Dit script maakt de array waarin het level word opgeslagen, eigenlijk plaats dit script alleen maar 0 in een array
row = [] #legen arrays
colum = []
Level = []
for y in range(21):
    for x in range(32):
        colum.append(0) #vult een colum met 32 0's
    row.append(colum) #doet deze colum in de array, en doet dit 21 keer (21 rows)
    colum = []
Level.append(row) #doet de complete array in het Level array


  
#vakjes 40p x 40p dus 32 breed en 25 hoog

everything = pygame.sprite.Group() #list that will hold everything
blocks = pygame.sprite.Group() #lijst die block sprites vasthoud
popups = pygame.sprite.Group() #lijst die popup spritees vasthoud

class parent(pygame.sprite.Sprite): #parent class met algemene waardes
    def __init__(self):
        super().__init__()
        self.xcord = 0  
        self.ycord = 0
        self.xspeed = 0 #horizontal speed
        self.yspeed = 0 #vertical speed
        everything.add(self) #voegt alles automatisch toe in de groep die alle sprites houd (handig voor alles in een keer te deleten)

class Curser(parent):
    def __init__(self):
        super().__init__()
        self.xsize = 160 #groten van curser, niet meer gebruikt zodra we curser sprite hadden
        self.ysize = 120 # ^^
        self.color = green # ^^
        self.image = pygame.image.load("Sprites/Extra/CurserPlayer.png") #laad de curser sprite in met grote van player
        self.rect = self.image.get_rect() #Dit is bij iedere sprite verplicht.
        self.colum = 0 #in welke colum de curser zit (waarde tussen 0 of 42)
        self.row = 0 #in welke row de curser zit (waarde tussen 0 en 21)
        self.blockvalue = 1 # Blockvalue geeft aan welk type object je aan het plaatsen bent, bijvoorbeeld een ladder
        self.blocksize = True
        self.Error = False #Dit is de variable die naar True veranderd word als een blok niet geplaatst mag worden.
        self.playercount = 0 #houdt bij hoeveel spelers er zijn geplaats (max 2)
        self.movingblockcord = 0 #Begin coordinaat van het moving blok
        self.sprite = ''    #Welke sprite het object heeft wat in de curser geselecteerd staat. (curser bevat informatie over welk object je kan plaatjes)
        self.row1 = 0       #Variable dat zorgt dat moving bloks verwijderd kunnen worden.
        self.colum1 = 0     #Variable die zorgt dat moving bloks verwijderd kunnen worden.




    def update(self):  #Update class van curser. Deze zorgt ervoor dat curser kan bewegen / dat grote kan veranderen


        #self.image = pygame.image.load(self.image)
            
        self.rect = self.image.get_rect() #alweer verplicht

        #hieronder word de curser op je juiste positie geplaats door gebruik te maken van de colum en row, aangezien dit bijhoudt als een soort van schaakboord waar de curser is, de * 40 zorgt ervoor dat dit dan ook vertaald
        #word naar de juiste pixel afstanden, aangezien ieder vakje 40x40 is.

        self.xcord = self.colum * 40 
        self.ycord = self.row * 40

        self.rect.y = self.ycord #dit zorgt ervoor dat de curser gemoved word.
        self.rect.x = self.xcord
        
#Object class, dit zijn de objecten die op je scherm verschijnen. Deze objecten zijn niet interactieve en zijn alleen plaatjes van de echte objecten die in de classes.py file staan.

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
        blocks.add(self) #hier worden alle objecten in een groep samen gestopt
        self.row1 = row1
        self.colum1 = colum1
        self.value = value


    def update(self):

        self.xcord = self.colum * 40
        self.ycord = self.row * 40 

        self.rect.y = self.ycord
        self.rect.x = self.xcord

class Popup(parent): #Dit is de Class waarin de popup word aangemaakt.
    def __init__(self):
        super().__init__()
        self.xcord = 500
        self.ycord = 300
        self.image = pygame.Surface([350,200])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.confirm = False #Dit is de waarde die ook op het scherm staat, dus True als je het zeker weet en false als je nog neit klaar was.
        #Dit is de tekst van de popup, dit hebben we zo gedaan inplaats van de tekst er in te hardcode, omdat dit makkelijker uitbreidbaar is.
        self.text = ''
        popups.add(self)

    def update(self):
        self.rect.y = self.ycord
        self.rect.x = self.xcord

    
            
        

#functies

#Deze functie plaats de code in de Array
        
def writearray(value, row, colum): 
 
    Level[0][row][colum] = value #Dit is de standaard plaatsing: Level(array), [0] aangezien dit nodig is. [row] in welke row de waarde geplaats moeten worden. en dan [colum] in welke colum. en zo kan je met 2 variable een gigantische grid weergeven.
    if value == 8: #als je value 8 is (wat een medium slime is) moet er naast een getal van hier is een medium slime ook nog het gebied dat de medium slime covered, gevult worden. Dit doen we zodat ze dan makkelijk kunnen kijken of er een ander object geplaats kan worden.
        for x in range(2):
            for y in range(2):
                if x != 0 or y != 0:
                    Level[0][row + x][colum + y] = 'a' #deze code vult eigenlijk een vierkantje van 2x2 met a's in de level array (aangeven dat hier een medium slime zit)

    elif value == 9: #zelfde als hierboven maar dan voor een grote slime.
        for x in range(3):
            for y in range(4):
                if x != 0 or y != 0:
                    Level[0][row + x][colum + y] = 'a'
    #Bij de code hieronder gebruiken de curser.movingblockcord om bij tehouden hoeveel grids het moving blok moet bewegen,
    #Van deze movingblockcord word dan de colum waarin het laatste blok geplaats is afgetrokken (+2) Hierdoor kunnen om alle locaties waar het moving blok beweegt, een b geplaats worden (behalven de meest rechter, dit is namelijk een 6)
    elif value == 6: # Dit is een moving blok
        for x in range(curser.movingblockcord + 2 - colum):
            if x != 0:
                Level[0][row][colum + x] = 'b'

    elif value == 1: #deze houdt bij hoeveel spelers er zijn.
        curser.playercount = curser.playercount + 1
            
#Deze functie verwijderd de code uit de array (als je dus een object weghaalt omdat je het daar niet wilt hebben)

def cleararray(row, colum):
    x = 1
    value = Level[0][row][colum] #pakt de value van de grid die geleegt moet worden
    
    if type(value != float): #In het begin werkte we met Decimale getallen om bijvoorbeeld een gebied gecovered door een slime aan te geven, wij zijn echter later overgestapt naar letters, wat deze line dus onnodig maakt. 
        if value != "b" and value!= "a": #zolang deze value niet gelijk is aan b & a word die niet verwijderd
            Level[0][row][colum] = 0
    
        if value == 8: #Dit het omgekeerde van de writearray functie voor waarde 8, wel op dezelfde manier.
            for x in range(2):
                for y in range(2):
                    if x != 0 or y != 0:
                        Level[0][row + x][colum + y] = 0

        elif value == 9: # ^^
            for x in range(3):
                for y in range(4):
                    if x != 0 or y != 0:
                        Level[0][row + x][colum + y] = 0

        elif value == 1: #als het de speler is (die 1x2 is) moet ook nog grid onder selecteerde plek weggehaalt worden.
            Level[0][row + 1][colum] = 0

        elif value == 6: #Dit verwijderd alle B's uit de lijst (dus in eenkeer hele moving blok verwijderen)
            while Level[0][row][colum + x] == "b": #zolang de volgende een B is, moet deze geleegt worden, en nog een verder gekeken worden of deze ook een B is.
                Level[0][row][colum + x] = 0
                x += 1 #hier word x dus verhoogd om nog een grid verder te kijken.
            
                    
#De check functie checked of iets geplaatst kan worden!

def check(value, row, colum):
    Error = False #eerst reset je iedere keer de Error naar False, voordat je gaat checken

    if value == 8: #hier kijkt hij of het gehele gebied wat een medium slime zou coveren vrij is, anders word Error = True
        for x in range(2):
            for y in range(2):
                if row + x < 0 or colum + y > 31 or type(Level[0][row + x][colum + y]) is str or Level[0][row + x][colum + y] != 0 or Level[0][row + x][colum + y] == 9:
                    Error = True
                    
    elif value == 9: #zelfde voor Big slime
        for x in range(3):
            for y in range(4):
                if row + x < 0 or colum + y > 31 or type(Level[0][row + x][colum + y]) is str or Level[0][row + x][colum + y] != 0 or Level[0][row + x][colum + y] == 9:
                    Error = True
    elif value == 1 and curser.playercount == 2: #Dit controleerd dat er niet al 2 spelers geplaats zijn (aangezien dit het limiet is)
        Error = True
    elif value == 1 and Level[0][row + 1][colum] != 0: #kijkt of er ook ruimte onder de speler is, aangezien deze 2x1 is en je maar 1 blokje tegelijkertijd kan checken.
        Error = True
    elif value == 6 and (Level[0][row][colum - 1] != 0): #Dit kijkt of de volgende ook beschikbaar is tijdens het plaatsen van een moving block.
        Error = True
    else:
        if Level[0][row][colum] != 0: #als allerlaatste word gekeken of het blok waar jij iets wil plaatsen vrij is.
            Error = True
        
            
    return Error #return de Error

def clearblock(row,colum): #Deze functie verwijderd de objecten zelf, naast dat ze uit de array gehaalt worden door de cleararray functie
    for block in blocks: #voor alle blokken in de blokkenlijst
        if row == block.row1 and colum == block.colum1: #kijk of de colum/row waar de curser nu opstaat overeenkomt met de colum/row waar een blok opgeplaatst is.
            pygame.sprite.Sprite.kill(block)
            
                    #hierboven maken we echter gebruik van de row1/colum1 variable ipv de normale row/colum variable. de row1/colum1 variable zijn biezonder omdat die niet altijd de exacte locatie weergeven waar een blokstaat.
                    #zoals de normale row/colum wel altijd aan, omdat de locatie van het object daarvan afhankelijk is. Dit is dus heel nuttig bij bijvoorbeeld de moving platform in een keer te kunnen verwijderen, 
                    #De objecten waaruit dit moving platform bestaat, zijn allemaal verschillende objecten. Maar hebben allemaal dezelfde row1/colum1 waarde -> in een keer te verwijderen. Slim he ;-)
                

            
            
    


def movement():  #Deze functie geeft de curser te juiste informatie die bij een bepaalde waarde hoort (zoals sprite/ grote/ kleur, toen we kleur en grote nog gebruikte / etc)
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

    offscreen() #Roept de offscreen fucntie aan
    curser.Error = check(curser.blockvalue, curser.row, curser.colum) #roept de functie aan die kijkt of er error zijn

#De offscreen functie kijkt als je bijvoorbeeld je curser groter maakt (bij het selecteren van een large slime) dat je curser dan niet half buiten het veld komt. En als dit wel gebeurd, word de curser aan de andere kant van het scherm gezet
#Dit gebeurd door de Curser size door 40 te delen (aantal pixels van een grid), dan weet je hoeveel grids hij boven een rand moet staan om te zorgen dat hij er niet buiten valt.
    
def offscreen():
    if curser.row > 21 - int(curser.ysize / 40) :
        curser.row = 0
    elif curser.row < 0:
        curser.row = 21 - int(curser.ysize / 40)
    if curser.colum > 32 - int(curser.xsize / 40):
        curser.colum = 0 
    elif curser.colum < 0:
        curser.colum = 32 - int(curser.xsize / 40)

def editor_value(editor_colum): #omzettings functie van curser.blockvalue naar editor_colum. ook zorgt dit dat editor_colum Niet 0 mag zijn, aangezien deze geen object aan zich gekoppelt heeft. Als dit wel zo is word waarde omgezet naar 1 ipv 0
    if editor_colum != 0:
        curser.blockvalue = editor_colum
    else:
        curser.blockvalue = 1

def keyboardpopup(text, editor_colum, name): #Dit is de functie die helpt bij de popup.
    confirm = False
    keyboardpopupvalue = 1
    for popup in popups:
        popup.text = text
    while keyboardpopupvalue == 1: #hier word een nieuwe while loop begonnen (zolang keyboardpopupvalue 1 is blijft hij runnen). Dus dit is een functie die lang blijft lopen
        for event in pygame.event.get(): #handles closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for popup in popups:
                        popup.confirm = False #als je naar links pijltjes toets indrukt, word de confirm false (dus nee)
                elif event.key == pygame.K_RIGHT:
                    for popup in popups:
                        popup.confirm = True #bij recht word waarde true
                elif event.key == pygame.K_SPACE:
                    for popup in popups:  #Bij spatie returned hij je waarde, en killed het programma de aangemaakte popup sprite (dus popup sluit af)
                        pygame.sprite.Sprite.kill(popup)
                    keyboardpopupvalue = 0
                    return popup.confirm
        screenmanage(40,40,1280,1024, editor_colum, name) #roept screen management functie aan


#Deze functie print alle benodigde informatie en dingen op het scherm.

def screenmanage(xlines, ylines, width, height, editor_colum, name):
    everything.update() #met de everything.update() functie worden alle updates die bij de classes stonden uitgevoerd die in de groep everything zitten (dus met andere woorden alles)
    editor1 = pygame.image.load('Sprites/Extra/Editor.png') #Plaatje

    screen.fill(black) #word het scherm weer geleegd (moet eerdere frame gebeuren)

        
    while xlines < width or ylines < (height - 184): #Dit plaats de lijnen die je op het scherm zit, en het scherm in grids verdeelt, 184 is de eind waarde waaronder de lijnen dus niet mogen komen: daar is de editor menu
        pygame.draw.line(screen, white, (xlines, 0), (ylines, (height - 184)))
        if ylines <= 840: 
            pygame.draw.line(screen, white, (0, ylines), (width, ylines)) #tekent lijnen
        xlines += 40
        ylines += 40
    xlines = 40
    ylines = 40
 
    everything.draw(screen) #hier worden alle sprites uit de everything group getekent.

    pygame.draw.rect(screen, darkred, (0, 840,1280,184)) #Dti plaats onder de editor menu een donker rood vlak, wat ook te zien is bij niet geselecteerde objecten.
    if editor_colum == 0:
        pygame.draw.rect(screen,green, (120, 896,288,52)) #Als de geselecteerde editor_colum = 0 is, betekend dit dat het gehighlide vak nu het name type vak is. Dus word daar nu een groen vierkant onder geplaatst
    else: #de eerste 2 getellen zijn de coordinaten, en de laaste 2 de grootte (bij de pygame.draw.rect functie)
        pygame.draw.rect(screen,green, (716 + (48 * editor_colum),896,52,52)) #als het niet 0 is betekend dat dat het 1 tm 9 is. Dus de colum waar je nu op zit * 48 (zoveel moet het groene vierkantje opschuiven om het volgende item te selectren) + begin waarde
    screen.blit(editor1, (0,840)) #tekent het op het scherm, belangrijk: dit staat boven de darkred squar, zodat hij ook daarboven word geblit en niet andersom, anders was het groene squar nooit te zien.

    txt_surface = font.render(name, True, black) #dit is de naam die in het naam hokje gedisplayed word
    screen.blit(txt_surface, (128, 912))
    info = fontsmall.render("Press 'E' to open select menu  //  Press 'ENTER' to select object // Press 'SPACE' to place object //  Press 'R' to remove object // Press 'S' to Save & Quit ", True, black)
    screen.blit(info, (116, 974)) #Dit zijn de instructies die onder het naam hokje worden geplaats, maar dan in een kleiner lettertype

    
    if len(popups) > 0: #Dit gebeurd alleen als er dus minimaal een popup object is -> met andere woorden als er één popup is. Dan word de False or true dus geblit, en de vraag of je klaar bent word geblit.
        for popup in popups:
            txt_text = font.render(str(popup.text), True, red)
            screen.blit(txt_text, (510, 350))
            txt_popup = font.render(str(popup.confirm), True, red)
            screen.blit(txt_popup, (650, 450))
            

        
    pygame.display.flip() #standaard flip functie
    

    

#Aanroepingen

curser = Curser() #hier word de curser eenmalig aangemaakt

        
#Echte spel (in functie in verband met main menu)

def editor():

        
    font = pygame.font.Font(None, 32)
    fontsmall = pygame.font.Font(None, 20)
    editor1 = pygame.image.load('Sprites/Extra/Editor.png')
    run = 1 #zolang dit 1 is blijft de while game loop runnen
    width = 1280 #grote scherm
    height = 1024

    xlines = 40 #grote lijnen
    ylines = 40

    Error = pygame.mixer.Sound("Sounds/Error.wav") #error sound

    name = '' #legen naam
    keyboard = 0 #welk keyboard er gebruikt moet worden -> welke toetsen beschikbaarzijn
    editor_colum = 1

    curser.playercount = 0
    
    

    confirm = True
    while run == 1: #gameloop

        movement() #movement functie 

        if keyboard == 0:
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN: #handles all keypresses
                    if event.key == pygame.K_LEFT:
                        curser.colum -= 1
                    elif event.key == pygame.K_RIGHT:
                        curser.colum += 1 #links en rechts de colums
                    elif event.key == pygame.K_UP:
                        curser.row -= 1 #omhoog en omlaag ga je de rows af
                    elif event.key == pygame.K_DOWN:
                        curser.row += 1
                    elif event.key == pygame.K_SPACE:
                        if curser.Error != True: #zolang er geen error is 
                            if curser.blockvalue == 6: #als de object value 6 is. word er geswitch naar keyboard 2 
                                keyboard = 2
                                block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, "b") #inspawnen van een block , array word pas later veranderd bij value 6.
                                curser.colum -= 1 #je curser word opzij geplaats 
                                curser.movingblockcord = curser.colum #De movingblockcord word gezet naar de curser.colum waar je op dat moment bent.
                            else: #alle andere waardes naast 6
                                writearray(curser.blockvalue, curser.row, curser.colum) #word in array geschreven
                                block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, 0) #word een blokgeplaats
                        else:
                            Error.play() #als error = True, dan word er een error sound geplayed
                    elif event.key == pygame.K_p: #debug keys
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
                    elif event.key == pygame.K_r: #Key die word gebruikt bij verwijderen van objecten, wegens bijvoorbeeld een fout 
                        clearblock(curser.row, curser.colum)
                        cleararray(curser.row, curser.colum)
                    elif event.key == pygame.K_s: #Save key
                        popup = Popup() #popup class word aangemaakt
                        if keyboardpopup("Weet je zeker dat je klaar bent?", editor_colum, name) == True: #als uit de keyboardpopup functie True komt, kan je doorgaan. anders niet
                            with open('Levels.txt', 'a') as f: #Level word hier opgeslagen in een .txt bestand.
                                f.write(name + "\n")
                                for x in range(21):
                                    for y in range(32):
                                        f.write(str(Level[0][x][y]))
                                    f.write("\n")
                            run = 0 #Run word naar 0 gezet dus while loop stopt
                    elif event.key == pygame.K_ESCAPE: #Escape key om altijd terug te gaan.
                        popup = Popup() #popup class word aangemaakt
                        if keyboardpopup("weg, zonder save?", editor_colum, name) == True: #als uit de keyboardpopup functie True komt, kan je doorgaan. anders niet
                            run = 0
                                
                                
                            
        elif keyboard == 1: #als keyboard naar 1 word gezet, Dit gebeurd als je in het editor menu zit
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        keyboard = 0
                        editor_value(editor_colum)
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1] #haalt een letter weg bij naam
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
                        if len(name) < 20: #20 is maxlengthe van levelnaam
                            name += event.unicode  #dit registreerd keypressed en doet ze in de naam string

        elif keyboard == 2: #Dit is de moving platform plaatsing Keyboard( je kan alleen naar links/rechts)
            for event in pygame.event.get(): #handles closing the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and curser.Error != True: 
                        if curser.colum != 0:
                            block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row1, curser.colum1, "b") #zo mogelijk word er een blok geplaatst
                            curser.colum -= 1 #je word weer een grid terug gezet
                    elif event.key == pygame.K_RIGHT:
                        if curser.colum < curser.movingblockcord: #Dit kijkt of je al voorbij de lengte bent van waar je begon > zo ja, ga uit keyboard 2 en terug naar normal editor
                            curser.colum += 1
                            for block in blocks:
                                if block.colum == curser.colum and block.row == curser.row:
                                    pygame.sprite.Sprite.kill(block) #verwijderd een blok (dus als je terug naar recht gaat)
                        else: #terug naar keyboard 1
                            for block in blocks:
                                if block.colum == curser.movingblockcord + 1:
                                    pygame.sprite.Sprite.kill(block)
                            curser.colum += 1
                            keyboard = 0
                    elif event.key == pygame.K_SPACE: #Je maakt de moving platform path af, en gaat terug naar keyboard 0
                        for block in blocks:
                            if block.value == "b":
                                block.colum1 = curser.colum #Dit geeft alle van de moving platform dezelfde waarden als het hoofd.
                                block.row1 = curser.row
                        block = Block(curser.xsize, curser.ysize, curser.color, curser.row, curser.colum, curser.sprite, curser.row, curser.colum, "b")
                        writearray(curser.blockvalue, curser.row, curser.colum)
                        keyboard = 0



        screenmanage(xlines, ylines, width, height, editor_colum, name) #Screenmanige function

            
    
     
                     
    screen.fill(black) #als je uit de While loop bent, word het scherm nog eenkeer helemaal zwart gemaakt
    return #ga terug naar hoofdmenu


    #Unimportant
    
    
