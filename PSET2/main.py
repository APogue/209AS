import numpy as np
from visuals import gridWorld
from pset2 import gridWorlds
import time

'''Creates trajectories and plots, also determines values for a trajectory'''

# Pe is the probability for error
Pe = 0

# to only have the heading point downwards in the goal state, input 'not all'
# this will not work with the initial policy, I didn't design it with that capability

# may be an error due to python interpreter versions, need to quick fix using if statements
case = 'policy iteration' # initial policy, policy iteration, or other

example = gridWorlds(6, 6, 12, Pe, 'all')

possible_goal_states = example.goal('all')

# make reward matrix
REWARD_MATRIX = np.zeros((6, 6))
REWARD_MATRIX[:, 0] = -100
REWARD_MATRIX[:, -1] = -100
REWARD_MATRIX[0, :] = -100
REWARD_MATRIX[-1, :] = -100
REWARD_MATRIX[3:5, 3] = -10
REWARD_MATRIX[2:5, 4] = 0
REWARD_MATRIX[4, 4] = 1

# create grid world object
grid_world = gridWorld('6x6 grid', REWARD_MATRIX, possible_goal_states)

if case == 'initial policy':
    # generate and plot a trajectory, initial policy
    state = (1, 4, 6)
    trajectory = [state]
    actionMatrix = example.policy_matrix()
    valuePi0 = example.policy_evaluation(actionMatrix)
    value = valuePi0[1][4][6]
    trajectory_value = [value]
    grid_world.updateState(state)
    grid_world.updateValue(value)
    while state not in possible_goal_states:
        action = actionMatrix[state]
        transition = example.transition_function(Pe, state, action) # with Pe = 0, it should get there in min moves
        state = tuple(transition)
        grid_world.updateState(state)
        trajectory.append(state)
        x = state[0]
        y = state[1]
        h = state[2]
        value = valuePi0[x][y][h]
        grid_world.updateValue(value)
        trajectory_value.append(value)
    grid_world.plotTrajectoryGradient()
    grid_world.saveFigure(grid_world.fig, 'Initial Policy Trajectory', '.pdf')
    grid_world.saveFigure(grid_world.value_fig, 'Iniital Policy Value', '.pdf')
    print trajectory
    print trajectory_value

elif case == 'policy iteration':
    # generate and plot a trajectory, policy iteration
    # value0 = np.zeros([example.L, example.W, example.h, 1])
    begin = time.time()
    state = (1, 4, 6)
    trajectory = [state]
    actionMatrix0 = example.policy_matrix()
    optPolicyMatrix, value0 = example.policy_iteration(actionMatrix0)
    valuePiStar = example.policy_evaluation(optPolicyMatrix, value0)
    value = valuePiStar[1][4][6]
    trajectory_value = [value]
    grid_world.updateState(state)
    grid_world.updateValue(value)
    while state not in possible_goal_states:
        prev_value = value
        action = optPolicyMatrix[state]
        transition = example.transition_function(Pe, state, action)
        state = tuple(transition)
        grid_world.updateState(state)
        trajectory.append(state)
        x = state[0]
        y = state[1]
        h = state[2]
        value = valuePiStar[x][y][h]
        grid_world.updateValue(value)
        trajectory_value.append(value)
        # if prev_value == value:
        #     break
    grid_world.plotTrajectoryGradient()
    grid_world.saveFigure(grid_world.fig, 'PolicyIterationTrajectoryPe1', '.pdf')
    grid_world.saveFigure(grid_world.value_fig, 'PolicyIterationValuePe1', '.pdf')
    end = time.time()
    print trajectory
    print trajectory_value
    print 'policy iteration timer', end-begin

else:
    # generate and plot a trajectory, value iteration
    begin = time.time()
    state = (1, 4, 6)
    trajectory = [state]
    optPolicyMatrix, valuePiStar = example.value_iteration()
    value = valuePiStar[1][4][6]
    trajectory_value = [value]
    grid_world.updateState(state)
    grid_world.updateValue(value)
    while state not in possible_goal_states:
        prev_value = value
        action = optPolicyMatrix[state]
        transition = example.transition_function(Pe, state, action)
        state = tuple(transition)
        grid_world.updateState(state)
        trajectory.append(state)
        x = state[0]
        y = state[1]
        h = state[2]
        value = valuePiStar[x][y][h]
        grid_world.updateValue(value)
        trajectory_value.append(value)
        # if prev_value == value:
        #     break
    grid_world.plotTrajectoryGradient()
    grid_world.saveFigure(grid_world.fig, 'ValueIterationTrajectoryPe1b', '.pdf')
    grid_world.saveFigure(grid_world.value_fig, 'ValueIterationValuePe1b', '.pdf')
    end = time.time()
    print trajectory
    print trajectory_value
    print 'value iteration timer', end - begin

raw_input('Press Enter when finished')
