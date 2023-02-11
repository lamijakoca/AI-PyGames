import os

GAME_FOLDER = os.path.dirname(__file__)
IMAGES_FOLDER = os.path.join(GAME_FOLDER, 'images')
MAPS_FOLDER = os.path.join(GAME_FOLDER, 'maps')

MAX_HEIGHT = 600
MAX_WIDTH = 1300    
HEIGHT = None
WIDTH = None
SPEED = None

TIME = [((255 * i) / 100, (255 * (100 - i)) / 100, 0) for i in range(101)]

TILE_SIZE = None
FONT = None
RIBBON_HEIGHT = None

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (90, 171, 97)
RED = (236, 72, 66)