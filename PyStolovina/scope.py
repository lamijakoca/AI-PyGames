import configuration
import pygame
import random
import os

class Sprite(pygame.sprite.Sprite):
    images = dict()
    def __init__(self, position, file_name, color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in Sprite.images:
            self.image = Sprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(configuration.IMAGES_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (configuration.TILE_SIZE, configuration.TILE_SIZE))
            Sprite.images[file_name] = self.image
        self.rect = self.image.get_rect()
        self.row = None
        self.col = None
        self.place_to(position)
        

    def position(self):
        return self.row, self.col

    def place_to(self, position):
        self.row = position[0]
        self.col = position[1]
        self.rect.x = self.col * configuration.TILE_SIZE
        self.rect.y = self.row * configuration.TILE_SIZE

    @staticmethod
    def kind():
        pass

class Tile(Sprite):
    def __init__(self, position, file_name):
        super(Tile, self).__init__(position, file_name, configuration.GREEN)


# only valid route for agent
class Road(Tile):
    def __init__(self, position):
        super().__init__(position, 'road.png')

    @staticmethod
    def kind():
        return 'r'

class Hole(Tile):
    def __init__(self, position):
        super().__init__(position, f'hole{random.randint(0, 9)}.png')

    @staticmethod
    def kind():
        return 'h'

class Goal(Tile):
    def __init__(self, position):
        super().__init__(position, 'x.png')
    
    @staticmethod
    def kind():
        return 'x'