import math

def calculate_circular_orbit_velocity(G, main_mass, dx, dy):

    radius = math.hypot(dx,dy)
    velocity = math.sqrt((G*main_mass)/radius)

    norm = math.hypot(dy, -dx)
    vx = velocity * dy / norm
    vy = -velocity * dx / norm

    return vx, vy