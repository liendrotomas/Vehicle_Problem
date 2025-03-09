'''
Title: controller
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the definitions of the controller abstract class and the controllers used:
    - PID_Discrete_Controller
    - No_Controller
'''
from abc import ABC, abstractmethod

class Controller(ABC):
    """Parent class to define a template and a clear interface with controllers"""
    @abstractmethod
    def update(self, error):
        pass

class PID_Discrete_Controller(Controller):
    """Implementation of a discrete PID Controller"""
    def __init__(self, kp:float, ki:float, kd:float, Ts:float) -> None:
        self.kp = kp    # Proportional gain
        self.ki = ki    # Integral gain
        self.kd = kd    # Derivative gain
        self.Ts = Ts    # Sampling time [s]
        
        self.error_int = 0      # Initialization of integral component
        self.error_prev = None  # Initialization of previous error value to compute derivative component

    def update(self, error:float) -> float:
        """Updates the controller output"""
        # Compute integral component
        self.error_int = self.error_int + error 

        # Compute derivative component
        if not self.error_prev is None: # At least two samples are required to compute the derivative.
            error_der = (error-self.error_prev)/self.Ts
        else:
            error_der = 0
        self.error_prev = error

        # Compute PID Output
        return error * self.kp + self.error_int * self.ki + error_der * self.kd
    
    def reset(self):
        """Resets parameters"""
        self.error_int = 0      # Initialization of integral component
        self.error_prev = None  # Initialization of previous error value to compute derivative component

class No_Controller(Controller):
    """Class used to simulate the absence of a controller while maintaining the interfaces well-defined"""
    def __init__(self):
        super().__init__()

    def update(self, error):
        """Updates the controller output as always 0"""
        return 0