'''
Title: test_pid_controller
Author: Tomas Liendro
Scope: Vehicle Control Problem

Description: This file contains the unit test for the PID_Discrete_Controller class.
'''

import pytest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.controller import PID_Discrete_Controller,Controller 

def test_initialization():
    # PID controller initialization
    pid = PID_Discrete_Controller(kp=1.0, ki=0.1, kd=0.01, Ts=0.01)
    assert isinstance(pid, Controller)
    assert pid.kp == 1.0
    assert pid.ki == 0.1
    assert pid.kd == 0.01
    assert pid.Ts == 0.01
    assert pid.error_int == 0
    assert pid.error_prev is None

def test_update():
    # PID controller initialization
    pid = PID_Discrete_Controller(kp=1.0, ki=0.1, kd=0.01, Ts=0.1) 
    # Zero-error test
    assert pid.update(0.0) == 0.0

    # Non-zero negative test
    pid = PID_Discrete_Controller(kp=1.0, ki=0.1, kd=0.01, Ts=0.1) 
    assert pid.update(-5) == pid.kp * (-5) + pid.ki * (-5)

    # Non-zero negative test after two succesive calls
    pid = PID_Discrete_Controller(kp=1.0, ki=0.1, kd=0.01, Ts=0.1) 
    assert pid.update(1) == pid.kp * 1 + pid.ki * 1
    assert pid.update(0.5) == pid.kp * 0.5 + pid.ki * (1+0.5) + (0.5-1)/pid.Ts * pid.kd

