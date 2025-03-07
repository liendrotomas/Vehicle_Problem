from src.vehicle import Vehicle
from src.simulation import Simulation
from src.pid_controller import PID_Discrete_Controller

if __name__=="__main__":
    # Definition of constants
    MASS = 1                # vehicle mass [kg]
    INITIAL_VELOCITY = 10   # initial speed [m/s]
    K_KGPM = 0.05           # Force constant [kg/m]
    SIM_TIME = 100          # Simulated time for plotting purposes [s]

    # Definition of discrete PID Controller parameters
    TS = 0.1                # Sampling time [s]
    KP = 1
    KI = 1
    KD = 1

    # Initialization of the Vehicle object
    myController = PID_Discrete_Controller(kp=KP, ki=KI, kd=KD, Ts=TS)
    myRover = Vehicle(mass=MASS, initial_velocity=INITIAL_VELOCITY,k_kgpm=K_KGPM, controller_obj=myController)

    simEnv = Simulation(sim_obj=myRover,dt=TS, sim_time=SIM_TIME)
    simEnv.run()