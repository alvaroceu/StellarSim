import pygame
import sys
import random
import math

from body import Body
from simulation.config import *
from simulation.physics import *

class AgentSimulation:
    """
    Experimental mode driven by an AI agent. The agent attempts to place a planet
    in a stable orbit around a central sun. Failed attempts reset automatically.
    """

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("StellarSim - Experimental Mode")

        self.clock = pygame.time.Clock()
        self.running = True
        self.timestep = TIMESTEP

        self.episode = 0
        self.episode_duration = 0
        self.episode_max_time = 20 * 60  # 20 seconds at 60 FPS

        self.reset_episode()

    def reset_episode(self):
        """
        Resets the simulation environment: places a sun in the center,
        and allows the agent to launch a new planet (with random parameters)
        """
        self.sun = Body(WIDTH / 2, HEIGHT / 2, 20, YELLOW, 2000, 0, 0)
        self.bodies = [self.sun]

        # Agent decision (for now: random velocity and angle)
        start_x, start_y = random_position_around(self.sun, 300)
        planet = Body(start_x, start_y, 5, BLUE, 1, 0, 0)

        velocity = random.uniform(0, 5)
        angle = random.uniform(0, 2 * math.pi)
        planet.vx = velocity * math.cos(angle)
        planet.vy = velocity * math.sin(angle)

        self.bodies.append(planet)
        self.episode_duration = 0
        self.episode += 1

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if not self.bodies:
            return

        for body in self.bodies:
            body.apply_gravity(self.bodies)
            body.movement(self.timestep)

        self.episode_duration += 1

        if self.episode_over():
            print(f"Episode {self.episode} ended")
            self.reset_episode()

    def episode_over(self):
        """
        Returns True if the planet has failed (collision or out of bounds)
        or False if the planet has survived the full episode (success).
        """
        if len(self.bodies) < 2:
            return True  # Planet destroyed or not present

        planet = self.bodies[1]
        if planet.is_colliding(self.sun):
            return True
        if planet.x < 0 or planet.x > WIDTH or planet.y < 0 or planet.y > HEIGHT:
            return True
        if self.episode_duration >= self.episode_max_time:
            return True
        return False

    def render(self):
        self.window.fill(BLACK)
        for body in self.bodies:
            body.draw(self.window)

        self.draw_episode_info()
        pygame.display.flip()

    def draw_episode_info(self):
        font = pygame.font.SysFont("consolas", 18)
        label = font.render(f"Episode: {self.episode}", True, WHITE)
        self.window.blit(label, (10, 10))

def random_position_around(center, radius):
    """
    Generates a random position around a center point at a given radius.
    """
    angle = random.uniform(0, 2 * math.pi)
    x = center.x + radius * math.cos(angle)
    y = center.y + radius * math.sin(angle)
    return x, y
