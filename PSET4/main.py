
from PSET4.visuals2 import parkingLot
from PSET4.pset4 import myCar
from PSET4.pset4 import Obstacle
from PSET4.pset4 import parkingLot
import numpy as np



car = myCar(80, 85)
car.p_xy = np.array([0, 0, 1])
car.heading = 20 * np.pi / 180
car.vel = 1
car.ang_vel = 1
obstacle = Obstacle(car.p_xy, 100, 100, 0)
obstacle.obstacle_dictionary()
check = car.check_obstacle_collision(obstacle.obstacle_dictionary())
parking_lot = parkingLot(500, 700)
check2 = car.check_boarder_collision(parking_lot.lot_dictionary())
print(check, check2)

h_count = np.arange(60) * np.pi / 180

possible_goal_states = set((150, 250, h) for h in h_count)

# Lot Matrix
LOT_MATRIX = np.zeros((50, 70))

# generate and plot a trajectory, initial policy

state_vector = np.zeros((50, 3))

state_vector[:, 0] = np.arange(101, 151)
state_vector[:, 1] = np.arange(201, 251)
state_vector[:, 2] = np.arange(50) * np.pi / 180

# create environment
car = parkingLot('Collision Stuff', lot_size, possible_goal_states)

car.trajectory = state_vector

car.plotTrajectoryGradient()
