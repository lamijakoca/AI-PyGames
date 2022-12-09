import Tile

class Water(Tile):
    
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def mark(self):
        return 'w'