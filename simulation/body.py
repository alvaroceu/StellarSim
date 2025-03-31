import pygame

class Body:

    def __init__(self, x, y, radius, color, mass, vx, vy):
        self.x = x # Position (in pixels)
        self.y = y
        self.radius = radius # Radius (in pixels)
        self.color = color
        self.mass = mass
        self.vx = vx # Velocity (pixels/frame)
        self.vy = vy

    def movement(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
