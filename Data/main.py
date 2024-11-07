# module import
import pygame
from grid import CreateGameGrid, UpdateGameLogic
from game_utils import LoadImage
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
        
        # ship selection 
        self.active = False

        # Image and rectangle 
        self.image = self.vimg
        self.rect = self.vimgrect
        self.rotation = False
    
    
    def selectshipandmove(self):
        while self.active:

            # sets the center of self.rect to follow the current position of the mouse. This means the ship tied to self.rect will move with the mouse.
            self.rect.center = pygame.mouse.get_pos()
            UpdateGameScreen(GameScreen)
            for event in pygame.event.get():

                # checks if a mouse button was pressed.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if not self.check_for_ollision(Playerfleet):
                        
                        # further checks if it was the left mouse button (button 1).
                        if event.button == 1:

                            # aligns the center of two rectangles, self.himgrect and self.vimgrect, to the center of self.rect
                            self.himgrect.center = self.vimgrect.center = self.rect.center

                            # exits the loop, as self.active is now False, ending the movement of the ship.
                            self.active = False

    def check_for_ollision(self, other_ships):
        # check for collision between two ships

        # Create a copy of the other ships
        CopyOfShip = other_ships.copy()

        # Remove the current ship from the list
        CopyOfShip.remove(self)

        # Check for collision between the current ship and the other ships in the list 
        for ship in CopyOfShip:

            # Check if the current ship rectangle collides with the other ship rectangle
            if self.rect.colliderect(ship.rect):

                # Return True if there is a collision
                return True
            
        # Return False if there is no collision
        return False

    def draw(self, window):
        # Draw the ship 
        window.blit(self.image, self.rect) # Draw the ship to the screen

# game utility function 
def ShowGridOnScreen(Window, CellSize, PlayerGrid, ComputerGrid):
    # Draw the grid to the screen
    GameGrids = [PlayerGrid, ComputerGrid]

    for grid in GameGrids:
        # GameGrids = [PlayerGrid, ComputerGrid], grid = PlayerGrid or ComputerGrid
        for Row in grid:
            # Row = [Col, Col, Col, Col, Col, Col, Col, Col, Col, Col]
            for Col in Row:
                # Col = [(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y)], Row = (x, y)

                # (window, color, (x, y, width, height), thickness)
                pygame.draw.rect(Window, (255, 255, 255), (Col[0], Col[1], CellSize, CellSize), 1)
                

def printtest():
    print(" Player grid ".center(50, "#"))
    for i in pGameLogic:
        print(i)
    
    print(" computer grid ".center(50, "#"))
    for i in cGameLogic:
        print(i)

def UpdateGameScreen(window):

    # Fill the window with black color
    window.fill((0, 0, 0))
    
    # Draw Grids to the screen
    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

    # Draw Ships to the screen 
    for ship in Playerfleet:
        ship.draw(window)

    # Update the display
    pygame.display.update()

def createfleet():
    # create fleet of ships
    fleet = []
    for name in Playerf.keys():
        fleet.append(
            ship(name, 
            Playerf[name][1],
            Playerf[name][2],
            Playerf[name][3])
        )
    return fleet


def sortfleet(ship, shiplist):
    # function to sort ships in the list to the top of the list when selected to show on top of other ships
    shiplist.remove(ship)
    shiplist.append(ship)

def set_grid_size(new_rows, new_cols):
    # function to set grid size and dynamically adjust cell size
    global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
    raws = new_rows
    cols = new_cols

    # divide ScreenHight by 2 to leave space for both grids and divide by raws to get the cell size for the grid
    CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws)) 
    # create game grid for player and computer grid with the new raws, cols and cell size
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
 # set the title of the window

# Game Lists/Dictionaries
    # Playerf = Player Fleet Dictionary     key: [name, image path, position, size]
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

 # set the grid size for the game (rows, cols)
set_grid_size(10, 10)
    
     # create player fleet
Playerfleet = createfleet()
    
        # create computer fleet
Computerfleet = None

printtest()

# loading game sound Image



# Initialise players 



# Main game loop 
run_game = True
def handle_events():
    global run_game

    # for loop to handle events in the game 
    for event in pygame.event.get():

        # check if the event is a quit event 
        if event.type == pygame.QUIT:

            # set run_game to False to exit the game loop
            run_game = False
        
        # check if the event is a mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # check if the mouse button pressed was the left mouse button
            if event.button == 1:
                # call the handle_ship_selection function to handle ship selection
                handle_ship_selection()

# function to handle ship selection
def handle_ship_selection():

    # for loop to iterate through the player fleet
    for i in Playerfleet:

        # check if the mouse position is within the rectangle of the ship
        if i.rect.collidepoint(pygame.mouse.get_pos()):

            # set the ship to active
            i.active = True

            # sort the ship to the top of the list to show on top of other ships
            sortfleet(i, Playerfleet)

            # move the ship to the mouse position and update the game screen
            i.selectshipandmove()

while run_game:
    handle_events()
    UpdateGameScreen(GameScreen)

pygame.quit()
