'''
Title: test_no_controller
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the unit test for the No_Controller class.
'''

import pytest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.controller import No_Controller, Controller

def test_initialization():
    # PID controller initialization
    controller = No_Controller()
    # Verify that the class is correctly initialized
    assert isinstance(controller, Controller)
    assert isinstance(controller, No_Controller)

def test_update():
    # No_controller initialization
    controller = No_Controller() 
    # Test update method
    assert controller.update(0) == 0
    assert controller.update(10) == 0
    assert controller.update(-100) == 0
