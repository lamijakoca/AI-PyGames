import Tile

class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')
    
    def cost(self):
        return 7
    
    def mark(self):
        return 'd'