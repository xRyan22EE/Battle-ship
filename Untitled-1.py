import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Image Transformation")

# Load the image
try:
    img = pygame.image.load("images/ships/battleship/battleship.png").convert_alpha()
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    sys.exit()

# Print the original image
print(img)

# Scale the image
img = pygame.transform.scale(img, (125, 600))
print(img)

# Get and print the width and height of the image
x = img.get_width()
y = img.get_height()
print(x, y)

# Rotate the image
img = pygame.transform.rotate(img, -90)
print(img)

# Get the image rectangle and set its position
Recttimg = img.get_rect()
print(Recttimg)
Recttimg.topleft = (100, 100)
print(Recttimg)

# Main loop to display the image
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen with black
    screen.blit(img, Recttimg)  # Draw the image
    pygame.display.flip()  # Update the display

pygame.quit()
