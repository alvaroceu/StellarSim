import math

def calculate_circular_orbit_velocity(G, main_mass, dx, dy):
    """
    Given a gravitational constant G, a central mass (main_mass),
    and the position vector (dx, dy) relative to the central body,
    returns the tangential velocity vector (vx, vy) required for a stable circular orbit.
    """

    radius = math.hypot(dx,dy)
    velocity = math.sqrt((G*main_mass)/radius)

    # Normalize direction vector perpendicular to radius for tangential velocity
    norm = math.hypot(dy, -dx)
    vx = velocity * dy / norm
    vy = -velocity * dx / norm

    return vx, vy