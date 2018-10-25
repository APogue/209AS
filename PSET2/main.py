import numpy as np
from visuals import gridWorld
from pset2 import gridWorlds


example = gridWorlds(6, 6, 12)

possible_goal_states = example.goal('all')

# make rewards matrix
REWARD_MATRIX = np.zeros((6, 6))
REWARD_MATRIX[:, 0] = -100
REWARD_MATRIX[:, -1] = -100
REWARD_MATRIX[0, :] = -100
REWARD_MATRIX[-1, :] = -100
REWARD_MATRIX[2:5, 2] = -10
REWARD_MATRIX[2:5, 4] = -10
REWARD_MATRIX[4, 3] = 1

# create grid world object
grid_world = gridWorld('6x6 grid', REWARD_MATRIX, possible_goal_states)

# generate and plot a trajectory
state = (1, 4, 6)
trajectory = [state]
actionMatrix = example.policy_matrix()
valuePi0 = example.policy_evaluation(actionMatrix)
trajectory_value = [valuePi0[1][4][6]]
while state not in possible_goal_states:
    x = state[0]
    y = state[1]
    h = state[2]
    action = actionMatrix[state]
    transition = example.transition_function(.25, state, action)
    state = tuple(transition)
    trajectory.append(state)
    grid_world.updateState(state)
    value = valuePi0[x][y][h]
    trajectory_value.append(value)
    grid_world.updateValue(value)
grid_world.plotTrajectoryGradient()
grid_world.saveFigure('trajectory', 'Initial Policy pe of pt25', '.pdf')
grid_world.saveFigure('value', 'Iniital Policy Value pe of pt25', '.pdf')
print trajectory
print trajectory_value







raw_input('Press Enter when finished')