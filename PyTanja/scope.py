import configuration
import pygame
import os

class Sprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file, transparent_color=None) -> None:
        pygame.sprite.Sprite.__init__(self)

        if file in Sprite.images:
            self.image = Sprite.images[file]
        else:
            self.image = pygame.image.load(os.path.join(configuration.IMAGES_FOLDER, file))
            self.image = pygame.transform.scale(self.image, (configuration.TILE_SIZE, configuration.TILE_SIZE))
            Sprite.images[file] = self.image
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * configuration.TILE_SIZE, row * configuration.TILE_SIZE)
        self.row = row
        self.col = col

class Tile(Sprite):
    def __init__(self, row, col, file):
        super(Tile, self).__init__(row, col, file)
    
    def position(self):
        return self.row, self.col
    
    def cost(self):
        pass
    
    def mark(self):
        pass

class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')
    
    def cost(self):
        return 7
    
    def mark(self):
        return 'd'

class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def mark(self):
        return 'g'

class Mud(Tile):

    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5
    
    def mark(self):
        return 'm'

class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def mark(self):
        return 'r'

class Water(Tile):
    
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def mark(self):
        return 'w'

class Trail(Sprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png')
        self.num = num

    def draw(self, screen):
        text = configuration.FONT.render(f'{self.num}', True, configuration.WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect) 

class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def mark(self):
        return 's'

class Goal(Sprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', configuration.GREEN)
