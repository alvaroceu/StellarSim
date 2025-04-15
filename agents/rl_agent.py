import numpy as np
import random
import math

class RLAgent:
    """
    A basic Q-learning agent that learns to launch planets into orbit by selecting
    velocity and angle combinations based on received rewards.
    """

    def __init__(self, pos_bins=10, vel_bins=10, angle_bins=12, learning_rate=0.1, discount=0.95, epsilon=1.0, epsilon_decay=0.995):
        self.vel_bins = vel_bins # 10 possible velocity values
        self.angle_bins = angle_bins # 12 possible angle values
        self.pos_bins = pos_bins  # 10 possible planet's initial positions (for x and y)

        self.learning_rate = learning_rate # Importance of new tries
        self.discount = discount # Importance of future tries
        self.epsilon = epsilon # % of random tries
        self.epsilon_decay = epsilon_decay # Reduces epsilon value after each try

        # Action space ranges --> ranges will be determined by vel_bins, angle_bins and pos_bins
        self.vel_range = (0.5, 5.0)  # min and max velocity
        self.angle_range = (0.0, 2 * math.pi) # min and max angle
        self.pos_range = (-300, 300) # min and max planet's initial position

        # Q-table [velocity_bin, angle_bin]: Each combination has a estimated output (good or bad try)
        self.q_table = np.zeros((pos_bins, pos_bins, vel_bins, angle_bins))

        self.last_action = None
        self.last_state = None

    def select_action(self, dx, dy):
        """
        Chooses a velocity and angle either randomly (exploration) or via the Q-table (exploitation).
        """

        px_bin, py_bin = self.discretize_position(dx, dy)


        if random.random() < self.epsilon:
            # Explore new tries
            v_bin = random.randint(0, self.vel_bins - 1)
            a_bin = random.randint(0, self.angle_bins - 1)
        else:
            # Exploit with known tries (if exist in that position)
            q_values = self.q_table[px_bin, py_bin]
            idx = np.unravel_index(np.argmax(q_values), q_values.shape) # Get best known try parameters
            v_bin, a_bin = idx # Use best known try parameters

        self.last_action = (px_bin, py_bin, v_bin, a_bin)
        return self._bin_to_action(v_bin, a_bin)

    def give_feedback(self, reward):
        """
        Updates the Q-table based on the outcome of the last action.
        """
        px_bin, py_bin, v_bin, a_bin = self.last_action
        current_q = self.q_table[px_bin, py_bin, v_bin, a_bin]
        max_future_q = np.max(self.q_table[px_bin, py_bin])

        # Q-learning update rule. 
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount * max_future_q)
        self.q_table[px_bin, py_bin, v_bin, a_bin] = new_q

        # Reduce exploration with each try
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(0.01, self.epsilon) # Never go fully greedy

    def _bin_to_action(self, v_bin, a_bin):
        """
        Converts discrete bin indices to continuous velocity and angle values.
        """

        # Every bin index has an associated velocity/angle 
        v_min, v_max = self.vel_range
        a_min, a_max = self.angle_range

        velocity = v_min + (v_max - v_min) * v_bin / (self.vel_bins - 1)
        angle = a_min + (a_max - a_min) * a_bin / (self.angle_bins - 1)

        return velocity, angle
    
    def discretize_position(self, dx, dy):
        """
        Discretizes a position (dx, dy) relative to the sun into bins.
        """
        min_val, max_val = self.pos_range
        bin_size = (max_val - min_val) / self.pos_bins

        px_bin = int((dx - min_val) / bin_size)
        py_bin = int((dy - min_val) / bin_size)

        # Clamp values
        px_bin = max(0, min(px_bin, self.pos_bins - 1))
        py_bin = max(0, min(py_bin, self.pos_bins - 1))

        return px_bin, py_bin

