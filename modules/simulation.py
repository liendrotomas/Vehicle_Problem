'''
Title: simulation
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the Simulation class definition which is used to assess the temporal behavior of a vehicle subject to a drag force and a controller.
            It also provides methods for plotting the output and extracting the metrics such as the settling time.
'''
import numpy as np
import matplotlib.pyplot as plt
from modules.vehicle import Vehicle
from modules.controller import Controller

class Simulation:
    """Definition of the Simulation Class"""
    def __init__(self,vehicle: Vehicle, controller:Controller, target_velocity:float, dt:float=1, sim_time:float=100, error_thr:float=1):
        """Definition of the Simulation Class attributes"""
        # Data validation
        if  not  isinstance(controller, Controller):
            raise TypeError('\'controller\' must be an object of class \'Controller\'')
        if  not  isinstance(vehicle, Vehicle):
            raise TypeError('\'vehicle\' must be an object of class \'Vehicle\'')
        if dt <= 0 or not isinstance(dt,(int,float)):
            raise ValueError('dt must be a positive float.')
        if sim_time <= 0 or not isinstance(sim_time,(int,float)):
            raise ValueError('sim_time must be a positive float.')
        
        self.vehicle = vehicle          # Vehicle object
        self.controller = controller    # Controller object
        self.target_velocity = target_velocity # Velocity setpoint [m/s]
        self.dt = dt                    # Simulation time step [s]
        self.sim_time = sim_time        # Simulation duration [s]
        self.error_thr = error_thr      # Error threshold [%]
        
        self.time = []                  # Time vector
        self.velocity = []              # Velocity vector
        self.error = []                 # Velocity vector


    def plot_velocity(self,label=''):
        """Used to plot the resulting velocity"""
        plt.figure(1)
        plt.plot(self.time, self.velocity,label=label)
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity [m/s]')
        plt.grid(visible=True)
        plt.legend()

    def plot_error(self,label=''):
        """Used to plot the resulting velocity error"""
        plt.figure(2)
        plt.plot(self.time, self.error,label=label)
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity Error [%]')
        plt.grid(visible=True)        
        plt.legend()
    
    def plot_velocity_sp(self):
        """Used to plot the velocity setpoint. This is not the best implementation, but was faster that handling axes/figures"""
        plt.figure(1)
        plt.plot(self.time,[self.target_velocity]*len(self.time),color='magenta',linestyle='--',label=f'Target velocity:{self.target_velocity}m/s')
        plt.legend()

    def plot_error_band(self):
        """Used to plot the velocity error band. This is not the best implementation, but was faster that handling axes/figures"""
        plt.figure(2)
        plt.plot(self.time, [self.error_thr]*len(self.time),color='red',label=f'$\pm${self.error_thr}% limit')
        plt.plot(self.time, [-self.error_thr]*len(self.time),color='red')
        plt.legend()

    def get_settling_time(self):
        """Used to extract the settling time of the result"""
        error_outside_th = np.where(np.array(self.error)>self.error_thr)[0] # Calculate elements outside the threshold
        if len(error_outside_th) == 0 or self.error[-1] > self.error_thr or np.isnan(self.error[-1]):
            return -1
        settling_time = self.time[error_outside_th[-1]]
        return settling_time
    
    def run(self):
        """Loop that simulates the temporal behavior of the vehicle with the drag force and the controller"""
        t = 0
        while t < self.sim_time:
            self.time.append(t)                                                 # Update timestamp
            self.velocity.append(self.vehicle.velocity)                         # Update velocity vector using the current vehicle's velocity
            error = (self.target_velocity - self.vehicle.velocity)              # Absolute error
            Fc = self.controller.update(error)                                  # Controller's output Fc
            self.error.append(error/self.target_velocity * 100)                 # Error calculated as percentage
            self.vehicle.velocity = self.vehicle.update(force=Fc,dt=self.dt)    # Calculate the new vehicle's velocity

            t += self.dt                                                        # Increase a time-step