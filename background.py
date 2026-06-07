class ScrollingBackground:
    def __init__(self, surface, speed=1):
        self.surface = surface
        self.speed = speed
        self.offset = 0

    def set_surface(self, surface):
        self.surface = surface
        self.offset %= self.surface.get_height()

    def advance(self):
        self.offset = (self.offset + self.speed) % self.surface.get_height()

    def draw(self, screen):
        height = self.surface.get_height()
        screen.blit(self.surface, (0, self.offset - height))
        screen.blit(self.surface, (0, self.offset))
