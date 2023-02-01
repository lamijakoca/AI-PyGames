import os
import sys
import pygame
import configuration

class Game:
    def __init__(self):
        self.running = True
        self.playing = False
        self.game_over = False
        self.time_to_think = 0
        self.max_levels = 0
        pygame.display.set_caption('PyStolovina')
        
        # load chosen map
        chars = Game.load_map(sys.argv[1] if len(sys.argv) > 1 else os.path.join(configuration.MAPS_FOLDER, 'map0.txt'))
    
        # window formatting 
        configuration.TILE_SIZE = min(configuration.MAX_HEIGHT // len(self.chars), configuration.MAX_WIDTH // len(self.chars))
        configuration.HEIGHT = configuration.TILE_SIZE * len(self.chars)
        configuration.WIDTH = configuration.TILE_SIZE * len(self.chars[0])
        configuration.SPEED = int(configuration.TILE_SIZE * 2)

        # define font - just size
        pygame.font.init()
        configuration.FONT = pygame.font.Font(None, configuration.TILE_SIZE // 3)
        configuration.RIBBON_HEIGHT = int(configuration.FONT.size('')[1] * 1.5)

        self.screen = pygame.display.set_mode(configuration.WIDTH, configuration.HEIGHT)
        pass

    def run(self):
        pass

    def check_is_active():
        pass

    def draw(self):
        pass

    @staticmethod
    def load_map(map):
        try:
            with open(map, 'r') as file:
                matrix = []
                while True:
                    line = file.readline().strip()
                    if not len(line):
                        break
                    matrix.append([c for c in line])
                return matrix
        except Exception as ex:
            raise ex
    
    def quit(self):
        self.game_over = True
        self.running = False

    def events(self):
        # space - pokrenuti i zaustaviti agenta
        # esc - prekinuti i zatvoriti prozor
        for event in pygame.event.get():
            if event.type == pygame.QUIT and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            if self.game_over:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.playing = not self.playing

class EndGame(Exception):
    pass