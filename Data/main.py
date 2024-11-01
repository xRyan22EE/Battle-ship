# module import
import pygame

# module Initialization 
pygame.init()

# game assets and objects 
class ship:
    def __init__(self, name, img, pos, size):
        self.name = name

        # Load the Vertical Image.
        self.vimg = LoadImage(img, size)
        self.vimgwidth = self.vimg.get_width()
        self.vimgheight = self.vimg.get_height()
        self.vimgrect = self.vimg.get_rect()
        self.vimgrect.topleft = pos

        # Load the Horizontal Image.
        self.himg = pygame.transform.rotate(self.vimg, -90)
        self.himgwidth = self.himg.get_width()
        self.himgheight = self.himg.get_height()
        self.himgrect = self.himg.get_rect()
        self.himgrect.topleft = pos

        # Image and rectangle 
        self.image = self.vimg
        self.rect = self.vimgrect
        self.rotation = False
    
    def draw(self, window):
        # Draw the ship 
        window.blit(self.image, self.rect)

# game utility function 
def CreateGameGrid(rows, cols, CellSize, pos):
    # create game grid with coordinate for each cell 
    startx = pos[0]
    starty = pos[1]
    CoordGrid = []

    for row in range(rows):
        rowx = []
        for col in range(cols):
            rowx.append((startx, starty))
            startx += CellSize
        CoordGrid.append(rowx)
        startx = pos[0]
        starty += CellSize

    return CoordGrid

def UpdateGameLogic(rows, cols):
    # Update the game grid with logic, ie - spaces and X for ships
    game_logice = []
    for row in range(rows):
        rowx = []
        for col in range(cols):
            rowx.append(" ")
        game_logice.append(rowx)
        
    return game_logice

def ShowGridOnScreen(Window, CellSize, PlayerGrid, ComputerGrid):
    GameGrids = [PlayerGrid, ComputerGrid]
    for grid in GameGrids:
        for Row in grid:
            for Col in Row:
                pygame.draw.rect(Window, (255, 255, 255), (Col[0], Col[1], CellSize, CellSize), 1)

def printtest():
    print(" Player grid ".center(50, "#"))
    for i in pGameLogic:
        print(i)
    
    print(" computer grid ".center(50, "#"))
    for i in cGameLogic:
        print(i)

def UpdateGameScreen(window):
    window.fill((0, 0, 0))

    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

    # Draw Ships to the screen 
    for ship in Playerfleet:
        ship.draw(window)

    pygame.display.update()

def LoadImage(path, size, rotate=False):
    # A function to import Images Into memory
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate:
        img = pygame.transform.rotate(img, -90)
    return img

def createfleet():
    fleet = []
    for name in Playerf.keys():
        fleet.append(
            ship(name, 
            Playerf[name][1],
            Playerf[name][2],
            Playerf[name][3])
        )
    return fleet

def set_grid_size(new_rows, new_cols):
    # function to set grid size and dynamically adjust cell size
    global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
    raws = new_rows
    cols = new_cols

    # divide ScreenHight by 2 to leave space for both grids
    CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws)) 
    pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
    pGameLogic = UpdateGameLogic(raws, cols)
    cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))
    cGameLogic = UpdateGameLogic(raws, cols)

# Game Settings and Variables
ScreenWidth = 1260 
ScreenHight = 960

# colors 



# pygame display Initialization 
GameScreen = pygame.display.set_mode((ScreenWidth, ScreenHight))
pygame.display.set_caption("Battle Ship Demo")

# Game Lists/Dictionaries
Playerf = {
    "battleship": ["battleship", "images/ships/battleship/battleship.png", (125, 600), (40, 195)],

    "cruiser": ["cruiser", "images/ships/cruiser/cruiser.png", (200, 600), (40, 195)],

    "destroyer": ["destroyer", "images/ships/destroyer/destroyer.png", (275, 600), (30, 145)],

    "patrol boat": ["patrol boat", "images/ships/patrol boat/patrol boat.png", (425, 600), (20, 95)],

    "submarine": ["submarine", "images/ships/submarine/submarine.png", (350, 600), (30, 145)],

    "carrier": ["carrier", "images/ships/carrier/carrier.png", (50, 600), (45, 245)],

    "rescue ship": ["rescue ship", "images/ships/rescue ship/rescue ship.png", (500, 600), (20, 95)]
}

# loading game variables 
set_grid_size(10, 10)
Playerfleet = createfleet()
Computerfleet = None

printtest()

# loading game sound Image



# Initialise players 



# Main game loop 
RunGame = True
while RunGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False
    UpdateGameScreen(GameScreen)

pygame.quit()
