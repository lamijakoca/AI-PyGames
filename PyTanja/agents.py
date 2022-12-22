import configuration
from scope import Sprite

class Agent(Sprite):
    def __init__(self, row, col, file):
        super(Agent, self).__init__(row, col, file)

    def move(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x = self.rect.x + col
        self.rect.y = self.rect.y + row
    
    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * configuration.TILE_SIZE
        self.rect.y = row * configuration.TILE_SIZE
    
    def get_agent_path(self, map, goal): 
        pass
    
class ExampleAgent(Agent):
    def __init__(self, row, col, file):
        super().__init__(row, col, file)
        
    def get_agent_path(self, map, goal):
        path = [map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col <goal[1] else col - 1
            else: break
            path.append(map[row][col])
        return path
        
# depth first search
class Aki:
    pass

# A*
class Bole:
    pass

# branch and bound
class Draza:
    pass

# breadth first search
class Jocke:
    pass
    