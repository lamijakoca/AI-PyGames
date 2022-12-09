import Sprite

class Goal(Sprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png')