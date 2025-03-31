import pygame

class Body:

    def __init__(self, x, y, radius, color, mass):
        self.x = x # Position (in pixels)
        self.y = y
        self.radius = radius # Radius (in pixels)
        self.color = color
        self.mass = mass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
