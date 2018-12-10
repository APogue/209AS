


import numpy as np


class parkingLot:
    # the parking lot contains the inertial frame A, A frame is 2D, x and y points only
    def __init__(self, width, height):
        self.width = width
        self.height = height


class myCar:
  # this class instantiates the car, the car will exist in its own frame C
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.heading = 0 # defined wrt frame A
        self.origin = np.array([[0, 0, 1]]) # the 1 is so that the position can be translated
        self.pxy = 0
        self.theta = 0
        self.vel = 0
        self.omega = 0

    def car_location(self, p_xy, theta, vel, omega): # this is the car location wrt the A frame
        self.pxy = p_xy
        self.theta = theta
        self.vel = vel
        self.omega = omega

        car_info = dict(origin = p_xy, heading = theta, lin_vel = vel, ang_vel = omega)
        return car_info

    def car_bumper(self, v):
        origin = np.array([[0, 0, 1]])  # the 1 is so that the position can be translated
        if v != 0:
            n = 5
            number_spaces = self.width/n -1
            bumper_space = self.width/number_spaces
            if v > 0:
                bumper = np.transpose(origin + np.array([0, self.length - 10, 0]))
            if v < 0:
                bumper = np.transpose(origin + np.array([0, -10, 0]))
            for i in np.arange(1, number_spaces / 2 + 1):
                bumper_point = np.transpose(bumper[:, 0] + np.array([[bumper_space, 0, 0]]) * i)
                bumper = np.append(bumper, bumper_point, axis=1)
            mirror_bumper = np.vstack((-1*bumper[0,1:], bumper[1:,1:]))
            bumper = np.append(bumper, mirror_bumper, axis=1)
            return bumper
        return 'car is not moving'

    def check_collision(self, obstacle_origin, obstacle_orientation):



class Obstacle: # this will require instance attributes that are specific to an instance of a class
  # this class instantiates the obstacles, they will exist in frames B, (not C) to Z
    def __init__(self, p_xy, length, width, orientation):
        self.length = length
        self.width = width
        self.orientation = orientation # defined wrt frame A
        self.origin = p_xy.transpose()


if __name__ == '__main__':

    car = myCar(80, 85, 0)
    bumper_points = car.car_bumper(-1)
    print(bumper_points)








