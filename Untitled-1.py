# module import
import pygame

# module Initialization 
pygame.init()


# game assets and objects 

class ship:
    def __init__(self, name, img, pos, size, NumberOfGun = 0, GunPath = None, gunsize = None, guncoordsoffset = None):
        self.name = name

        # Load the Vertical Imge.

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

        self.image =  self.vimg
        self.rect = self.vimgrect
        self.rotation = False
    
    def draw(self, window):
        # Draw the ship 
        window.blit(self.image, self.rect)



# game utility function 
def CreateGameGrid(rows, cols, CellSize, pos):
    #create game grid with coordinate for each cell 

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

def UpdateGameLogic(rows, cols ,):
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
    for gird in GameGrids:
        for Row in gird:
            for Col in Row:
                pygame.draw.rect(Window, (255, 255, 255), (Col[0], Col[1], CellSize, CellSize), 1)

def printtest():
    print(" Player grid ".center(50,"#"))
    for i in pGameLogic:
        print(i)
    
    print(" computer grid ".center(50,"#"))
    for i in cGameLogic:
        print(i)

def UpdateGameScreen(window):
    window.fill((0, 0, 0))

    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

    # Draw Ships to the screen 
    for ship in Playerfleet:
        ship.draw(window)


    pygame.display.update()

def LoadImage(path, size, rotate = False):
    # A function to import Images Into memory
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img,size)
    if rotate:
        img = pygame.transform.rotate(img,-90)
    return img

def createfleet():
    fleet = []
    for name in Playerf.keys():
        fleet.append(
            ship(name, 
            Playerf[name][1],
            Playerf[name][2],
            Playerf[name][3],
            Playerf[name][4],
            Playerf[name][5],
            Playerf[name][6],
            Playerf[name][7])
        )
    return fleet





#  Game Settings and Variables
ScreenWidth = 1260 
ScreenHight = 960
raws = 10
cols = 10
CellSize = 50


# colors 


# pygame display Initialization 
GameScreen = pygame.display.set_mode((ScreenWidth, ScreenHight))
pygame.display.set_caption("Battle Ship Demo")

# Game Lists/Dictionaries
Playerf = {
    "battleship": ["battleship", "images/ships/battleship/battleship.png", (125, 600), (40, 195), 4, "images/ships/battleship/battleshipgun.png", (0.4, 0.125), [-0.525, -0.34, 0.67, 0.49]],

    "cruiser": ["cruiser", "images/ships/cruiser/cruiser.png", (200, 600), (40, 195), 2, "images/ships/cruiser/cruisergun.png", (0.4, 0.125), [-0.36, 0.64]],

    "destroyer": ["destroyer", "images/ships/destroyer/destroyer.png", (275, 600), (30, 145), 2, "images/ships/destroyer/destroyergun.png", (0.5, 0.15), [-0.52, 0.71]],

    "patrol boat": ["patrol boat", "images/ships/patrol boat/patrol boat.png", (425, 600), (20, 95), 0, "", None, None],

    "submarine": ["submarine", "images/ships/submarine/submarine.png", (350, 600), (30, 145), 1, "images/ships/submarine/submarinegun.png", (0.25, 0.125), [-0.45]],

    "carrier": ["carrier", "images/ships/carrier/carrier.png", (50, 600), (45, 245), 0, "", None, None],

    "rescue ship": ["rescue ship", "images/ships/rescue ship/rescue ship.png", (500, 600), (20, 95), 0, "", None, None]

}

# loading game variables 
pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
pGameLogic = UpdateGameLogic(raws, cols)
Playerfleet = createfleet()

cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth-50)-(raws * CellSize)),50))
cGameLogic = UpdateGameLogic(raws, cols)
Computerfleet = None

printtest()

# loading game sound Image




# Initialise players 

# Track if a ship is being dragged and store the selected ship
dragging_ship = None
offset_x = 0
offset_y = 0

# Updated snap_to_grid function
def snap_to_grid(ship, grid, cell_size):
    # Find the top-left position of the closest cell based on ship's current position
    closest_cell_x = round((ship.rect.x - grid[0][0][0]) / cell_size) * cell_size + grid[0][0][0]
    closest_cell_y = round((ship.rect.y - grid[0][0][1]) / cell_size) * cell_size + grid[0][0][1]

    # Set the ship's position to the closest cell's top-left corner
    ship.rect.topleft = (closest_cell_x, closest_cell_y)

# Main game loop
RunGame = True
while RunGame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for ship in Playerfleet:
                    if ship.rect.collidepoint(event.pos):  # Check if clicked on a ship
                        dragging_ship = ship  # Store the selected ship
                        mouse_x, mouse_y = event.pos
                        offset_x = ship.rect.x - mouse_x
                        offset_y = ship.rect.y - mouse_y
                        break  # Stop after finding the ship being dragged

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                if dragging_ship:  # If a ship was being dragged
                    snap_to_grid(dragging_ship, pGameGrid, CellSize)  # Snap it to the closest grid cell
                dragging_ship = None  # Stop dragging

        elif event.type == pygame.MOUSEMOTION:
            if dragging_ship:  # Only update if a ship is being dragged
                mouse_x, mouse_y = event.pos
                dragging_ship.rect.x = mouse_x + offset_x
                dragging_ship.rect.y = mouse_y + offset_y

    # Update the display each frame
    UpdateGameScreen(GameScreen)

pygame.quit()
