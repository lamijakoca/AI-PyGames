import random
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
            else: 
                break
            path.append(map[row][col])
        return path
        
# depth first search
# stack
class Aki(Agent):
    def __init__(self, row, col, file):
        super().__init__(row, col, file)

    def get_agent_path(self, map, goal):
        
        stack = []
        possible = []
        path= [map[self.row][self.col]]

        row = self.row
        col = self.col
        visited = [(row, col)]
        run = True

        while run:
            if row == goal[0] and col == goal[1]:
                break
            
            if row > 0:
                temp = (row - 1, col)
                if temp not in visited:
                    possible.append(map[row-1][col])
            if col > 0:
                temp = (row, col - 1)
                if temp not in visited:
                    possible.append(map[row][col-1])
            if row < (len(map) - 1):
                temp = (row + 1, col)
                if temp not in visited:
                    possible.append(map[row + 1][col])
            if col < (len(map[0]) - 1):
                temp = (row, col + 1)
                if temp not in visited:
                    possible.append(map[row][col + 1])
            
            if not possible:
                path.pop()
                elem = stack.pop()

                while elem in visited:
                    if not stack:
                        return
                    elem = stack.pop()
                    path.pop()
                row = elem.row
                col = elem.col
                visited.append((elem.row, elem.col))
                print(visited)
                
            else:
                #need to sort (tile costs) in reverse order
                possible.sort(key=lambda tile: (tile.cost(), -4 if tile.row < row else -3 if tile.col > col else -2 if tile.row > row else -1), reverse=True)
                elem = possible.pop()
                row = elem.row
                col = elem.col
                path.append(map[elem.row][elem.col])
                visited.append((elem.row, elem.col))
                stack.extend(possible)
                possible = []
            
            if not stack:
                run = False
        return path

# A*
# f = h + c
class Bole(Agent):
    def __init__(self, row, col, file):
        super().__init__(row, col, file)
    
    def get_agent_path(self, mapa, goal):
        path = []
        queue = []
        possible = []
        current_list = [mapa[self.row][self.col]]

        row = self.row
        col = self.col
        visited = [(row, col)]
        run = True

        while run:
            if row == goal[0] and col == goal[1]:
                break
            
            if row > 0:
                temp = (row - 1, col)
                if temp not in visited:
                    possible.append(mapa[row-1][col])
            if col > 0:
                temp = (row, col - 1)
                if temp not in visited:
                    possible.append(mapa[row][col-1])
            if row < (len(mapa) - 1):
                temp = (row + 1, col)
                if temp not in visited:
                    possible.append(mapa[row + 1][col])
            if col < (len(mapa[0]) - 1):
                temp = (row, col + 1)
                if temp not in visited:
                    possible.append(mapa[row][col + 1])

            if not possible:
                current_list = queue.pop(0)
                elem = current_list[-1]
                row = elem.row
                col = elem.col
                visited.append((row,col))
            
            else:
                current_copy_list = current_list.copy()
                for i in possible:
                    current_copy_list.append(i)
                    queue.append(current_copy_list)
                    current_copy_list = current_list.copy()

                queue.sort(key=lambda md: (sum(map(lambda tile: tile.cost(), md)) 
                + sum(map(lambda tile: tile.cost(), md))
                * (abs(md[-1].row - goal[0]) + abs(md[-1].col - goal[1]))
                ))

                current_list = queue.pop(0)
                elem = current_list[-1]
                row = elem.row
                col = elem.col
                visited.append((row, col))

            if not queue:
                run = False
        
        path = current_list
        return path
        
# branch and bound
# reverse cost and pick best path
class Draza(Agent):
    def __init__(self, row, col, file):
        super().__init__(row, col, file)

    def get_agent_path(self, mapa, goal):
        queue = []
        possible = []
        path = []
        current_list = [mapa[self.row][self.col]]

        row = self.row
        col = self.col
        visited = [(row, col)]
        run = True

        while run:
            if row == goal[0] and col == goal[1]:
                break
            
            if row > 0:
                temp = (row - 1, col)
                if temp not in visited:
                    possible.append(mapa[row-1][col])
            if col > 0:
                temp = (row, col - 1)
                if temp not in visited:
                    possible.append(mapa[row][col-1])
            if row < (len(mapa) - 1):
                temp = (row + 1, col)
                if temp not in visited:
                    possible.append(mapa[row + 1][col])
            if col < (len(mapa[0]) - 1):
                temp = (row, col + 1)
                if temp not in visited:
                    possible.append(mapa[row][col + 1])

            if not possible:
                current_list = queue.pop(0)
                elem = current_list[-1]
                row = elem.row
                col = elem.col
                visited.append((row, col))

            else:
                current_copy_list = current_list.copy()
                for i in possible:
                    current_copy_list.append(i)
                    queue.append(current_copy_list)
                    current_copy_list = current_list.copy()
                
                #sum - need to calculate number of non-blank tiles not in their goal position
                queue.sort(key = lambda l: (sum(map(lambda tile: tile.cost(), l)), len(l), random.random()))
                possible = []
                current_list = queue.pop(0)
                elem = current_list[-1]
                row = elem.row
                col = elem.col
                visited.append((row, col))

            if not queue:
                run = False
                
        path = current_list
        return path

# breadth first search
# queue
class Jocke(Agent):
    pass
    # def __init__(self, row, col, file):
    #     super().__init__(row, col, file)

    # def get_agent_path(self, mapa, goal):
    #     pass
        # possible = []
        # queue = [] # treba da cuva komsije
        # path = [mapa[self.row][self.col]]
        
        # row = self.row
        # col = self.col
        # visited = [(row, col)]
        # run = True    

        # while run:
        #     if row == goal[0] and col == goal[1]:
        #         break
            
        #     if row > 0:
        #         temp = (row - 1, col)
        #         if temp not in visited:
        #             possible.append(mapa[row-1][col])
        #     if col > 0:
        #         temp = (row, col - 1)
        #         if temp not in visited:
        #             possible.append(mapa[row][col-1])
        #     if row < (len(mapa) - 1):
        #         temp = (row + 1, col)
        #         if temp not in possible:
        #             possible.append(mapa[row + 1][col])
        #     if col < (len(mapa[0]) - 1):
        #         temp = (row, col + 1)
        #         if temp not in possible:
        #             possible.append(mapa[row][col + 1])