import pygame
import sys
from simulation.body import *
from simulation.physics import *

# Initialize pygame
pygame.init()

# Display config
WIDTH, HEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("StellarSim")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237) 

# Create bodies
sun = Body(WIDTH/2, HEIGHT/2, 30, YELLOW, 2000, 0, 0)
planetA = Body(WIDTH/2 + 150, HEIGHT/2, 25, BLUE, 2000, 0, 0)
planetA.set_circular_orbit(sun)

bodies = [sun, planetA]


# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill background
    WINDOW.fill(BLACK)

    # Update and draw bodies
    for body in bodies:

        body.apply_gravity(bodies)
        body.movement()
        body.draw(WINDOW)
    
    # Detect and handle collisions
    to_remove = set()

    for i, body_a in enumerate(bodies):
        for j, body_b in enumerate(bodies):
            if i >= j:  # Avoid duplicate pairs and self-check
                continue
            if body_a.is_colliding(body_b):
                print(f"Collision: {body_a} vs {body_b}")
                to_remove.add(body_b)

    # Remove one collided body from bodies
    bodies = [body for body in bodies if body not in to_remove]

    # Update display
    pygame.display.flip()

# Exit
pygame.quit()
sys.exit()