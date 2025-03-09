'''
Title: test_vehicle
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the unit test for the Vehicle class.
'''

import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.vehicle import Vehicle

def test_initialization():
    """Tests variables initialization"""
    myVehicle = Vehicle(mass=2,initial_velocity=10,k_kgpm=0.1)
    assert myVehicle.mass == 2
    assert myVehicle.velocity == 10
    assert myVehicle.k_kgpm == 0.1
    
    with pytest.raises(ValueError): # Verifies the data validation in Vehicle is working properly as negative k_kgpm is not allowed
        myVehicle = Vehicle(mass=1,initial_velocity=5,k_kgpm=-0.05)

    with pytest.raises(ValueError): # Verifies the data validation in Vehicle is working properly as negative mass is not allowed
        myVehicle = Vehicle(mass=-1,initial_velocity=5,k_kgpm=0.05)
    
    with pytest.raises(ValueError): # Verifies the data validation in Vehicle is working properly as negative mass is not allowed
        myVehicle = Vehicle(mass=0,initial_velocity=5,k_kgpm=0.05)

def test_friction():
    """Tests get_drag method"""
    myVehicle = Vehicle(mass=1,initial_velocity=0,k_kgpm=0.05)
    assert myVehicle.get_drag() == 0

    myVehicle = Vehicle(mass=0.1,initial_velocity=-9,k_kgpm=0.01)
    assert myVehicle.get_drag() == 0.81
    
    myVehicle = Vehicle(mass=10,initial_velocity=5,k_kgpm=0.05)
    assert myVehicle.get_drag() == -1.25

   
def test_update():
    """Tests update method"""
    myVehicle = Vehicle(mass=1,initial_velocity=0,k_kgpm=0.05)
    assert myVehicle.update(force=0, dt=0.01) == 0
    
    myVehicle = Vehicle(mass=1,initial_velocity=10,k_kgpm=0.05)
    assert myVehicle.update(force=0, dt=0.01) == 10 + myVehicle.get_drag()/myVehicle.mass*0.01
    
    myVehicle = Vehicle(mass=2,initial_velocity=5,k_kgpm=0.01)
    assert myVehicle.update(force=1.2, dt=0.01) == 5 + (1.2+myVehicle.get_drag())/myVehicle.mass*0.01