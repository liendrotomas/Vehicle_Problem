'''
Title: vehicle
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the definition of the Vehicle Class.

'''
import numpy as np

class Vehicle:
    """Represents a 1D vehicle with initial velocity subject to a quadratic drag force"""
    def __init__(self, mass:float, initial_velocity:float, k_kgpm:float):
        """Vehicle initialization"""
        # Data validation
        if mass <= 0:
            raise ValueError("Mass must be positive.")

        self.mass = mass                    # Vehicle mass [kg]
        self.velocity = initial_velocity    # Vehicle velocity [m/s]
        
        # Drag force constant validation 
        if k_kgpm < 0:
            raise ValueError("k_kgpm cannot be negative.")
        self.k_kgpm = k_kgpm

    def get_drag(self):
        """Returns quadratic drag force"""
        return -np.sign(self.velocity) * self.k_kgpm * self.velocity **2 
        
    def update(self, force:float, dt: float):
        """Update vehicle's velocity based on the forces acting on it"""
        acceleration = (force + self.get_drag())/self.mass          # Calculates the acceleration of the vehicle given the forces acting on it.
        Vf = self.velocity + acceleration * dt                      # Calculates the velocity of the vehicle given the forces acting on it.
        return Vf