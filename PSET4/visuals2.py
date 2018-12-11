#!/usr/bin/env python
# depending on the python distribution release this might error
'''Module containing all graphical objects and supporting functions.'''

__author__ = 'Alexie Pogue'

# libraries
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib as mpl
import numpy as np
import copy
import os

# path where images are stored
IMAGE_PATH = './images'


class parkingLot(object):
    '''Graphics object to animate algorithms'''

    def __init__(self, title, lot_size, possible_goal_states):
        '''Constructor

        Arguments:
            title - string: title that is shown on top of grid
            trajectory - the path the car needs to follow
            possible_goal_states - desired destination
         '''


        self.trajectory = 0


        # plot out rewards
        fig, ax = plt.subplots()

        # set title and x/y labels
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()

        # turn off all the ticks marks
        ax = plt.gca()
        for t in ax.xaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False
        for t in ax.yaxis.get_major_ticks():
            t.tick1On = False
            t.tick2On = False

        # all goal states have the same x and y so choose the first one for display
        goal_state = next(iter(possible_goal_states))

        # plot a star at the goal state x, y
        plt.plot(goal_state[0] + 0.5, goal_state[1] + 0.5, marker='*', color='k', markersize=10)


        # save the figure, axes, and possible goal states for use in other methods
        self.fig = fig
        self.ax = ax
        self.possible_goal_states = possible_goal_states

        # reset the starting point
        self.start_marker = None




    def plotTrajectoryGradient(self):
        '''Plots the state trajectory with gradient colors to show time progression'''

        points = np.array([self.trajectory[:,0], self.trajectory[:,1]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Create a continuous norm to map from data points to colors

        norm = plt.Normalize(self.trajectory[:,0].min(), self.trajectory[:,0].max())
        lc = LineCollection(segments, cmap='viridis', norm=norm)
        # Set the values used for colormapping
        lc.set_array(self.trajectory[:,0])
        lc.set_linewidth(1.5)
        lc.set_linestyle('--')

        self.ax.add_collection(lc)
        self.ax.set_xlim(self.trajectory[:,0].min(), self.trajectory[:,0].max()+10)
        self.ax.set_ylim(self.trajectory[:,1].min(), self.trajectory[:,1].max()+10)



        plt.show()





if __name__ == '__main__':

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















