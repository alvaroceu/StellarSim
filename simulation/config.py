"""
Global configuration values for the simulation (window size, colors, constants).
"""

WIDTH = 1000
HEIGHT = 700

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237) 
RED = (200, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

DEFAULT_PARAMS = {
    "mass": 1,
    "radius": 5,
    "color": BLUE,
}

# Gravitational constant and simulation time step
G = 1
TIMESTEP = 1