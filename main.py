'''
Title: main
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file sets up the scenario to simulate the motion of a 1D vehicle subject to a drag force and a force exerted by a controller.
'''

from modules.vehicle import Vehicle
from modules.simulation import Simulation
from modules.controller import *

import matplotlib.pyplot as plt
import logging
import numpy as np

def main():
    ######### Setup logger #########
    logging.basicConfig(level=logging.INFO)

    ######### Definition of constants #########
    MASS = 1                # vehicle mass [kg]
    INITIAL_VELOCITY = 10   # initial speed [m/s]
    TARGET_VELOCITY = 5     # initial speed [m/s]
    ERROR_BAND = 1          # [%]
    K_KGPM = 0.05           # Force constant [kg/m]
    SIM_TIME = 50           # Simulated time for plotting purposes [s]
    CONTROLLER_MODE = "PI"  # or "PID" 
    COEFFICIENTS_CALC = None # or "ZIEGLER" to calculate coefficients according to Ziegler-Nicholson.
    logging.info(f'Constants: MASS:{MASS}kg, INITIAL_VELOCITY:{INITIAL_VELOCITY}m/s, TARGET_VELOCITY:{TARGET_VELOCITY}m/s, ERROR_BAND:{ERROR_BAND}%, K_KGMP:{K_KGPM}kg/m, SIM_TIME:{SIM_TIME}s')
    
    ######### Output paths setup #########
    velocity_no_control_path = 'output/velocity_profile_no_control.png'
    error_plot_path = 'output/error_profile.png'
    error_plot_zoom_path = 'output/error_profile_zoom.png'

    ######### Discrete PID Controller parameters definition #########
    TS = 1                                              # Sampling time [s]
    if COEFFICIENTS_CALC == "ZIEGLER":                  # Used to calculate PID parameters based on Zieger Nicholson method
        KU = 0.8
        TU = 2.1
        velocity_control_path = f'output/velocity_profile_{CONTROLLER_MODE}_ZN.png'
        if CONTROLLER_MODE == "PI":
            # PI Parameters:
            KP = 0.45*KU
            KI = 0.54*KU/TU
            KD = 0
        elif CONTROLLER_MODE == "PID":
            # PID Parameters
            KP = 0.6*KU
            KI = 1.2*KU/TU
            KD = 0.075*KU*TU
    else: # Used to manually input PID parameters
        velocity_control_path = 'output/velocity_profile.png'
        KP = 0.28
        KI = 0.12
        KD = 0.05
    logging.info(f'Control parameters: : {CONTROLLER_MODE} Sampling Time:{TS}, Kp:{round(KP,4)}, Ki:{round(KI,4)}, Kd:{round(KD,4)}')

    ######### Simulation of Vehicle without controller #########
    myRover = Vehicle(mass=MASS, initial_velocity=INITIAL_VELOCITY,k_kgpm=K_KGPM)   # Initialization of the Vehicle object without controller
    logging.info('Initializing vehicle without controller')
    myController = No_Controller()
    simEnv_noControl = Simulation(vehicle=myRover,controller=myController,target_velocity=TARGET_VELOCITY,dt=TS, sim_time=SIM_TIME,error_thr=ERROR_BAND)                   # Simulation environment setup adding the Vehicle object
    simEnv_noControl.run()                                                                    # Run simulation
    simEnv_noControl.plot_velocity(label='Velocity profile')                                                          
    simEnv_noControl.plot_error(label='Velocity error profile')                                                          
    simEnv_noControl.plot_velocity_sp()
    simEnv_noControl.plot_error_band()

    plt.figure(1)
    plt.title('Vehicle velocity without controller')
    plt.savefig(velocity_no_control_path)
    plt.figure(2)
    plt.title('Vehicle velocity error without controller')
    logging.info(f'Velocity profile plot without controller saved in {velocity_no_control_path}')
    logging.info(f'Close figures to continue')
    plt.show()
    
    ######### Simulation of Vehicle with controller #########
    logging.info('Initializing vehicle with controller')                            
    myRover2 = Vehicle(mass=MASS, initial_velocity=INITIAL_VELOCITY,k_kgpm=K_KGPM)   # Initialization of the Vehicle object without controller
    myPIDController = PID_Discrete_Controller(kp=KP, ki=KI, kd=KD, Ts=TS) # Initialization of the Controller object
    simEnv_PID = Simulation(vehicle=myRover2,controller=myPIDController,target_velocity=TARGET_VELOCITY,dt=TS, sim_time=SIM_TIME,error_thr=ERROR_BAND)                   # Simulation environment setup adding the Vehicle object
    simEnv_PID.run()                                                                                        # Run simulation
    simEnv_noControl.plot_velocity(label='Velocity profile without controller')                                                                
    simEnv_PID.plot_velocity(label='Velocity profile with PID controller')                                                                      
    simEnv_PID.plot_error(label='Velocity error profile')                                                                      
    simEnv_PID.plot_velocity_sp()                                                                      
    simEnv_PID.plot_error_band()                                                                      
    
    plt.figure(1)
    plt.title(f'Vehicle velocity with PID controller\n (Settling time:{simEnv_PID.get_settling_time()}s, Error band {ERROR_BAND}%)')
    plt.savefig(velocity_control_path)
    logging.info(f'Velocity profile plot saved in {velocity_control_path}')
    plt.figure(2)
    plt.title(f'Vehicle velocity error with PID controller \n (Settling time:{simEnv_PID.get_settling_time()}s, Error band {ERROR_BAND}%)')
    plt.savefig(error_plot_path)
    plt.ylim((-2,2))
    plt.savefig(error_plot_zoom_path)
    logging.info(f'Error profile plot saved in {error_plot_path}')
    logging.info(f'Close figures to continue')
    plt.show()

    ######### Robustness with respect to the initial velocity #########
    logging.info(f'Starting robustness analysis...')
    velocity_vec = []
    settling_time = []
    for v0 in np.arange(start=-50, stop=50, step=5):
        myPIDController.reset()                                             # Resets PID parameters
        myRover3 = Vehicle(mass=MASS, initial_velocity=v0,k_kgpm=K_KGPM)    # Initialization of the Vehicle object without controller
        simEnv = Simulation(vehicle=myRover3,controller=myPIDController,target_velocity=TARGET_VELOCITY,dt=TS, sim_time=SIM_TIME,error_thr=ERROR_BAND)                   # Simulation environment setup adding the Vehicle object
        simEnv.run()
        ts = simEnv.get_settling_time()
        if ts != -1:
            simEnv.plot_velocity(label=f'V_0: {v0}m/s - ts: {ts}s')    
        velocity_vec.append(v0)
        settling_time.append(ts)
    plt.legend(loc='right')
    plt.title('Robustness analysis with respect to the initial velocity')
    plt.savefig('output/response_sensitivity.png')
    logging.info(f'Robustness analysis completed.')
    
    plt.figure()
    plt.plot(velocity_vec,settling_time)
    plt.title('Settling time as function of the initial velocity')
    plt.xlabel('Initial velocity [m/s]')
    plt.ylabel('Settling time [s]')
    plt.ylim((0,30))
    plt.grid(visible=True)
    plt.savefig('output/settling_time.png')
    plt.show()

    logging.info(f'Execution finished!')

if __name__=="__main__":
    main()