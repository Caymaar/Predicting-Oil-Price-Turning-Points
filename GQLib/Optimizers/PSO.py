from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
import random
from GQLib.LPPL import LPPL
import json
from .abstract_optimizer import Optimizer
from ..njitFunc import (
    njit_calculate_fitness,
    njit_selection,
    njit_crossover,
    njit_immigration_operation,
    njit_mutate,
    njit_initialize_population,
    njit_update_position,
    njit_update_velocity

)


class PSO(Optimizer):
    """
    Particle Swarm Optimisation for optimizing LPPL parameters.

    Particle Swarm Optimization (PSO) is a nature-inspired optimization algorithm that mimics the social behavior of birds flocking or fish schooling. 
    The algorithm involves a group of particles, each representing a set of parameters of the model, which collectively explore 
    the search space to find the optimal solution (minimum RSS).  These particles move through the space by adjusting their positions and velocities based 
    on two primary influences: the best solution they have individually found and the best solution discovered by the entire group. 
    Over successive iterations, particles communicate and learn from each other, progressively converging towards the optimal region of the search space.
    """

    def __init__(self,  w: float = 0.8, c1: float = 1.2, c2: float =1.2) -> None:
        """
        Initialize the PSO optimizer.

        Parameters
        ----------
        
        w : float
            Weight in the velocity calculation corresponding to the inertia of the particle.
            The larger the parameter, the more freedom the particle has to move.
        
        c1 : float
            Weight in the velocity calculation corresponding to the memory of the local best position.
            The larger the parameter, the closer the particle will want to get to its local minimum.

        c2 : float
            Weight in the velocity calculation corresponding to the memory of the global best position.
            The larger the parameter, the closer the particle will want to get to the global best position of the swarm

        """
        self.w = w # Inertia weight
        self.c1 = c1 # Cognitive coefficient
        self.c2 = c2 # Social coefficient
        # Load optimization parameters from a JSON configuration file
        with open("params/params_pso.json", "r") as f:
            params = json.load(f)

        self.PARAM_BOUNDS = params["PARAM_BOUNDS"]
        self.NUM_PARTICLES = params["NUM_PARTICLES"]
        self.MAX_GEN = params["MAX_GEN"]

    def fit(self, start: int, end: int, data: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Fit LPPL parameters using the MPGA optimizer.

        Parameters
        ----------
        start : int
            The start index of the subinterval.
        end : int
            The end index of the subinterval.
        data : np.ndarray
            A 2D array of shape (J, 2), where:
                - Column 0 is time.
                - Column 1 is the observed price.

        Returns
        -------
        Tuple[float, np.ndarray]
            - Best fitness value (RSS) as a float.
            - Best chromosome (parameters: t_c, alpha, omega, phi) as a 1D NumPy array.
        """
        param_bounds = self.convert_param_bounds(end)

        # Initialize particles with initial fitness values
        particles = [
            Particle(param_bounds, data, w = self.w, c1 = self.c1, c2 =  self.c2)
            for _ in range(self.NUM_PARTICLES)
        ]

        # Compute initial global best particle
        best_particle : Particle = min(particles, key=lambda p: p.local_best_fitness)
        global_best_fitness = best_particle.local_best_fitness
        global_best_solution = best_particle.local_best_position

        current = 0
        # Iterate through the generations
        while current <= self.MAX_GEN:

            # Update each particle position in the swarm
            for m in range(self.NUM_PARTICLES):
                particles[m].update_position(global_best_solution, data)
            
            # Update the new global best particle
            best_particle : Particle = min(particles, key=lambda p: p.local_best_fitness)
            if best_particle.local_best_fitness < global_best_fitness:
                global_best_fitness = best_particle.local_best_fitness
                global_best_solution = best_particle.local_best_position

            current+=1
        
        return global_best_fitness, global_best_solution
    
class Particle():
    """
    In Particle Swarm Optimization, a particle represents a potential solution to the optimization problem being addressed
    Each particle is characterized by its position in the search space, which corresponds to a set of parameters of the model
    and its velocity vector, which determines the direction and magnitude of its movement. As the algorithm progresses, the particle 
    adjusts its position by considering its own past experiences and the knowledge gained from other particles in the swarm.
    """

    def __init__(self, param_bounds: np.ndarray, data: np.ndarray, 
                 w: float = 0.8, c1: float = 1.2, c2: float =1.2):
        """
        Initialize a particle for particle Swarm Optimisation
        
        Parameters
        ----------
        param_bounds : np.ndarray, shape (D, 2)
            Rows correspond to each parameter [low, high].
            For instance, if we have 4 parameters:
                param_bounds[0] = [t_c_min, t_c_max]
                param_bounds[1] = [omega_min, omega_max]
                param_bounds[2] = [phi_min, phi_max]
                param_bounds[3] = [alpha_min, alpha_max]

        data : np.ndarray
            A 2D array of shape (J, 2), where:
                - Column 0 is time.
                - Column 1 is the observed price.

        w : float
            Weight in the velocity calculation corresponding to the inertia of the particle.
            The larger the parameter, the more freedom the particle has to move.
        
        c1 : float
            Weight in the velocity calculation corresponding to the memory of the local best position.
            The larger the parameter, the closer the particle will want to get to its local minimum.

        c2 : float
            Weight in the velocity calculation corresponding to the memory of the global best position.
            The larger the parameter, the closer the particle will want to get to the global best position of the swarm.
        """

        self.param_bounds = param_bounds
        num_params = self.param_bounds.shape[0]  # D
        self.position = np.empty(num_params, dtype=np.float64)

        # Initialize the parameters according to their bounds
        for i, bounds in enumerate(self.param_bounds): 
            self.position[i] = np.random.uniform(bounds[0], bounds[1])
        
        # Initialize particle (local) best position and best fitness associated
        self.local_best_position : np.ndarray = self.position[0]
        self.local_best_fitness : float = np.inf

        # Compute the fitness of the newly created particle
        self.compute_fitness(data)

        self.velocity = np.zeros(num_params)
        self.w = w # Inertia weight
        self.c1 = c1 # Cognitive coefficient
        self.c2 = c2 # Social coefficient

    def compute_fitness(self, data: np.ndarray):
        """
        Compute the fitness of the given particle with actual position (= set of parameters).
        Update the best position that occured in the life of the particle.

        Parameters
        ----------
        data : np.ndarray
            A 2D array of shape (J, 2), where:
                - Column 0 is time.
                - Column 1 is the observed price.
        """
        # Call numba fonction of the LPPL model to compute fitness
        fit = LPPL.numba_RSS(self.position, data)

        # Update the particle best position and best fitness associated
        if fit < self.local_best_fitness:
            self.local_best_position = self.position
            self.local_best_fitness = fit
            
    def update_position(self, global_best_position: np.ndarray, data: np.ndarray):
        """
        Compute the velocity vector of the particle according to the best position in the swarm.
        Update the position of the particle with the new velocity.

        Parameters
        ----------
        global_best_position : np.ndarray
            Set of parameters corresponding to the best particle in the swarm according to the fitness

        data : np.ndarray
            A 2D array of shape (J, 2), where:
                - Column 0 is time.
                - Column 1 is the observed price.
        """
        self.velocity = njit_update_velocity(self.velocity, self.position, self.local_best_position, 
                                             global_best_position, self.w, self.c1, self.c2)
        
        self.position = njit_update_position(self.position, self.velocity, self.param_bounds)
        
        self.compute_fitness(data)
