import pygame
import sys
from simulation.body import Body
from simulation.physics import *
from ui.interface import draw_interface
from simulation.config import *

class Simulation:
    """
    Main simulation class that handles initialization, event proceessing,
    physics updates, and rendering for StellarSIm
    """

    def __init__(self):
        """
        Pygame and simulation state initialization
        """

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("StellarSim")

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        self.selected_body_type = "planet"
        self.current_params = DEFAULT_PARAMS.copy()

        self.sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 2000, 0, 0)
        self.bodies = [self.sun]

        self.color_palette = [
            BLUE, 
            RED,   
            GREEN,  
            WHITE, 
        ]
        self.color_index = 0

        self.timestep = TIMESTEP
    
    def run(self):
        """
        Main game loop: processes events, updates simulation, renders frame.
        """

        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """
        Handles all Pygame input events including keyboard and mouse.
        Allows body creation, parameter tweaking, and simulation control.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Key events
            elif event.type == pygame.KEYDOWN:

                # Select new bodies to create
                if event.key == pygame.K_1:
                    self.selected_body_type = "star"
                    print("Selected type: star")
                elif event.key == pygame.K_2:
                    self.selected_body_type = "planet"
                    print("Selected type: planet")

                # Simulation control keys
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    print("Paused" if self.paused else "Resumed")
                elif event.key == pygame.K_r:
                    self.sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 2000, 0, 0)
                    self.bodies = [self.sun]
                    print("Simulation reset")
                elif event.key == pygame.K_PLUS:
                    self.timestep = round(self.timestep + 0.2,2)
                    print(f"Simulation speed: {self.timestep}")
                elif event.key == pygame.K_MINUS and self.timestep > 0.2:
                    self.timestep = round(self.timestep - 0.2,2)
                    print(f"Simulation speed: {self.timestep}")

                # Change mass
                elif event.key == pygame.K_w:
                    self.current_params["mass"] += 1
                elif event.key == pygame.K_s and self.current_params["mass"] > 1:
                    self.current_params["mass"] -= 1

                # Change radius
                elif event.key == pygame.K_d:
                    self.current_params["radius"] += 1
                elif event.key == pygame.K_a and self.current_params["radius"] > 1:
                    self.current_params["radius"] -= 1

                # Change color
                elif event.key == pygame.K_q:
                    self.color_index = (self.color_index - 1) % len(self.color_palette)
                    self.current_params["color"] = self.color_palette[self.color_index]
                elif event.key == pygame.K_e:
                    self.color_index = (self.color_index + 1) % len(self.color_palette)
                    self.current_params["color"] = self.color_palette[self.color_index]

            # Create selected body
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if self.selected_body_type == "star":
                    new_body = Body(mx, my, 20, YELLOW, 2000, 0, 0)
                    self.bodies.append(new_body)
                elif self.selected_body_type == "planet":
                    new_body = Body(mx, my, self.current_params["radius"], self.current_params["color"], self.current_params["mass"], 0, 0)
                    self.bodies.append(new_body)
                    new_body.set_circular_orbit(self.sun)
    
    def update(self):
        """
        Applies physics and handles collisions if simulation is running.
        """

        if not self.paused:
            for body in self.bodies:
                body.apply_gravity(self.bodies)
                body.movement(self.timestep)
            
            # Detect and handle collisions
            to_remove = set()

            for i, body_a in enumerate(self.bodies):
                for j, body_b in enumerate(self.bodies):
                    
                    # Avoid duplicate pairs and self-check
                    if i >= j:  
                        continue

                    # On collision, mark the second body for removal
                    if body_a.is_colliding(body_b):
                        print(f"Collision: {body_a} vs {body_b}")
                        to_remove.add(body_b)

            # Remove one collided body from bodies
            self.bodies = [body for body in self.bodies if body not in to_remove]

    
    def render(self):
        """
        Clears the screen, draws all bodies and the user interface.
        """
        
        self.window.fill(BLACK)
        for body in self.bodies:
            body.draw(self.window)
        draw_interface(self.window, self.selected_body_type, self.current_params)
        pygame.display.flip()