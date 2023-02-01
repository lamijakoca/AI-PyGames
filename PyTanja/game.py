import os
import sys
import pygame
import configuration
from scope import Dune, Goal, Grass, Mud, Road, Stone, Water, Trail 

class Game:
    def __init__(self):
        self.path_cost = 0
        pygame.display.set_caption("PyTanja")
        # load/run maps
        values = Game.load_map(sys.argv[1] if len(sys.argv) > 1 else os.path.join(configuration.MAPS_FOLDER, 'map0.txt'))
        self.char_map = values[0]
        self.start = values[1:3]
        self.goal = values[3:]
        #window formatting
        configuration.TILE_SIZE = min(configuration.MAX_HEIGHT // len(self.char_map), configuration.MAX_WIDTH // len(self.char_map))
        configuration.HEIGHT = configuration.TILE_SIZE * len(self.char_map)
        configuration.WIDTH =  configuration.TILE_SIZE * len(self.char_map[0])
        configuration.SPEED = int(configuration.TILE_SIZE * 2)

        pygame.font.init()
        configuration.FONT = pygame.font.Font(None, configuration.TILE_SIZE // 3)
        configuration.RIBBON_HEIGHT = int(configuration.FONT.size('')[1] * 1.5)

        self.screen = pygame.display.set_mode((configuration.WIDTH, configuration.HEIGHT))
        self.tilesSprites = pygame.sprite.Group()
        self.trailsSprites = pygame.sprite.Group()
        self.agentsSprites = pygame.sprite.Group()

        tile_map = []
        for i, row in enumerate(self.char_map):
            map_row = []
            for j, elem in enumerate(row):
                if elem == 'r':
                    t = Road(i, j)
                elif elem == 's':
                    t = Stone(i,j)
                elif elem == 'm':
                    t = Mud(i, j)
                elif elem == 'd':
                    t = Dune(i, j)
                elif elem == 'w':
                    t = Water(i, j)
                else: 
                    t = Grass(i, j)
                self.tilesSprites.add(t)
                map_row.append(t)
            tile_map.append(map_row)
        self.tile_map = tile_map
        self.tilesSprites.add(Goal(self.goal[0], self.goal[1]))
        # run agents
        module2 = __import__('agents')
        class_ = getattr(module2, sys.argv[2] if len(sys.argv) > 2 else 'ExampleAgent')
        self.agent = class_(self.start[0], self.start[1], f'{sys.argv[2]}.png' if len(sys.argv) > 2 else 'ExampleAgent.png')
        self.agentsSprites.add(self.agent)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.game_over = False

    def run(self):
        path = self.agent.get_agent_path(self.tile_map, self.goal)
        original_path = [p for p in path]
        print(f"Path: {', '.join([str(p.position()) for p in path])}")
        print(f"Path cost: {sum([trace.cost() for trace in path])}")
        tile = path.pop(0)
        x, y = tile.position()
        self.path_cost = tile.cost()
        counter = 1
        time = 0
        while self.running:
            try:
                if self.playing:
                    if not time:
                        self.agent.place_to(x, y)
                        self.trailsSprites.add(Trail(x, y, counter))
                        counter += 1
                        try:
                            tile = path.pop(0)
                        except IndexError:
                            raise EndGame()
                        old_x, old_y = x, y
                        x,y = tile.position()
                        self.check_move(old_x, old_y, x, y)
                        self.path_cost += tile.cost()
                    time += 1
                    if time == configuration.TILE_SIZE:
                        time = 0
                    self.agent.move(x, y)
                    self.clock.tick(configuration.SPEED)
                self.events()
                self.draw()
            except EndGame:
                self.game_over = True
                self.playing = False
                if len(original_path):
                    self.path_cost = sum([t.cost() for t in original_path])
                    goal_x, goal_y = original_path[-1].position()
                    self.trailsSprites = pygame.sprite.Group()
                    for num, tile in enumerate(original_path):
                        old_x, old_y = x, y
                        x, y = tile.position()
                        if num:
                            self.check_move(old_x, old_y, x, y)
                        self.trailsSprites.add(Trail(x, y, num + 1))
                    self.agent.place_to(goal_x, goal_y)
            except Exception as e:
                self.game_over = True
                raise e
    
    def check_move(self, old_x, old_y, x, y):
        if abs(old_x - x) + abs(old_y - y) != 1:
            raise Exception(f'ERROR: Path nodes {old_x, old_y} and {x, y} are not adjacent')
        if not(x in range(len(self.tile_map)) and y in range (len(self.tile_map[0]))):
            raise Exception(f'ERROR: Agent {x, y} is out of bounds')

    def draw(self):
        self.screen.fill(configuration.BLACK, rect=(0, configuration.HEIGHT, configuration.WIDTH, configuration.RIBBON_HEIGHT))
        self.tilesSprites.draw(self.screen)
        # draw background around numbers (steps)
        self.trailsSprites.draw(self.screen)
        # draw steps
        for t in self.trailsSprites:
            t.draw(self.screen)
        self.agentsSprites.draw(self.screen)
        cost = configuration.FONT.render(f'Score: {str(self.path_cost)}', True, configuration.GREEN)
        self.screen.blit(cost, (10, configuration.HEIGHT + configuration.RIBBON_HEIGHT // 5))
        if self.game_over:
            game_over = configuration.FONT.render('GAME OVER', True, configuration.RED)
            text_rect = game_over.get_rect(center = (configuration.WIDTH // 2, configuration.HEIGHT // 2))
            self.screen.blit(game_over, text_rect)
        pygame.display.flip()

    @staticmethod
    def load_map(map):
        try:
            with open(map, 'r') as file:
                ar, ac = [int(val) for val in file.readline().strip().split(',')]
                gr, gc = [int(val) for val in file.readline().strip().split(',')]
                matrix = []
                while True:
                    line = file.readline().strip()
                    if not len(line):
                        break
                    matrix.append([c for c in line])
            return matrix, ar, ac, gr, gc
        except Exception as ex:
            raise ex

    def quit(self):
        self.game_over = True
        self.running = False

    def events(self):
        # space - pokrenuti i zaustaviti
        # enter = prikazati konacnu putanju do cilja
        # esc - prekinuti i zatvoriti prozor
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            if self.game_over:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.playing = not self.playing
            elif event.type == pygame.KEYDOWN and event.key in(pygame.K_RETURN, pygame.K_KP_ENTER):
                raise EndGame()
            
class EndGame(Exception):
    pass