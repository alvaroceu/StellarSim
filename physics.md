# Physics Behind StellarSim
This document provides a detailed explanation of the physics calculations used in StellarSim, focusing on the simulation of gravitational interactions between celestial bodies

## Gravitational Force and Acceleration
To simulate realistic planetary motion, StellarSims uses Newton´s Law of Universal Gravitation

### Newton's Law of Gravitation
The gravitational force F between two bodies is calculated as: 

###### F = G * (m1 * m2) / r^2

### Vector Descomposition of Force
The gravitational force is a vector pointing from one object to another. To simulate motion in 2D space, we need to decompose this force into its x and y components:

###### dx = x2 - x1
###### dy = y2 - y1

The unit vector from body 1 to body 2 is:

###### u = (dx/d, dy/d)

So the force vector components are:

###### Fx = F * dx/d
###### Fy = F * dy/d

### Acceleration
According to Newton's second law: a = F/m

We apply this to each axis separately:

###### ax = Fx/m = F * dx/d /m

###### ay = Fy/m = F * dy/d /m

This acceleration is used to update the velocity and position of the body over time

