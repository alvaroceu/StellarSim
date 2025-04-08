import pygame
from simulation.config import WHITE

# Basic UI
def draw_interface(surface, selected_body_type, current_params):
    """
    Renders the user interface on the given surface, showing current settings and controls.
    """
    
    font = pygame.font.SysFont("consolas", 18)

    # Display selected type
    text = font.render(f"Selected type: {selected_body_type}", True, WHITE)
    surface.blit(text, (10, 10))

    # Display params: mass, radius, color
    y_offset = 40
    for key, value in current_params.items():
        if key != "color":
            label = font.render(f"{key.capitalize()}: {value}", True, WHITE)
        else:
            label = font.render(f"{key.capitalize()}:", True, WHITE)
        surface.blit(label, (10, y_offset))
        y_offset += 25

    # Color preview rectangle next to "Color:" label
    pygame.draw.rect(surface, current_params["color"], pygame.Rect(75, 90, 40, 20))

    # Controls panel
    controls_y = 10
    controls_text = [
        "Controls:",
        "",
        "1 = Star, 2 = Planet",
        "Q/E = Select color",
        "W/S = Select mass",
        "A/D = Select radius",
        "Click = Add body",
        "",
        "Space = Pause/Resume",
        "+/- = Change speed",
        "R = Reset simulation"
    ]

    for line in controls_text:
        control_label = font.render(line, True, WHITE)
        surface.blit(control_label, (780, controls_y))
        controls_y += 25