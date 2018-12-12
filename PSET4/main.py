
from PSET4.visuals2 import visualEnvironment
from PSET4.collision_detection import myCar
from PSET4.collision_detection import Obstacle
from PSET4.collision_detection import parkingLot
import numpy as np



'''Environment containing the car and the obstacles'''

# create the parking lot instance
lot = parkingLot(500, 700)
# vertices for plotting
lot_plot_info = lot.lot_plot_info()

# instantiate the car (length, width)
car = myCar(80, 85)
# car point on wheel axle
car.p_xy = np.array([350, 350, 1])
# car heading angle, velocity and angular velocity
car.heading = 0 * np.pi / 180
car.vel = 1
car.ang_vel = 1

# car target
h_count = np.arange(60) * np.pi / 180
possible_goal_states = set((350, 350, h) for h in h_count)

# mock car trajectory
state_vector = np.zeros((350, 3))
state_vector[:, 0] = np.arange(0, 350)
state_vector[:, 1] = np.arange(0, 350)
state_vector[:, 2] = np.arange(350) * np.pi / 180

# instantiate the obstacles
# arguments are the bottom left corner in frame A, length, width, orientation
obstacle1 = Obstacle(np.array([100, 100, 1]), 100, 100, 10*np.pi/180)
obstacle2 = Obstacle(np.array([0, 0, 1]), 100, 50, 10*np.pi/180)
# obstacle vertices for plotting
obstacle1_plot_info = obstacle1.obstacle_plot_info()
obstacle2_plot_info = obstacle2.obstacle_plot_info()
# stack the vertices information
obstacle_plot_info = np.vstack(([obstacle1_plot_info], [obstacle2_plot_info]))
# color the obstacles
face_color = ((0, 0, 0, 1), (0, 1, 1, 1))

# plot everything to debug
# instantiate the environment
visual = visualEnvironment('Collision Stuff', lot_plot_info, possible_goal_states)

# plot the obstacles
visual.plotObstacle(obstacle_plot_info, face_color)

# plot the car trajectory
visual.trajectory = state_vector
visual.plotTrajectoryGradient()
visual.plotCar(car.p_xy, [car.car_plot_info()])


# check the collision detector is working
car.check_obstacle_collision(obstacle1.obstacle_dictionary())
car.check_obstacle_collision(obstacle2.obstacle_dictionary())
car.check_boarder_collision(lot.lot_dictionary())









