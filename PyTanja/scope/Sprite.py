import configuration
import pygame
import os

class Sprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file, color=None) -> None:
        super().__init__(self)

        if file in Sprite.images:
            self.image = Sprite.images[file]
        else:
            self.image = pygame.image.load(os.path.join(configuration.IMAGES_FOLDER, file))
            #self.image = pygame.transform.scale(self.image, (configuration.TILE_SIZE, configuration.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = (col, row)
        self.row = row
        self.col = col