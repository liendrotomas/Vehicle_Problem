import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self,sim_obj, dt=1, sim_time=100):
        # Simulation variables
        self.dt = dt                # Simulation time step [s]
        self.sim_time = sim_time    # Simulation duration [s]
        self.sim_obj = sim_obj
        
        self.time = []              # Time vector
        self.velocity = []          # Velocity vector

        self.time.append(0) 
        self.velocity.append(sim_obj.velocity) # First element is the initial velocity

    def plot_velocity(self,time, velocity):
        plt.plot(time, velocity)
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity [m/s]')
        plt.grid(visible=True)
        plt.title('Velocity profile')
        plt.show()

    def run(self):
        for ti in np.arange(self.dt,self.sim_time+self.dt, self.dt):
            self.time.append(ti)
            self.velocity.append(self.sim_obj.get_new_velocity(self.velocity[-1], self.dt))

        self.plot_velocity(self.time,self.velocity)
