import pygame

# Create a game grid with rows, columns, cell size, and starting position
def CreateGameGrid(rows, cols, CellSize, pos):
    startx, starty = pos
    CoordGrid = []

    # Generate grid coordinates for each cell
    for row in range(rows):
        rowx = []
        for col in range(cols):
            rowx.append((startx, starty))
            startx += CellSize  # Move to next cell in row
        CoordGrid.append(rowx)
        startx = pos[0]  # Reset x position for new row
        starty += CellSize  # Move to the next row

    return CoordGrid

# Initialize game logic grid with empty spaces
def UpdateGameLogic(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Render grids on the screen, drawing cell borders for PlayerGrid and ComputerGrid
def ShowGridOnScreen(Window, CellSize, PlayerGrid, ComputerGrid):
    GameGrids = [PlayerGrid, ComputerGrid]
    for grid in GameGrids:
        for Row in grid:
            for Col in Row:
                pygame.draw.rect(Window, (255, 255, 255), (Col[0], Col[1], CellSize, CellSize), 1)
