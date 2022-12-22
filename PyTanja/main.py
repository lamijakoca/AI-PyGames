import pygame
import traceback
from game import Game

try:
    pygame.init()
    game = Game()
    game.run()

except(Exception):
    traceback.print_exc()
    input()
finally:
    pygame.quit()
