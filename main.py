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
sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 2000, 0, 0)
bodies = [sun]


# Main loop
running = True
selected_body_type = "planet" # Default selected body

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Select new bodies to create
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_body_type = "star"
                print("Selected type: star")
            elif event.key == pygame.K_2:
                selected_body_type = "planet"
                print("Selected type: planet")
        # Create selected body
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if selected_body_type == "star":
                new_body = Body(mx, my, 20, YELLOW, 2000, 0, 0)
                bodies.append(new_body)
            elif selected_body_type == "planet":
                new_body = Body(mx, my, 5, BLUE, 1, 0, 0)
                bodies.append(new_body)
                new_body.set_circular_orbit(sun)

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