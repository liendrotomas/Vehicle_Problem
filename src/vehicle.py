import numpy as np

class Vehicle:
    def __init__(self, mass, initial_velocity, k_kgpm, controller_obj):
        # Vehicle variables
        self.mass = mass # Vehicle mass [kg]
        self.velocity = initial_velocity # Vehicle velocity [m/s]
        
        # Force function variables
        self.k_kgpm = k_kgpm

        # Define vehicle controller
        self.controller = controller_obj

    def force_function(self, velocity): 
        return -np.sign(velocity) * self.k_kgpm * velocity **2
        
    def get_new_velocity(self, velocity, dt):
        Vf = velocity + self.force_function(velocity) * dt
        return Vf