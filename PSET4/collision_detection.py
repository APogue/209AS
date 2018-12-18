
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class parkingLot:
    # the parking lot contains the inertial frame A, A frame is 2D, x and y points only
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.origin = np.array([0, 0])

    def lot_dictionary(self):
        lot_info_dict = dict(length=self.length, width=self.width)
        return lot_info_dict

    def lot_plot_info(self):
        bottom_edge_point = np.array([self.width, 0])
        top_edge_point = np.array([0, self.length])
        diagonal_edge_point = np.array([self.width, self.length])
        lot_plot_points = np.vstack((self.origin, top_edge_point,
                                     diagonal_edge_point, bottom_edge_point))
        return lot_plot_points

class myCar:
    # this class instantiates the car, the car will exist in its own frame C, you could also use a class attribute here which is myCar.length
    def __init__(self, length, width, heading):
        self.length = length
        self.width = width
        # wrt frame A
        self.p_xy = 0
        self.heading = heading
        self.vel = 0
        self.ang_vel = 0

    def car_info(self): # this is the car information wrt the A frame
        car_info_dict = dict(origin = self.p_xy, heading = self.heading, lin_vel = self.vel, ang_vel = self.ang_vel)
        return car_info_dict

    def car_attribute_update(self, update_dict): # you can just use car_info as the argument
        self.p_xy = update_dict['origin']
        self.heading = update_dict['heading']
        self.vel = update_dict['lin_vel']
        self.ang_vel = update_dict['ang_vel']

    def car_bumper(self, v): # wrt frame C, this assumes the car doesn't hit an object if pivoting about a wheel
        # also assumes that the car cannot slip
        origin = np.array([[0, 0, 1]])
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
            mirror_bumper = np.vstack((-1*bumper[0, :0:-1], bumper[1:,1:]))
            bumper = np.append(mirror_bumper, bumper, axis=1)
            return bumper
        return 'car is not moving'

    def homogeneous_transform(self, point, angle):
        R = np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)], [0, 0]])
        T = np.hstack((R, np.array([point]).transpose()))
        return T

    def check_obstacle_collision(self, obstacle_dict):
        obs_length, obs_width = obstacle_dict['length'], obstacle_dict['width']
        T_ba = obstacle_dict['T_ba'] # Transform frame A wrt frame B
        # car wrt frame A
        T_ac = self.homogeneous_transform(self.p_xy, self.heading)
        # car wrt frame B (obstacle frame)
        T_bc = np.dot(T_ba, T_ac)
        # put either the front or back bumper in the B frame
        bumper = self.car_bumper(self.vel)
        bumper_fb = np.dot(T_bc, bumper)
        # check if the bumper is in collision w obstacle b
        copy_x = bumper_fb[0,:]
        mask_greater_than = copy_x > 0
        if not any(mask_greater_than):
            return False
        mask_less_than = copy_x < obs_width
        if not any(mask_less_than):
            return False
        mask_both = np.logical_and(mask_greater_than, mask_less_than)
        if not any(mask_both):
            return False
        boolean_x = mask_both
        boolean_x = boolean_x.astype(np.int)
        copy_y = bumper_fb[1, :]
        mask_greater_thany = copy_y > 0
        if not any(mask_greater_thany):
            return False
        mask_less_thany = copy_y < obs_length
        if not any(mask_less_thany):
            return False
        mask_bothy = np.logical_and(mask_greater_thany, mask_less_thany)
        if not any(mask_bothy):
            return False
        boolean_y = mask_bothy
        boolean_y = boolean_y.astype(np.int)
        collision_value = np.dot(boolean_x, boolean_y)
        if not collision_value:
            return False
        return True



    def check_boarder_collision(self, lot_dict):
        # max boarder in config space: in the event that the robot can rotate, just taking the worst case
        car_diag_dist = np.sqrt(self.length**2 + self.width**2)
        lot_length, lot_width = lot_dict['length'], lot_dict['width']
        # check parking lot in worst case config space
        if self.p_xy[0] < (0 + car_diag_dist)or self.p_xy[0] > (lot_width - car_diag_dist) \
            or self.p_xy[1] < (0 + car_diag_dist) or self.p_xy[1] < (lot_length - car_diag_dist):
            # put the bumper in the A frame
            T_ac = self.homogeneous_transform(self.p_xy, self.heading)
            bumper = self.car_bumper(self.vel)
            bumper_fa = np.dot(T_ac, bumper)
            copy_x = bumper_fa[0, :]
            copy_y = bumper_fa[1, :]
            if any(copy_x <0) or any(copy_x > lot_width) \
                    or any(copy_y < 0) or any(copy_y > lot_length):
                return True
        return False

    def car_plot_info(self):
        front_bumper = self.car_bumper(np.abs(self.vel))
        rear_bumper = self.car_bumper(-np.abs(self.vel))
        end_points = np.vstack((rear_bumper[:,0], front_bumper[:,0], front_bumper[:,-1], rear_bumper[:, -1])).transpose()
        # rotate them into the frame A
        T_ac = self.homogeneous_transform(self.p_xy, self.heading)
        car_plot_points = np.dot(T_ac, end_points).transpose()
        car_plot_points = car_plot_points[:, :2]
        return car_plot_points

class Obstacle:
    # this class instantiates the obstacles, they will exist in frames B, (not C) to Z
    def __init__(self, p_xy, length, width, orientation):
        self.length = length
        self.width = width
        self.orientation = orientation # defined wrt frame A
        self.origin = p_xy # this is the origin in frame A
        self.T_inv, self.T_ab = self.homogeneous_transform()

    def obstacle_dictionary(self):
        obstacle_info_dict = dict(origin = self.origin, orientation = self.orientation,
                                  length=self.length, width=self.width, T_ba = self.T_inv)
        return obstacle_info_dict

    def homogeneous_transform(self):
        R = np.array([[np.cos(self.orientation), -np.sin(self.orientation)],
                      [np.sin(self.orientation), np.cos(self.orientation)], [0, 0]])
        T = np.hstack((R, np.array([self.origin]).transpose()))
        self.T_inv, self.T_ab = np.linalg.inv(T), T
        return self.T_inv, self.T_ab

    def obstacle_plot_info(self):
        origin = np.array([0, 0, 1]) # in the obstacles frame B, the origin is always at 0
        bottom_edge_point = np.array([self.width, 0, 1])
        top_edge_point = np.array([0, self.length, 1])
        diagonal_edge_point = np.array([self.width, self.length, 1])
        obstacle_points = np.vstack((origin, top_edge_point,
                                     diagonal_edge_point, bottom_edge_point)).transpose()
        obstacle_plot_points = np.dot(self.T_ab, obstacle_points).transpose()
        obstacle_plot_points = obstacle_plot_points[:, :2]
        return obstacle_plot_points






if __name__ == '__main__':

    car = myCar(80, 85)
    car.p_xy = np.array([0, 0, 1])
    car.heading = 0*np.pi/180
    car.vel = 1
    car.ang_vel = 1

    obstacle = Obstacle(car.p_xy, 100, 100, 0)
    obstacle.obstacle_dictionary()

    lot = parkingLot(500, 700)

    check = car.check_obstacle_collision(obstacle.obstacle_dictionary())
    parking_lot = parkingLot(500, 700)
    check2 = car.check_boarder_collision(parking_lot.lot_dictionary())
    print(obstacle.obstacle_plot_info())
    print(car.car_plot_info())
    print(lot.lot_plot_info())










