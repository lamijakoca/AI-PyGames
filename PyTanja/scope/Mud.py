import Tile

class Mud(Tile):

    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5
    
    def mark(self):
        return 'm'