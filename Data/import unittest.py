import unittest
import pygame
from main import ship
from game_utils import LoadImage

# FILE: test_ship.py


class TestShip(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.name = "battleship"
        self.img = "images/ships/battleship/battleship.png"
        self.pos = (125, 600)
        self.size = (40, 195)
        self.test_ship = ship(self.name, self.img, self.pos, self.size)
        self.window = pygame.display.set_mode((800, 600))

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        self.assertEqual(self.test_ship.name, self.name)
        self.assertEqual(self.test_ship.vimgrect.topleft, self.pos)
        self.assertEqual(self.test_ship.himgrect.topleft, self.pos)
        self.assertFalse(self.test_ship.active)
        self.assertEqual(self.test_ship.image, self.test_ship.vimg)
        self.assertEqual(self.test_ship.rect, self.test_ship.vimgrect)
        self.assertFalse(self.test_ship.rotation)

    def test_load_images(self):
        vimg = LoadImage(self.img, self.size)
        himg = pygame.transform.rotate(vimg, -90)
        self.assertEqual(self.test_ship.vimg.get_size(), vimg.get_size())
        self.assertEqual(self.test_ship.himg.get_size(), himg.get_size())

    def test_selectshipandmove(self):
        self.test_ship.active = True
        self.test_ship.selectshipandmove()
        self.assertFalse(self.test_ship.active)

    def test_draw(self):
        self.test_ship.draw(self.window)
        # Check if the ship is drawn on the window
        self.assertEqual(self.window.get_at(self.test_ship.rect.topleft), self.test_ship.image.get_at((0, 0)))

if __name__ == '__main__':
    unittest.main()