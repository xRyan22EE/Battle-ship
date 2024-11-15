# module import
import random
import pygame
from grid import CreateGameGrid
from game_utils import LoadImage
from Buttons import Button
# module Initialization
pygame.init()

# game variables
game_started = False # variable to check if the game has started
settings_active = False


# Game Settings and Variables
ScreenWidth = 1260
ScreenHight = 960


# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


# pygame display Initialization
GameScreen = pygame.display.set_mode((ScreenWidth, ScreenHight))


# set the title of the window
pygame.display.set_caption("Battle Ship Demo")


# Game Lists/Dictionaries


# Playerf = Player Fleet Dictionary     key: [name, image path, position, size]
Playerf = {
    "carrier": ["carrier", "images/ships/carrier/carrier.png", (50, 600), 5],
    "battleship": ["battleship", "images/ships/battleship/battleship.png", (125, 600), 4],
    "cruiser": ["cruiser", "images/ships/cruiser/cruiser.png", (200, 600), 4],
    "destroyer": ["destroyer", "images/ships/destroyer/destroyer.png", (275, 600), 3],
    "submarine": ["submarine", "images/ships/submarine/submarine.png", (350, 600), 3],
    "patrol boat": ["patrol boat", "images/ships/patrol boat/patrol boat.png", (425, 600), 2],
    "rescue ship": ["rescue ship", "images/ships/rescue ship/rescue ship.png", (500, 600), 2]
}


# loading game variables


# loading game sound and Image
start_img = pygame.image.load("images/Button/start_btn.png").convert_alpha()
exit_img = pygame.image.load("images/Button/exit_btn.png").convert_alpha()
setting_img = pygame.image.load("images/Button/settings_icon.png").convert_alpha()




# game assets and objects
class ship:
    # Class variable to store all created instances
    instances = []

    def __init__(self, name: str, img: str, pos: tuple, size: tuple):
        self.name = name

        # Set the start position of the ship to the position passed in the constructor. This is the position the ship will return to if it is not placed in the grid.
        self.start_pos = pos

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

        # Append the current instance to the class variable instances
        ship.instances.append(self)

    def resize_ship(self, cell_count):
        # Update the size based on the cell count and current CellSize
        adjusted_size = (CellSize, cell_count * CellSize) if not self.rotation else (cell_count * CellSize, CellSize)
        self.vimg = pygame.transform.scale(self.vimg, adjusted_size)
        self.himg = pygame.transform.rotate(self.vimg, -90)  # Rotate for horizontal
        self.rect = self.vimg.get_rect()
        self.himgrect = self.himg.get_rect()
        self.rect.topleft = self.start_pos  # Reset to starting position if needed

    def set_grid_size(new_rows: int, new_cols: int) -> None:
        global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
        raws = new_rows
        cols = new_cols

        # Calculate CellSize based on grid dimensions
        CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws))
        # Re-create the player and computer grids
        pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
        cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

        # Resize each ship according to the new CellSize
        for ship in Playerfleet + Computerfleet:
            ship.resize_ship(Playerf[ship.name][3])  # Pass in the cell count for each ship

    def selectshipandmove(self) -> None:
        if game_started:
            return

        while self.active:
            self.rect.center = pygame.mouse.get_pos()
            UpdateGameScreen(GameScreen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.check_for_collision(Playerfleet):
                        if event.button == 1:
                            if self.CheckinGrid(pGameGrid):
                                self.snap_to_grid(pGameGrid)
                                self.himgrect.center = self.vimgrect.center = self.rect.center
                                self.active = False
                            else:
                                self.return_to_start()
                                self.active = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Rotate the ship if the space key is pressed
                    self.rotate_ship()

    def rotate_ship(self):
        # Toggle the rotation state
        self.rotation = not self.rotation

        # Update the image and rectangle based on the new orientation
        if self.rotation:
            self.image = self.himg
            self.rect = self.himgrect
        else:
            self.image = self.vimg
            self.rect = self.vimgrect
        self.rect.center = pygame.mouse.get_pos()

    def CheckinGrid(self, grid: list) -> bool:
        for row in grid:
            for col in row:
                cell_rect = pygame.Rect(col[0], col[1], CellSize, CellSize)
                if self.rect.colliderect(cell_rect):
                    return True
        return False

    def return_to_start(self) -> None:
        self.rotation = False
        self.image = self.vimg
        self.rect = self.vimgrect
        self.rect.topleft = self.start_pos
        self.vimgrect.topleft = self.start_pos
        self.himgrect.topleft = self.start_pos
        self.active = False

    def snap_to_grid(self, grid: list):
        if self.rotation:
            cells_required_x = self.rect.width // CellSize
            cells_required_y = 1
        else:
            cells_required_x = 1
            cells_required_y = self.rect.height // CellSize

        current_top_left = self.rect.topleft
        closest_cell_top_left = None
        min_distance = float("inf")

        if self.CheckinGrid(pGameGrid):
            for row in grid:
                for col in row:
                    cell_top_left_x = col[0]
                    cell_top_left_y = col[1]
                    distance = ((current_top_left[0] - cell_top_left_x) ** 2 +
                                (current_top_left[1] - cell_top_left_y) ** 2) ** 0.5

                    if distance < min_distance:
                        min_distance = distance
                        closest_cell_top_left = (cell_top_left_x, cell_top_left_y)

            if closest_cell_top_left:
                snapped_x = closest_cell_top_left[0]
                snapped_y = closest_cell_top_left[1]

                border = 530
                if self.rotation:
                    if snapped_x + cells_required_x * CellSize > border:
                        snapped_x = border - cells_required_x * CellSize
                else:
                    if snapped_y + cells_required_y * CellSize > border:
                        snapped_y = border - cells_required_y * CellSize

                if self.rotation:
                    if snapped_x + (cells_required_x * CellSize) <= ScreenWidth and snapped_y <= ScreenHight:
                        self.rect.topleft = closest_cell_top_left
                        self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                        self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                    else:
                        self.return_to_start()
                else:
                    if snapped_y + (cells_required_y * CellSize) <= ScreenHight:
                        self.rect.topleft = closest_cell_top_left
                        self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                        self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                    else:
                        self.return_to_start()

    def computer_snap_to_grid(self, grid: list):
        if self.rotation:  # Horizontal

            # Calculate the number of cells required to fit the ship
            cells_required_x = self.rect.width // CellSize

            # The ship is always 1 cell tall when horizontal
            cells_required_y = 1

        else:  # Vertical
            # The ship is always 1 cell wide when vertical
            cells_required_x = 1

            # Calculate the number of cells required to fit the ship
            cells_required_y = self.rect.height // CellSize

        # Get the top-left position of the ship
        current_top_left = self.rect.topleft

        # Initialize variables to store the closest cell's top-left position and the minimum distance
        closest_cell_top_left = None

        # Set the minimum distance to infinity to ensure the first cell is selected
        min_distance = float("inf")

        # Iterate through the grid to find the closest cell to the ship
        for row in grid:
            for col in row:
                # Get the top-left position of the current cell
                cell_top_left_x = col[0]
                cell_top_left_y = col[1]

                # Calculate the distance between the ship and the current cell
                distance = ((current_top_left[0] - cell_top_left_x) ** 2 + (
                            current_top_left[1] - cell_top_left_y) ** 2) ** 0.5
                # Pythagorean theorem (a^2 + b^2 = c^2) to calculate the distance between two points in 2D space (x, y)

                # Check if the current cell is closer to the ship than the previous closest cell
                if distance < min_distance:
                    # Update the minimum distance and the closest cell's top-left position
                    min_distance = distance

                    # Set the closest cell's top-left position to the current cell's top-left position
                    closest_cell_top_left = (cell_top_left_x, cell_top_left_y)

        # Check if a closest cell was found
        if closest_cell_top_left:
            # Get the x and y coordinates of the closest cell's top-left position
            snapped_x = closest_cell_top_left[0]
            # Get the y coordinate of the closest cell's top-left position
            snapped_y = closest_cell_top_left[1]

            # Ensure the ship does not go out of the grid boundaries
            if self.rotation:  # Horizontal
                # Check if the ship is within the grid boundaries when horizontal and snap to the closest cell if it is
                if snapped_x + cells_required_x * CellSize > ScreenWidth:
                    snapped_x = ScreenWidth - cells_required_x * CellSize
            else:  # Vertical
                # Check if the ship is within the grid boundaries when vertical and snap to the closest cell if it is
                if snapped_y + cells_required_y * CellSize > ScreenHight:
                    snapped_y = ScreenHight - cells_required_y * CellSize

            if self.rotation:  # Horizontal
                # Snap the ship to the closest cell if it is within the grid boundaries when horizontal
                if snapped_x + (cells_required_x * CellSize) <= ScreenWidth and snapped_y <= ScreenHight:
                    self.rect.topleft = closest_cell_top_left
                    self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                    self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                else:  # Return the ship to the start position if it is out of bounds
                    self.return_to_start()

            else:  # Vertical
                # Snap the ship to the closest cell if it is within the grid boundaries when vertical
                if snapped_y + (
                        cells_required_y * CellSize) <= ScreenHight:  # Check if the ship is within the grid boundaries

                    # Snap the ship to the closest cell if it is within the grid boundaries when vertical
                    self.rect.topleft = closest_cell_top_left

                    # Center the ship in the cell by setting the x and y coordinates to the center of the cell
                    self.rect.centerx = snapped_x + (cells_required_x * CellSize) // 2
                    self.rect.centery = snapped_y + (cells_required_y * CellSize) // 2
                else:  # Return the ship to the start position if it is out of bounds
                    self.return_to_start()  # Return the ship to the start position if it is out of bounds

    def check_for_collision(self, other_ships: list) -> bool:
        CopyOfShip = other_ships.copy()
        CopyOfShip.remove(self)
        for ship in CopyOfShip:
            if self.rect.colliderect(ship.rect):
                return True
        return False

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.image, self.rect)

        pygame.draw.rect(window, red, self.rect, 1)  # Debugging: red rectangle around the ship

    def is_placed_in_grid(self) -> bool:
        # Check if the ship is placed in the grid and not active

        # Return True if the ship is placed in the grid and not active, otherwise return False
        return self.CheckinGrid(pGameGrid) and not self.active

    # Debugging methods
    def __str__(self):
        return f"{self.name}: {self.rect.center} || {self.rect} || {self.vimg} || {self.himg} "
    
    @classmethod
    def view_all_instances(cls):
        for ships in cls.instances:
            print(ships)


# game utility functions
def print_game_state() -> None:
    # Function to print the current state of the game
    def create_grid_view(fleet, reference_grid): # Create a grid view with ships placed on it


        # Initialize empty grid
        Vrows = raws
        Vcols = cols

        grid = [[' .. ' for Cols in range(Vcols)] for Raws in range(Vrows)]  # Create an empty grid with dots representing empty cells in the grid (..)
        
        # Map ships to grid using grid coordinates
        for ship in fleet:

            # Calculate ship's starting grid position using the correct reference grid
            start_x = (ship.rect.x - reference_grid[0][0][0]) // CellSize
            start_y = (ship.rect.y - reference_grid[0][0][1]) // CellSize
            
            # Calculate ship length in cells
            if ship.rotation:  # Horizontal
                length_x = ship.rect.width // CellSize # Calculate the length of the ship in cells
                length_y = 1 # Ship is horizontal, so length in y is 1
            else:  # Vertical
                length_x = 1 # Ship is vertical, so length in x is 1
                length_y = ship.rect.height // CellSize # Calculate the length of the ship in cells
            
            # Fill all cells occupied by the ship

            for dx in range(length_x): # Loop through the ship's length in x
                for dy in range(length_y): # Loop through the ship's length in y

                    x = start_x + dx # Calculate the x coordinate of the cell
                    y = start_y + dy # Calculate the y coordinate of the cell

                    # Check if the cell is within the grid boundaries
                    if 0 <= x < Vcols and 0 <= y < Vrows: # Check if the cell is within the grid boundaries

                        grid[y][x] = f' {ship.name[:2]} ' # Fill the cell with the ship's name (first two characters)
        
        return grid

    def print_fleet_grid(fleet, reference_grid, title):
        print(f"\n=== {title} ===")
        
        # Print column headers
        print("   ", end="")
        for i in range(10):
            print(f"  {i} ", end="")
        print("\n")
        
        # Create and print grid with ships
        grid = create_grid_view(fleet, reference_grid)
        for row_num, row in enumerate(grid): # Loop through the grid rows

            print(f"{row_num:2d} ", end="") # Print the row number with 2 digits (e.g., 01, 02, ..., 10)

            print("".join(row)) # Print the row with ships and empty cells (..)
        
        # Print ship coordinates and lengths
        print(f"\n{title} Ship Positions:")
        
        for ship in fleet:

            # Calculate ship's starting grid position using the correct reference grid
            start_x = (ship.rect.x - reference_grid[0][0][0]) // CellSize
            start_y = (ship.rect.y - reference_grid[0][0][1]) // CellSize

            # Calculate ship length in cells
            length = ship.rect.width // CellSize if ship.rotation else ship.rect.height // CellSize

            # Print ship name, starting position, orientation, and length
            orientation = "Horizontal" if ship.rotation else "Vertical"

            # Print ship name, starting position, orientation, and length
            print(f"{ship.name:12} at ({start_x}, {start_y}) - {orientation} - Length: {length}")

        print()

    # Print both player and computer grids using their respective reference grids
    print_fleet_grid(Playerfleet, pGameGrid, "Player Grid")
    print_fleet_grid(Computerfleet, cGameGrid, "Computer Grid")

def ShowGridOnScreen(Window: pygame.surface, CellSize: int, PlayerGrid: list, ComputerGrid: list) -> None:
    # Draw the grid to the screen
    GameGrids = [PlayerGrid, ComputerGrid]

    for grid in GameGrids:
        # GameGrids = [PlayerGrid, ComputerGrid], grid = PlayerGrid or ComputerGrid
        for Row in grid:
            # Row = [Col, Col, Col, Col, Col, Col, Col, Col, Col, Col]
            for Col in Row:
                # Col = [(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y),(x, y)], Row = (x, y)

                # (window, color, (x, y, width, height), thickness)
                pygame.draw.rect(Window, white, (Col[0], Col[1], CellSize, CellSize), 1)

def randomized_computer_ships(shiplist: list, gamegrid: list) -> None:
    for ship in shiplist:
        placed = False
        while not placed:
            # Reset ship's position
            ship.return_to_start()

            # Randomly select rotation and apply it
            rotate_ship = random.choice([True, False])
            if rotate_ship:
                ship.rotate_ship()  # Rotate to horizontal if True
            else:
                ship.rotation = False  # Keep vertical

            # Get the maximum position based on grid size and ship size to avoid going out of bounds
            max_x = len(gamegrid[0]) - (ship.rect.width // CellSize if ship.rotation else 1)
            max_y = len(gamegrid) - (1 if ship.rotation else ship.rect.height // CellSize)

            # Randomly select a starting cell within the allowed bounds
            start_x = random.randint(0, max_x)
            start_y = random.randint(0, max_y)

            # Calculate the top-left position in pixels for the grid
            ship.rect.topleft = (gamegrid[start_y][start_x][0], gamegrid[start_y][start_x][1])

            # Check if this position collides with other ships in the fleet
            if not ship.check_for_collision(shiplist):
                # Snap to grid if valid, and mark as placed
                ship.computer_snap_to_grid(gamegrid)
                placed = True

def UpdateGameScreen(window: pygame.surface) -> None:
    global game_started, run_game, settings_active # Access the global game_started variable to update the game state and run_game to exit the game loop

    # Fill the window with black color
    window.fill(black)

    # Draw Grids to the screen
    ShowGridOnScreen(window, CellSize, pGameGrid, cGameGrid)

    # Draw Ships to the screen
    for ship in Playerfleet:
        ship.draw(window)
        ship.snap_to_grid(pGameGrid)

    for ship in Computerfleet:
        ship.draw(window)

    # Draw Buttons to the screen and check for button clicks to start the game or exit the game or show settings
    if all_ships_placed() and not game_started:
       if start_button.Draw(window):
            game_started = True
            print_game_state()
    
    if exit_button.Draw(window) and not settings_active:
        run_game = False
    if game_started:
        exit_button.rect.center = (ScreenWidth // 2, (ScreenHight // 2) - ScreenWidth // 10)

    if setting_button.Draw(window): 
        settings_active = not settings_active  # Toggle settings menu

    # Draw settings panel if active
    if settings_active:
        # Draw semi-transparent overlay
        overlay = pygame.Surface((ScreenWidth, ScreenHight))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        window.blit(overlay, (0, 0))
        
        # Draw settings panel
        window.blit(settings_panel, settings_panel_rect)
        


    # Update the display    
    pygame.display.update()

def createfleet() -> list:
    fleet = []
    for name, (img_name, img_path, pos, cell_count) in Playerf.items():
        # Calculate the ship size in pixels based on CellSize and cell count
        if name != "patrol boat" and name != "rescue ship":
            adjusted_size = (CellSize, cell_count * CellSize)
        else:
            adjusted_size = (CellSize*0.65, CellSize * cell_count)
        fleet.append(ship(name, img_path, pos, adjusted_size))
    return fleet

def all_ships_placed() -> bool:
    # Check if all ships are placed in the grid

    # Return True if all ships are placed in the grid, otherwise return False
    return all(ship.is_placed_in_grid() for ship in Playerfleet)

def sortfleet(ship, shiplist: list) -> None:
    # function to sort ships in the list to the top of the list when selected to show on top of other ships
    shiplist.remove(ship)
    shiplist.append(ship)

def set_grid_size(new_rows: int, new_cols: int) -> None:
    # function to set grid size and dynamically adjust cell size
    global raws, cols, CellSize, pGameGrid, pGameLogic, cGameGrid, cGameLogic
    raws = new_rows
    cols = new_cols

    # divide ScreenHight by 2 to leave space for both grids and divide by raws to get the cell size for the grid
    CellSize = min(ScreenWidth // cols, ScreenHight // (2 * raws))
    # create game grid for player and computer grid with the new raws, cols and cell size
    pGameGrid = CreateGameGrid(raws, cols, CellSize, (50, 50))
    cGameGrid = CreateGameGrid(raws, cols, CellSize, (((ScreenWidth - 50) - (cols * CellSize)), 50))

# function to handle ship selection
def handle_ship_selection() -> None:
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


# set the grid size for the game (rows, cols)
set_grid_size(10, 10)


# Button instance for start and exit button

exit_button = Button(ScreenWidth // 2, (ScreenHight // 2) + ScreenWidth // 25, exit_img, ScreenHight, ScreenWidth)
start_button = Button(ScreenWidth // 2, (ScreenHight // 2) - ScreenWidth // 10, start_img, ScreenHight, ScreenWidth)
setting_button = Button(ScreenWidth - 10, 30, setting_img, ScreenHight, ScreenWidth)
setting_button.image = pygame.transform.scale(setting_button.image, (50, 50))

settings_panel = pygame.Surface((400, 300))
settings_panel.fill((50, 50, 50))  # Dark gray background
settings_panel_rect = settings_panel.get_rect(center=(ScreenWidth//2, ScreenHight//2))


# Initialise players

    # create player fleet
Playerfleet = createfleet()

    # create computer fleet
Computerfleet = createfleet()
randomized_computer_ships(Computerfleet, cGameGrid)



# Main game loop
run_game = True

def handle_events() -> None:
    global run_game

    # for loop to handle events in the game
    for event in pygame.event.get():

        # check if the event is a quit event
        if event.type == pygame.QUIT:

            # set run_game to False for exiting the game loop
            run_game = False

        # check if the event is a mouse button down event
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # check if the mouse button pressed was the left mouse button
            if event.button == 1:
                # call the handle_ship_selection function to handle ship selection
                handle_ship_selection()

while run_game:
    handle_events()
    UpdateGameScreen(GameScreen)

pygame.quit()