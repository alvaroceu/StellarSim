import pygame
import math
from config import *

class Body:

    def __init__(self, x, y, radius, color, mass, vx, vy):
        self.x = x # Position (in pixels)
        self.y = y
        self.radius = radius # Radius (in pixels)
        self.color = color
        self.mass = mass
        self.vx = vx # Velocity (pixels/frame)
        self.vy = vy
        self.ax = 0 # Acceleration
        self.ay = 0

    def apply_gravity(self, others):
        total_ax = 0
        total_ay = 0

        for other in others:
            if other is self:
                continue
            
            # Distance calculation
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.hypot(dx, dy)

            if distance == 0:
                continue # Avoid /0
            
            # Gravitational force: F = G * (m1 * m2) / r^2
            force = G * self.mass * other.mass / distance**2
            # Acceleration in each axis
            ax = force * (dx/distance) / self.mass
            ay = force * (dy/distance) / self.mass

            total_ax += ax
            total_ay += ay
        
        self.ax = total_ax
        self.ay = total_ay

    def movement(self):
        self.vx += self.ax * TIMESTEP
        self.vy += self.ay * TIMESTEP
        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
