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



state = (1, 4, 6)
trajectory = [state]

while state not in possible_goal_states:
    actionMatrix = example.policy_matrix()
    action = actionMatrix[state]
    transition = example.transition_function(0, state, action)
    state = tuple(transition)
    trajectory.append(state)
    grid_world.updateState(state)
    #grid_world.updateValue(state)
grid_world.plotTrajectoryGradient()
grid_world.saveFigure('trajectory', 'Initial Policy \pi_0', '.pdf')
#grid_world.saveFigure('value', 'someValue', '.pdf')

print trajectory

# grid_world.saveFigure('trajectory', 'someName', '.pdf')
# grid_world.saveFigure('value', 'someValue', '.pdf')

raw_input('Press Enter when finished')