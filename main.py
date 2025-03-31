import pygame
import sys

# Initialize pygame
pygame.init()

# Display config
WIDTH, HEIGHT = 1000, 700
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("StellarSim")

# Colors
BLACK = (0, 0, 0)

# Main loop
running = True
x = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill background
    WINDOW.fill(BLACK)

    # Update display
    pygame.display.flip()

# Exit
pygame.quit()
sys.exit()