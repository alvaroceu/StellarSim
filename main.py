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
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

color_palette = [
    BLUE, 
    RED,   
    GREEN,  
    WHITE, 
]
color_index = 0


# Currently Selected Body Params
current_params = {
    "mass": 1,
    "radius": 5,
    "color": BLUE,
}

# Create bodies
sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 2000, 0, 0)
bodies = [sun]

# Basic UI
font = pygame.font.SysFont("consolas", 18)

def draw_interface(surface):
    # Selected type
    text = font.render(f"Selected type: {selected_body_type}", True, WHITE)
    surface.blit(text, (10, 10))

    # Params
    y_offset = 40
    for key, value in current_params.items():
        if key != "color":
            label = font.render(f"{key.capitalize()}: {value}", True, WHITE)
        else:
            label = font.render(f"{key.capitalize()}:", True, WHITE)
        surface.blit(label, (10, y_offset))
        y_offset += 25

    # Color preview
    pygame.draw.rect(surface, current_params["color"], pygame.Rect(75, 90, 40, 20))

    # Controls
    controls_y = 10
    controls_text = [
        "Controls:",
        "1 = Star, 2 = Planet",
        "Q/E = Select color",
        "W/S = Select mass",
        "A/D = Select radius",
        "Click = Add body"
    ]

    for line in controls_text:
        control_label = font.render(line, True, WHITE)
        surface.blit(control_label, (780, controls_y))
        controls_y += 25

# Main loop
running = True
paused = False
selected_body_type = "planet" # Default selected body

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key events
        elif event.type == pygame.KEYDOWN:

            # Select new bodies to create
            if event.key == pygame.K_1:
                selected_body_type = "star"
                print("Selected type: star")
            elif event.key == pygame.K_2:
                selected_body_type = "planet"
                print("Selected type: planet")

            # Simulation control keys
            elif event.key == pygame.K_SPACE:
                paused = not paused
                print("Paused" if paused else "Resumed")
            elif event.key == pygame.K_r:
                sun = Body(WIDTH/2, HEIGHT/2, 20, YELLOW, 2000, 0, 0)
                bodies = [sun]
                print("Simulation reset")

            # Change mass
            elif event.key == pygame.K_w:
                current_params["mass"] += 1
            elif event.key == pygame.K_s and current_params["mass"] > 1:
                current_params["mass"] -= 1

            # Change radius
            elif event.key == pygame.K_d:
                current_params["radius"] += 1
            elif event.key == pygame.K_a and current_params["radius"] > 1:
                current_params["radius"] -= 1

            # Change color
            elif event.key == pygame.K_q:
                color_index = (color_index - 1) % len(color_palette)
                current_params["color"] = color_palette[color_index]
            elif event.key == pygame.K_e:
                color_index = (color_index + 1) % len(color_palette)
                current_params["color"] = color_palette[color_index]

        # Create selected body
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            if selected_body_type == "star":
                new_body = Body(mx, my, 20, YELLOW, 2000, 0, 0)
                bodies.append(new_body)
            elif selected_body_type == "planet":
                new_body = Body(mx, my, current_params["radius"], current_params["color"], current_params["mass"], 0, 0)
                bodies.append(new_body)
                new_body.set_circular_orbit(sun)

    # Fill background
    WINDOW.fill(BLACK)

    # Update and draw bodies
    if not paused:
        for body in bodies:

            body.apply_gravity(bodies)
            body.movement()
    for body in bodies:
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
    
    # Draw UI
    draw_interface(WINDOW)

    # Update display
    pygame.display.flip()

# Exit
pygame.quit()
sys.exit()