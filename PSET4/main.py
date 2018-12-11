
from PSET4.visuals import parkingLot
import numpy as np


h_count = np.arange(60)*np.pi/180

possible_goal_states = set((150, 250, h) for h in h_count)

# Lot Matrix
LOT_MATRIX = np.zeros((500, 700))

# create environment
car = parkingLot('500x700 grid', LOT_MATRIX, possible_goal_states)

# generate and plot a trajectory, initial policy

state_vector = np.zeros((50, 3))

state_vector[:, 0] = np.arange(50)
state_vector[:, 1] = np.arange(50)
state_vector[:, 1] = np.arange(50)*np.pi/180


state = (100, 200, 0)
trajectory = [state]
car.updateState(state)

for i in state_vector:
    state = tuple(i)
    car.updateState(state)
    trajectory.append(state)

car.plotTrajectoryGradient()
car.saveFigure('trajectory', 'Initial Policy Trajectory', '.pdf')
car.saveFigure('value', 'Iniital Policy Value', '.pdf')
