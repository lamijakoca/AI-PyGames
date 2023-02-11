from actions import Action
from students import StudentAgent
from states import GameState
from scope import Hole, Road, Goal
from bots import BotAgent, Aki
from queue import Queue
from util import TimeFunction, Timeout

import os
import sys
import time
import pygame
import threading
import configuration

class Game:
    def __init__(self):
        self.game_steps = 0
        self.think_time = 0
        # self.max_levels = 0
        pygame.display.set_caption('PyStolovina')
        
        # load chosen map
        self.char_map = Game.load_map(sys.argv[1] if len(sys.argv) > 1 else os.path.join(configuration.MAPS_FOLDER, 'map0.txt'))
        
        # window formatting 
        configuration.TILE_SIZE = min(configuration.MAX_HEIGHT // len(self.char_map), configuration.MAX_WIDTH // len(self.char_map[0]))
        configuration.HEIGHT = configuration.TILE_SIZE * len(self.char_map)
        configuration.WIDTH = configuration.TILE_SIZE * len(self.char_map[0])
        configuration.SPEED = int(configuration.TILE_SIZE * 2)
        # init font, need just font size
        pygame.font.init()
        configuration.FONT = pygame.font.Font(None, sorted([30, 50, configuration.TILE_SIZE // 3])[1])
        configuration.RIBBON_HEIGHT = int(configuration.FONT.size('')[1] * 1.5)
        
        self.screen = pygame.display.set_mode((configuration.WIDTH, configuration.HEIGHT + configuration.RIBBON_HEIGHT))
        self.agents_sprites = pygame.sprite.Group()
        self.agents = []
        self.tiles_sprites = pygame.sprite.Group()
        self.tiles = []
        self.x_sprites = pygame.sprite.Group()
        
        bots_module = __import__('bots')
        st_module = __import__('students')
        for i, row in enumerate(self.char_map):
            map_row = []
            for j, el in enumerate(row):
                if el == Hole.kind():
                    t = Hole((i, j))
                else:
                    if el == StudentAgent.kind(): 
                        if len(self.agents) and not self.agents[0].get_id():
                            raise Exception(f'StudentAgent already defined!')
                        class_ = getattr(st_module, f'{sys.argv[2]}' if len(sys.argv) > 2 else StudentAgent.__name__)
                        agent = class_((i, j), f'{StudentAgent.__name__}.png')
                        self.agents.insert(0, agent)
                        self.agents_sprites.add(agent)
                    elif el in BotAgent.agent_names.keys():
                        try:
                            class_ = getattr(bots_module, BotAgent.agent_names[el])
                        except KeyError:
                            class_ = getattr(bots_module, Aki.__name__)
                        agent = class_((i, j), f'{class_.__name__}.png')
                        self.agents.append(agent)
                        self.agents_sprites.add(agent)
                    t = Road((i, j))
                self.tiles_sprites.add(t)
                map_row.append(t)
            self.tiles.append(map_row)
        if len(self.agents) and self.agents[0].get_id():
            raise Exception(f'StudentAgent not defined!')
        self.max_think_time = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        self.max_levels = int(sys.argv[4]) if len(sys.argv) > 4 else -1
        GameState.initial_state = GameState(self.char_map, self.agents, None)
        self.state = GameState.initial_state.copy()
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.game_over = False

    def run(self):
        try:
            self.draw()
            while self.running:
                try:
                    if self.playing and not self.game_over:
                        for agent_id, agent in enumerate(self.agents):
                            self.check_game_status()
                            if not agent.is_active():
                                continue
                            legal_actions = agent.get_legal_actions(self.state)
                            try:
                                tf_queue = Queue(1)
                                tf = TimeFunction(threading.current_thread().ident,
                                                   tf_queue, self.max_think_time, agent.get_next_action, self.state,
                                                   self.max_levels)
                                tf.setDaemon(True)
                                tf.start()
                                start_time = time.time()
                                sleep_time = 0.001
                                while tf_queue.empty():
                                    time.sleep(sleep_time)
                                    self.think_time = time.time() - start_time
                                    self.draw_ribbon()
                                    self.events()
                                action, elapsed = tf_queue.get(block=False)
                                print(f'Action time elapsed: {elapsed:.2f}')
                            except Timeout:
                                print(f'Agent {agent_id} action took more than {self.max_think_time} seconds!')
                                self.deactivate_agent(agent_id)
                                continue
                            if not legal_actions or action is None or action not in legal_actions:
                                self.deactivate_agent(agent_id)
                                continue
                            print(f'On position {agent.position()} Agent {agent_id} chose action {action}')
                            self.state = self.state.apply_action(agent_id, action)
                            old_position = agent.position()
                            new_position = tuple(map(sum, zip(agent.position(), Action.actions[action])))
                            while True:
                                agent.move_towards(new_position)
                                if agent.is_in_tile():
                                    x, y = old_position
                                    self.tiles_sprites.remove(self.tiles[x][y])
                                    hole = Hole(old_position)
                                    self.tiles_sprites.add(hole)
                                    self.tiles[x][y] = hole
                                    self.draw()
                                    break
                                self.clock.tick(configuration.SPEED)
                                self.draw()
                                self.events()
                                while not self.playing:
                                    self.events()
                            agent.place_to(new_position)
                        self.game_steps += 1
                        self.draw_ribbon()
                    self.events()
                except EndGame:
                    self.game_over = True
                    self.draw()
        except Quit:
            self.quit()
        except Exception as e:
            self.quit()
            raise e

    def activate_agent(self, agent_id):
        self.agents[agent_id].set_active(True)
        self.state.agents[agent_id].set_active(True)
        for x in self.x_sprites:
            if x.rect == self.agents[agent_id].rect:
                self.x_sprites.remove(x)
                break
        self.draw()

    def deactivate_agent(self, agent_id):
        self.agents[agent_id].set_active(False)
        self.state.agents[agent_id].set_active(False)
        self.x_sprites.add(Goal(self.agents[agent_id].position()))
        self.draw()

    def check_game_status(self):
        self.state.adjust_win_loss()
        for agent_id in range(len(self.agents)):
            if self.agents[agent_id].is_active() and not self.agents[agent_id].get_legal_actions(self.state):
                self.deactivate_agent(agent_id)

        if self.state.is_win() or self.state.is_loss() or all(not agent.is_active() for agent in self.agents):
            if self.state.last_agent_played_id is not None and \
                    all([not len(self.state.get_legal_actions(agent_id)) for agent_id in range(len(self.agents))]):
                self.activate_agent(self.state.last_agent_played_id)
            raise EndGame()

    def draw(self):
        self.tiles_sprites.draw(self.screen)
        self.agents_sprites.draw(self.screen)
        self.x_sprites.draw(self.screen)

        if self.game_over:
            if self.state.is_win():
                game_over = configuration.FONT.render('WIN', True, configuration.GREEN)
            elif self.state.is_loss():
                game_over = configuration.FONT.render('LOSS', True, configuration.RED)
            else:
                game_over = configuration.FONT.render('GAME OVER', True, configuration.WHITE)
            text_rect = game_over.get_rect(center=(configuration.WIDTH // 2, configuration.HEIGHT // 2))
            self.screen.blit(game_over, text_rect)
        pygame.display.flip()

    def draw_ribbon(self):
        self.screen.fill(configuration.BLACK, rect=(0, configuration.HEIGHT, configuration.WIDTH, configuration.RIBBON_HEIGHT))
        steps_str = f'Steps: {str(self.game_steps)}'
        steps = configuration.FONT.render(steps_str, True, configuration.GREEN)
        self.screen.blit(steps, (configuration.RIBBON_HEIGHT // 5, configuration.HEIGHT + configuration.RIBBON_HEIGHT // 5))
        think_time_str = f'Time: {self.think_time:.3f}'
        tt_color = min(int(self.think_time / self.max_think_time * 100), 100)
        think_time = configuration.FONT.render(think_time_str, True, configuration.TIME[tt_color])
        self.screen.blit(think_time, (configuration.FONT.size(steps_str)[0] + 2 * configuration.RIBBON_HEIGHT // 5,
                                      configuration.HEIGHT + configuration.RIBBON_HEIGHT // 5))
        pygame.display.flip()

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
        self.running = False
        self.game_over = True

    def events(self):
        # space - pokrenuti i zaustaviti agenta
        # esc - prekinuti i zatvoriti prozor
        for event in pygame.event.get():
            if event.type == pygame.QUIT and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            if self.game_over:
                raise Quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.playing = not self.playing

class EndGame(Exception):
    pass

class Quit(Exception):
    pass