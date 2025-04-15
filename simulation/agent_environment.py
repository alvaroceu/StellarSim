import pygame
import sys
import random
import math
from simulation.body import Body
from simulation.config import *
from simulation.physics import *
from agents.rl_agent import RLAgent


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

        self.agent = RLAgent() # Simultion agent

        self.update_episode_max_duration()
        self.reset_episode()

    def reset_episode(self):
        """
        Resets the simulation environment: places a sun in the center,
        and allows the agent to launch a new planet (with random parameters)
        """
        self.sun = Body(WIDTH / 2, HEIGHT / 2, 20, YELLOW, 2000, 0, 0)
        self.bodies = [self.sun]

        # Agent decision based on his knowledge
        start_x, start_y = random_position_around(self.sun, 300)
        dx = start_x - self.sun.x
        dy = start_y - self.sun.y
        planet = Body(start_x, start_y, 5, BLUE, 1, 0, 0)

        velocity, angle = self.agent.select_action(dx, dy)
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
            
            # Key events
            elif event.type == pygame.KEYDOWN:

                # Simulation control keys
                if event.key == pygame.K_PLUS:
                    self.timestep = round(self.timestep + 0.2,2)
                    self.update_episode_max_duration()
                    print(f"Simulation speed: {self.timestep}")
                elif event.key == pygame.K_MINUS and self.timestep > 0.2:
                    self.timestep = round(self.timestep - 0.2,2)
                    self.update_episode_max_duration()
                    print(f"Simulation speed: {self.timestep}")

    def update(self):
        if not self.bodies:
            return

        for body in self.bodies:
            body.apply_gravity(self.bodies)
            body.movement(self.timestep)

        self.episode_duration += 1

        if self.episode_over():
            print(f"Episode {self.episode} ended")
            self.evaluate_episode()
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

        # Controls panel
        controls_y = 10
        controls_text = [
            "Controls:",
            "",
            "+/- = Change speed",
        ]

        for line in controls_text:
            control_label = font.render(line, True, WHITE)
            self.window.blit(control_label, (780, controls_y))
            controls_y += 25

    def evaluate_episode(self):
        """
        Calculates the reward for the last episode and updates the agent.
        """
        if len(self.bodies) < 2:
            reward = -1  # Planet destroyed or not created
        else:
            planet = self.bodies[1]
            if planet.is_colliding(self.sun):
                reward = -1
            elif planet.x < 0 or planet.x > WIDTH or planet.y < 0 or planet.y > HEIGHT:
                reward = -1
            elif self.episode_duration >= self.episode_max_time:
                reward = 1  # Successful orbit
            else:
                reward = 0

        self.agent.give_feedback(reward)
    
    def update_episode_max_duration(self):
        """
        Updates the max duration of an episode (in frames) based on timestep speed.
        Ensures the simulation always runs for 20 seconds of simulated time.
        """
        fps = 60
        sim_seconds = 20

        # Total frames needed = total simulated seconds / timestep * fps
        self.episode_max_time = int((sim_seconds / self.timestep) * fps)


def random_position_around(center, radius):
    """
    Generates a random position around a center point at a given radius.
    """
    angle = random.uniform(0, 2 * math.pi)
    x = center.x + radius * math.cos(angle)
    y = center.y + radius * math.sin(angle)
    return x, y
