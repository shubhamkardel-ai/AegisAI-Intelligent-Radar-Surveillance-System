class Radar:

    def __init__(self):
        self.angle = 0

    def update(self):
        self.angle = (self.angle + 1) % 360

    def draw(self, screen):
        pass