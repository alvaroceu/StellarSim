import pygame
import sys
from simulation.body import *

# Initialize pygame
pygame.init()

# Display config
WIDTH, HEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("StellarSim")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Create bodies
sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 1.989e30)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill background
    WINDOW.fill(BLACK)

    # Draw bodies
    sun.draw(WINDOW)

    # Update display
    pygame.display.flip()

# Exit
pygame.quit()
sys.exit()