# StellarSim
**Building AI course project**

_A personal learning project combining physics, simulation and reinforcement learning._

## Summary
StellarSim is a 2D simulator of planetary systems driven by physics and reinforcement learning. It features real-time interaction and an AI agent that learns to place planets into orbit.

## Main goals

- Create celestial bodies with customizable properties
- Simulate gravity and orbital mechanics
- Real-time 2D visualization
- Interactive menu to explore and modify the stellar systems
- Add an AI agent capable of learning orbital strategies using Q-learning

## Physics behind the simulation
This project uses real-world physics formulas to simulate gravitational forces and motion between celestial bodies. For a detailed explanation of the calculations made, see [physics.md](physics.md)

## AI: Experimental mode
In the experimental mode, an RL agent attempts to learn how to launch planets into orbit. It does so by:

- Observing the planet's initial position relative to the sun
- Selecting a launch velocity and angle
- Receiving a simple reward (+1 for success, -1 for failure)

The agent improves by trial and error, forming a Q-table that guides future decisions.

## Background
**What is the problem your idea will solve?**  
It provides a visual, hands-on way to understand basic reinforcement learning in a dynamic environment.

**Why is this topic important or interesting?**  
Because it connects physics and AI in a tangible, visual experiment that is easy to explore and iterate.

## How it is used
Currently, the project runs locally and does not include a standalone installer. To use it:

#### Requirements
- Python 3.10+
- pygame (install with pip install pygame)
#### Running the simulator
0) Recomended: 
    
    Use an IDE like VSCode or PyCharm for running and modifying the code
1) Clone the repository:

    git clone https://github.com/alvaroceu/StellarSim.git
    
    cd StellarSim
2) Install dependencies:
    
    pip install pygame
3) Start de simulation
    
    python main.py


## Project Purpose
This is a personal, learning-oriented project designed to explore physics simulation, interactive graphics, system dynamics and artificial intelligence in one place. A great opportunity to improve skills in development, visualization, and computational modeling.

## Acknowledgements
- University of Helsinki – Building AI Course 
- Pygame for 2D graphics
- Inspired by space physics and classic orbital mechanics problems

## Controls Overview
| Key    | Action                         |
|--------|--------------------------------|
| 1 / 2  | Select star / planet           |
| Click  | Place selected body            |
| W/S    | Increase / Decrease mass       |
| A/D    | Increase / Decrease radius     |
| Q/E    | Change color                   |
| Space  | Pause / Resume simulation      |
| R      | Reset system                   |
| +/-    | Increase / Decrease speed      |
| X      | Switch to AI experimental mode |
