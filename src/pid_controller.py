class PID_Discrete_Controller:
    def __init__(self, kp, ki, kd, Ts):
        self.kp = kp    # Proportional gain
        self.ki = ki    # Integral gain
        self.kd = kd    # Derivative gain
        self.Ts = Ts    # Sampling time [s]

    def update(self, error):
        return error * self.kp + error_int * self.ki + error_der * self.kd