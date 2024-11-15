import pygame
import time 
# A class to create buttons
class Button():

    def __init__(self, x, y, img, ScreenHight, ScreenWidth) -> None:
        self.image = img  # load the image of the button
        # Calculate the desired size based on the screen size
        button_width = ScreenWidth // 10
        button_height = ScreenHight // 15
        self.image = pygame.transform.scale(self.image,
                                            (button_width, button_height))  # scale the image to the desired size
        self.rect = self.image.get_rect()  # get the rectangle of the image
        self.rect.center = (x, y)  # set the position of the button
        self.clicked = False  # set the button to not clicked

    def Draw(self, window) -> bool:

        action = False  # set the action to False

        # grab the mouse position
        pos = pygame.mouse.get_pos()

        # check if the mouse is over the button
        if self.rect.collidepoint(pos):

            # if the button is clicked, set the clicked variable to True and perform the action
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                time.sleep(0.2)

            # if the button is not clicked, reset the clicked variable
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        # draw the button on the screen
        window.blit(self.image, (self.rect.x, self.rect.y))
        return action