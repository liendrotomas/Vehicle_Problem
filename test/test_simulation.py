'''
Title: test_simulation
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the unit test for the Simulation class.
'''

import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.simulation import Simulation
from modules.vehicle import Vehicle
from modules.controller import PID_Discrete_Controller, No_Controller

def test_initialization():
    """Tests variables initialization"""
    mySim = Simulation(vehicle=Vehicle(mass=1,initial_velocity=10,k_kgpm=0.05), controller=No_Controller(), target_velocity=10, dt=1, sim_time=100, error_thr=1)
    assert mySim.vehicle == Vehicle(mass=1,initial_velocity=10,k_kgpm=0.05)          # Vehicle object
    assert mySim.controller == No_Controller()    # Controller object
    assert mySim.target_velocity == 10 # Velocity setpoint [m/s]
    assert mySim.dt == 1                    # Simulation time step [s]
    assert mySim.sim_time == 100        # Simulation duration [s]
    assert mySim.error_thr == 1      # Error threshold [%]
