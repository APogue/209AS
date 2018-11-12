
import numpy as np
import math


class DistanceGenerator(object):
    def __init__(self, x, y, theta, width, length):
        self.x = x
        self.y = y
        self.theta = theta
        self.location = np.array([x, y])
        self.x_line_vertical = width
        self.y_line_horizontal = length
        self.min_distance = 0
        self.test_points = [[0, 0], [0, 0]]
        self.landmark_point = np.zeros(2)
        self.distance = 0

    def laser_output(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.location = np.array([x, y])
        test_points = self.valid_points()
        shape = np.shape(test_points)
        self.distance = np.zeros(int(shape[0]))

        for m, n in enumerate(test_points):
            self.distance[m] = self.distance_calc(n)
        self.min_distance = np.min(self.distance)
        return self.min_distance

    def direction_calc(self, X, nhat):
        rho = np.dot(X, nhat)/np.linalg.norm(X)
        value = np.round(rho, 0) + 1
        return value

    def distance_calc(self, point):
        distance = np.sqrt((point[0] - self.location[0])**2 + (point[1] - self.location[1])**2)
        return distance

    def valid_points(self):
        phi = self.theta + np.pi / 2
        nhat = np.array([np.cos(phi), np.sin(phi)])
        slope = np.tan(phi)
        y_int = self.y - slope*self.x
        direction_check = np.zeros(4)
        X = np.zeros((4, 2))

        if np.absolute(slope) < 1e-12:
            condition = 'slope is zero'
            slope = slope + 1
            alt_slope = 0
        else:
            condition = 'slope is not zero'
            alt_slope = slope

        # start with the y-int
        X[0] = np.array([0.0, y_int])
        # x-int
        X[1] = np.array([-y_int/slope, 0.0])
        # vertical line
        X[2] = np.array([self.x_line_vertical, alt_slope*self.x_line_vertical + y_int])
        # horizontal line
        X[3] = np.array([(self.y_line_horizontal-y_int)/slope, self.y_line_horizontal])
        bob = 2
        if condition == 'slope is zero':
            X = X[0::2]
            bob = 1
        elif np.absolute(slope) > 1e10:
            X = X[1::2]
            bob = 1
        X_relative = X - self.location

        i = 0
        while np.linalg.norm(direction_check) <= bob:
            direction_check[i] = self.direction_calc(X_relative[i], nhat)
            i += 1
        direction_index = [k for k, e in enumerate(direction_check) if e != 0]
        self.test_points = [X[direction_index[p]] for p, v in enumerate(direction_index)]
        return self.test_points

    def get_landmarks(self):
        landmark = np.argmin(self.distance)
        self.landmark_point = self.test_points[np.asscalar(landmark)]
        return self.landmark_point


class car_simulation(DistanceGenerator):
    def __init__(self, r, phi_1, phi_2, L, dt, total_time, x, y, theta, width, length):
        super(car_simulation, self).__init__(x, y, theta, width, length)
        self.x_i = x
        self.y_i = y
        self.theta_i = theta
        self.loops = np.round(total_time/dt, 0)
        self.r = r
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.L = L
        self.sensor_output = np.zeros((int(self.loops), 4))
        self.dt = dt
        self.z = np.zeros((int(self.loops), 5))
        self.v_t = ((self.r * self.phi_1) + (self.r * self.phi_2)) / 2

    def get_simulation(self):
        # precompute the car simulation
        i = 0
        x_t_state = self.x_i
        y_t_state = self.y_i
        theta_t_state = self.theta_i
        bias_state = 0.05
        while i < self.loops:
            w_omega_t = np.random.normal(0, 0.0288)
            w_v_t = np.random.normal(0, .0288)
            omega_t_state = ((self.r*self.phi_1) - (self.r*self.phi_2))/self.L + w_omega_t
            x_t_state = x_t_state + (self.v_t + w_v_t)*math.cos(theta_t_state + np.pi/2)*self.dt
            y_t_state = y_t_state + (self.v_t + w_v_t)*math.sin(theta_t_state + np.pi/2)*self.dt
            theta_t_state = (theta_t_state + 2 * np.pi) % (2 * np.pi) + omega_t_state*self.dt
            bias_state = bias_state
            self.z[i][:] = np.array([x_t_state, y_t_state,
                                     theta_t_state, omega_t_state, bias_state])
            i = i + 1
        return self.z

    def get_sensor_simulation(self):
        # precompute the sensor output
        i = 0
        while i < self.loops:
            distance_one = self.laser_output(self.z[i][0], self.z[i][1], self.z[i][2])
            distance_two = self.laser_output(self.z[i][0], self.z[i][1], self.z[i][2] + np.pi/2)
            distance_one = distance_one + np.random.normal(0, 0.002*distance_one)
            distance_two = distance_two + np.random.normal(0, .002*distance_one)
            theta_t_measured = self.z[i][2] + np.random.normal(0, .00122) + self.z[i][4]
            omega_t_measured = self.z[i][3] + np.random.normal(0, .00122)
            self.sensor_output[i][:] = np.array([distance_two, distance_one,
                                                 theta_t_measured, omega_t_measured])
            i = i + 1
        return self.sensor_output

def find_F_t(F_t,theta_t_hat, v_t, dt): # good
    F_t[0][2] = -1 * v_t * np.sin(theta_t_hat + np.pi/2) * dt
    F_t[1][2] = v_t * np.cos(theta_t_hat + np.pi/2) * dt
    F_t[0][0], F_t[1][1], F_t[2][2], F_t[3][3], F_t[4][4] = 1, 1, 1, 1, 1
    return F_t


def find_W_t(W_t,theta_t_hat, dt): # good
    W_t[0][0] = math.cos(theta_t_hat + np.pi/2) * dt
    W_t[1][0] = math.sin(theta_t_hat + np.pi/2) * dt
    W_t[2][1] = dt
    W_t[3][1] = 1
    return W_t


def find_H_t(H_t,observation,z_bar,landmark_values): # good
    x_bar = z_bar[0]
    y_bar = z_bar[1]
    x_l1_bar = landmark_values[0][0]
    y_l1_bar = landmark_values[0][1]
    x_l2_bar = landmark_values[1][0]
    y_l2_bar = landmark_values[1][1]
    d1_bar = observation[0]
    d2_bar = observation[1]
    H_t[0][0] = (x_bar - x_l1_bar)/d1_bar
    H_t[0][1] = (y_bar - y_l1_bar)/d1_bar
    H_t[1][1] = (y_bar - y_l2_bar)/d2_bar
    H_t[1][0] = (x_bar - x_l2_bar)/d2_bar
    H_t[2][2], H_t[2][4], H_t[3][3] = 1, 1, 1
    return H_t


class EKF(car_simulation):
    c1 = 1e2 # trust the measurement over the model
    c2 = 1e2
    c3 = 1e3
    c4 = 1e3
    c5 = 1e3
    c6 = .01

    def __init__(self, phi_1, phi_2, dt, L, r, total_time, x, y, theta, width, length):
        super(EKF, self).__init__(r, phi_1, phi_2, L, dt, total_time, x, y, theta, width, length)
        self.z_hat = np.zeros(5)
        self.z_hat[0] = x
        self.z_hat[1] = y
        self.z_hat[2] = theta
        self.z_hat[3] = 0
        self.z_hat[4] = 0.05 # without the bias state it tracks perfectly
        self.z_bar = np.zeros(5)
        self.landmark_0 = 0
        self.landmark_1 = 0
        self.F_t = np.zeros((5, 5))
        self.W_t = np.zeros((5, 2))
        self.sigma_hat = np.diag(np.ones(5))*0
        self.sigma_bar = np.zeros((5, 5))
        self.H_t = np.zeros((4, 5))
        self.observation_model = np.zeros(4)
        self.Q = np.diag(np.array([self.c1, self.c2]))
        # self.R = np.diag(np.array([self.c3 * np.random.normal(0, 0.04), self.c4 * np.random.normal(0, 0.04),
        #                            self.c5 * np.random.normal(0, .001), self.c6 * np.random.normal(0, .001)]))
        self.R = np.diag(np.array([self.c3, self.c4,
                                   self.c5, self.c6]))

        self.kalman_gain = np.zeros((5, 4))
        self.error = 0
        
    def time_propagation_update(self):
        x_t_hat = self.z_hat[0]
        y_t_hat = self.z_hat[1]
        theta_t_hat = self.z_hat[2]
        omega_t_hat = self.z_hat[3]
        bias = self.z_hat[4]
        #print self.z_hat
        x_t_plus_one_bar = x_t_hat + self.v_t*math.cos(theta_t_hat + np.pi/2)*self.dt
        y_t_plus_one_bar = y_t_hat + self.v_t*math.sin(theta_t_hat + np.pi/2)*self.dt
        theta_t_plus_one_bar = (theta_t_hat + 2 * np.pi) % (2 * np.pi) + omega_t_hat*self.dt
        omega_t_plus_one_bar = omega_t_hat
        bias_plus_one_bar = bias

        self.z_bar[0] = x_t_plus_one_bar
        self.z_bar[1] = y_t_plus_one_bar
        self.z_bar[2] = theta_t_plus_one_bar
        self.z_bar[3] = omega_t_plus_one_bar
        self.z_bar[4] = bias_plus_one_bar
        #print self.z_bar
        return self.z_bar

    def time_linearization(self):
        theta_t_hat = self.z_hat[2]
        self.F_t = find_F_t(self.F_t, theta_t_hat, self.v_t, self.dt)
        self.W_t = find_W_t(self.W_t, theta_t_hat, self.dt)
        this = np.dot(self.F_t, self.W_t)
        these = np.dot(this, self.Q)
        that = np.dot(these, np.transpose(self.W_t))
        those = np.dot(that, np.transpose(self.F_t))
        eval, evec = np.linalg.eig(those)
        # print('controllability evals from F')
        # print(eval)
        return self.F_t, self.W_t

    def covariance_update(self): # good
        sigma_t_plus_one_temp1 = np.dot(self.F_t, self.sigma_hat)
        sigma_t_plus_one_temp2 = np.dot(sigma_t_plus_one_temp1, np.transpose(self.F_t))
        sigma_t_plus_one_temp3 = np.dot(self.W_t, self.Q)
        sigma_t_plus_one_temp4 = np.dot(sigma_t_plus_one_temp3, np.transpose(self.W_t))
        self.sigma_bar = sigma_t_plus_one_temp2 + sigma_t_plus_one_temp4
        #self.sigma_bar = .5 * self.sigma_bar + .5 * np.transpose(self.sigma_bar)
        eigval, eigvec = np.linalg.eig(self.sigma_bar)
        # print('controllability eigenvalues')
        # print(eigval)
        return self.sigma_bar

    def get_observation_model(self): # good
        x_bar = self.z_bar[0]
        #print 'location'
        #print x_bar
        y_bar = self.z_bar[1]
        #print y_bar
        theta_bar = self.z_bar[2]
        omega_bar = self.z_bar[3]
        bias_bar = self.z_bar[4]
        distance_one_bar = self.laser_output(x_bar, y_bar, theta_bar)
        #print 'distance one'
        #print distance_one_bar
        self.landmark_0 = self.get_landmarks()
        distance_two_bar = self.laser_output(x_bar, y_bar, theta_bar + np.pi / 2)
        #print distance_two_bar
        self.landmark_1 = self.get_landmarks()
        self.observation_model[0] = distance_two_bar + np.random.normal(0, 0.002*distance_two_bar)
        self.observation_model[1] = distance_one_bar + np.random.normal(0, 0.002*distance_one_bar)
        self.observation_model[2] = theta_bar + bias_bar + np.random.normal(0, 0.00122)
        self.observation_model[3] = omega_bar + np.random.normal(0, 0.00122)
        return self.observation_model

    def observation_linearization(self): # good
        landmark_values = [self.landmark_0, self.landmark_1]
        self.H_t = find_H_t(self.H_t, self.observation_model, self.z_bar, landmark_values)
        self.H_t = np.absolute(self.H_t)
        return self.H_t


    def kalman_gain_value(self): # good
        inner_temp1 = np.dot(self.H_t, self.sigma_bar)
        #print inner_temp1
        inner_temp2 = np.dot(inner_temp1, self.H_t.transpose())
        #print self.sigma_bar
        inner_temp3 = inner_temp2 + self.R
        #print np.dot(self.H_t, self.H_t.transpose())
        inner_temp4 = np.linalg.inv(inner_temp3)
        #print inner_temp4
        outer_temp = np.dot(self.sigma_bar, self.H_t.transpose())
        #print outer_temp
        self.kalman_gain = np.dot(outer_temp, inner_temp4)
        #print self.kalman_gain
        #self.kalman_gain = np.zeros((5,4))
        #self.kalman_gain[0][0], self.kalman_gain[1][1], self.kalman_gain[2][2], self.kalman_gain[3][3] = 1,1,1,1
        #print self.kalman_gain
        return self.kalman_gain

    def error_calculation(self, sensor_read):
        this = self.get_observation_model()
        self.error = sensor_read - self.observation_model
        #print sensor_read[2]
        #print self.observation_model[2]
        self.error[2] = self.error[2]%(2*np.pi)
        if self.error[2] > np.pi:
            self.error[2] -= 2*np.pi
        #print self.error
        #self.error[2] = 0
        #print self.kalman_gain*self.error
        return self.error
        
    def conditional_mean(self): # good last resort change the model to something linear
        temp_product = np.dot(self.kalman_gain, self.error)
        # print(self.error)
        self.z_hat = self.z_bar + temp_product
        #print self.this
        #print self.z_bar
        #print self.kalman_gain
        #print self.z_hat
        #self.z_hat[2:4] = 0
        #print self.z_hat
        return self.z_hat

    def observation_update_covariance(self): # good
        inner_product1 = np.dot(self.kalman_gain, self.H_t)
        inner_product2 = np.dot(inner_product1, self.sigma_bar)
        self.sigma_hat = self.sigma_bar - inner_product2
        #self.sigma_hat = .5 * self.sigma_bar + .5 * np.transpose(self.sigma_hat)
        eigval, eigvec = np.linalg.eig(self.sigma_hat)
        print('observability eigenvalues')
        print(eigval)
        return self.sigma_hat

# #ddd
# if __name__ == '__main__':
#     k = 0
#     input1 = -.2
#     input2 = .1
#     sim_time = 5 # the car travels at 20 mm per second
#     wheel_radius = 20
#     width = 500
#     length = 750
#     wheel_base = 85
#     time_step = .01
#     x_i = 300
#     y_i = 300
#     theta_i = 0
#     car = car_simulation(wheel_radius, input1, input2, wheel_base, time_step, sim_time, x_i, y_i, theta_i, width, length)
#     car_state = car.get_simulation()
#     car_sensor_readout = car.get_sensor_simulation()
#     estimator = EKF(input1, input2, time_step, wheel_base, wheel_radius, sim_time, x_i, y_i, theta_i, width, length)
#     z_hat_list = np.zeros((1, 5))
#     while k < car.loops:
#         z_bar = estimator.time_propagation_update()
#         #print z_bar
#         F_t, W_t = estimator.time_linearization()
#         sigma_bar = estimator.covariance_update()
#         h_z = estimator.get_observation_model()
#         H_t = estimator.observation_linearization()
#         #print h_z
#         k_gain = estimator.kalman_gain_value()
#         error = estimator.error_calculation(car_sensor_readout[k])
#         z_hat = np.array([estimator.conditional_mean()])
#         z_hat_list = np.concatenate((z_hat_list, z_hat), axis = 0)
#         sigma_hat = estimator.observation_update_covariance()
#         k = k + 1
#     #print car_sensor_readout
#     #print car_state
#     z_hat_final = z_hat_list[1:]
#     # print(car_state)
#     # print(z_hat_final)
