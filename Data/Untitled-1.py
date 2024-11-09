import pygame
from game_utils import LoadImage
class Ship:
    def __init__(self, name: int, img: int, pos, obj_rows, obj_cols, cell_size):
        self.img = "images/ships/battleship/battleship.png"
        self.name = name
        self.image = LoadImage(img, (obj_cols * cell_size, obj_rows * cell_size))  # Scale image to fit grid size
        self.rect = self.image.get_rect(topleft=pos)
        self.start_pos = pos
        self.obj_rows = obj_rows  # Number of rows the object occupies
        self.obj_cols = obj_cols  # Number of columns the object occupies
        self.cell_size = cell_size
        self.active = False

    def snap_to_grid(self, grid, start_x, start_y):
        """
        Snap the ship to the nearest free cells on the grid if possible.
        
        grid: 2D list representing the grid (False means free, True means occupied)
        start_x, start_y: Coordinates for the start position of the grid
        """
        grid_rows = len(grid)
        grid_cols = len(grid[0])

        # Calculate the top-left grid cell based on the ship's position
        grid_col = (self.rect.left - start_x) // self.cell_size
        grid_row = (self.rect.top - start_y) // self.cell_size

        # Boundary check: ensure object stays within grid limits
        if grid_row + self.obj_rows > grid_rows or grid_col + self.obj_cols > grid_cols:
            self.return_to_start()
            return

        # Check if the required grid cells for the object are all free
        for r in range(self.obj_rows):
            for c in range(self.obj_cols):
                if grid[grid_row + r][grid_col + c]:  # Cell is occupied
                    self.return_to_start()
                    return

        # Mark the grid cells as occupied by this object
        for r in range(self.obj_rows):
            for c in range(self.obj_cols):
                grid[grid_row + r][grid_col + c] = True

        # Snap the object to the nearest cell position
        self.rect.topleft = (start_x + grid_col * self.cell_size, start_y + grid_row * self.cell_size)

    def return_to_start(self):
        # Return the ship to its start position if snapping fails
        self.rect.topleft = self.start_pos

    def draw(self, window):
        # Draw the ship at its current position
        window.blit(self.image, self.rect)

# Example of usage

def create_grid(rows, cols):
    # Create a 2D grid (False means unoccupied, True means occupied)
    return [[False for _ in range(cols)] for _ in range(rows)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snap to Grid Example")

    cell_size = 50
    start_x, start_y = 50, 50
    rows, cols = 10, 10
    grid = create_grid(rows, cols)

    # Create a ship that occupies 2 rows by 3 columns
    ship = Ship("Battleship", "battleship.png", (100, 100), 2, 3, cell_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Activate the ship movement with mouse if clicked
                ship.active = True

        # If ship is active, move it with the mouse and snap on release
        if ship.active:
            ship.rect.center = pygame.mouse.get_pos()

            # Snap to grid on mouse release
            if pygame.mouse.get_pressed()[0] == 0:  # Left mouse button released
                ship.snap_to_grid(grid, start_x, start_y)
                ship.active = False

        # Draw everything
        screen.fill((255, 255, 255))

        # Draw the grid for reference
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(start_x + col * cell_size, start_y + row * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

        # Draw the ship
        ship.draw(screen)

        pygame.display.flip()

    pygame.quit()

main()
