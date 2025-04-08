import pygame
import math
from simulation.config import *
from simulation.physics import *


class Body:
    """
    Represents a celestial body in the simulation with basic physics properties:
    position, velocity, acceleration, mass, radius, and color.
    """

    def __init__(self, x, y, radius, color, mass, vx, vy):
        self.x = x # Position (in pixels)
        self.y = y
        self.radius = radius # Radius (in pixels)
        self.color = color
        self.mass = mass
        self.vx = vx # Velocity (pixels/frame)
        self.vy = vy
        self.ax = 0 # Acceleration (pixels/frame^2)
        self.ay = 0

    def apply_gravity(self, others):
        """
        Updates this body's acceleration based on gravitational attraction 
        from all other bodies in the simulation.
        """

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
                continue # Avoid division by 0
            
            # Gravitational force: F = G * (m1 * m2) / r^2
            force = G * self.mass * other.mass / distance**2
            
            # Acceleration in each axis
            ax = force * (dx/distance) / self.mass
            ay = force * (dy/distance) / self.mass

            total_ax += ax
            total_ay += ay
        
        self.ax = total_ax
        self.ay = total_ay

    def set_circular_orbit(self, main_mass):
        """
        Sets this body's velocity for a stable circular orbit around another body.
        Assumes 'main_mass' is another Body object.
        """

        dx = self.x - main_mass.x
        dy = self.y - main_mass.y
        vx, vy = calculate_circular_orbit_velocity(G, main_mass.mass, dx, dy)
        self.vx = vx
        self.vy = vy
    
    def is_colliding(self, other):
        """
        Returns True if this body is colliding with another body (based on radius overlap).
        """

        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx,dy)
        return distance <= (self.radius + other.radius)

    def movement(self):
        """
        Updates this body's position and velocity based on acceleration.
        """

        self.vx += self.ax * TIMESTEP
        self.vy += self.ay * TIMESTEP
        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP

    def draw(self, surface):
        """
        Renders the body as a filled circle on the given Pygame surface.
        """
        
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
