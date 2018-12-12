#!/usr/bin/env python
# depending on the python distribution release this might error
'''Module containing all graphical objects and supporting functions.'''

__author__ = 'Alexie Pogue'

# libraries
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
import numpy as np

# path where images are stored
IMAGE_PATH = './images'


class visualEnvironment(object):
    '''Graphics object to animate algorithms'''

    def __init__(self, title, lot_info, possible_goal_states):
        '''Constructor

        Arguments:
            title - string: title that is shown on top of grid
            trajectory - the path the car needs to follow
            possible_goal_states - desired destination
         '''

        self.lot_info = lot_info
        self.trajectory = 0


        # plot out rewards
        fig, ax = plt.subplots()

        # set title and x/y labels
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.grid()


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
        plt.plot(goal_state[0], goal_state[1], marker='*', color='k', markersize=7)

        # plot the parking lot
        parking_lot = Polygon(lot_info, fc=(1, 1, 1, 0.5), ec=(0, 0, 0, 1), lw=2)
        ax.add_artist(parking_lot)




        # save the figure, axes, and possible goal states for use in other methods
        self.fig = fig
        self.ax = ax
        self.possible_goal_states = possible_goal_states

        # reset the starting point
        self.start_marker = None

        self.ax.set_xlim(self.lot_info[:, 0].min() - 50, self.lot_info[:, 0].max()+50)
        self.ax.set_ylim(self.lot_info[:, 1].min() - 50, self.lot_info[:, 1].max()+50)


    def plotObstacle(self, obstacle_info, face_color):
        '''accepts stacked object vertices info for plotting '''

        V = 0
        for N in obstacle_info:
            obstacle = Polygon(N, fc=face_color[V], ec=(0, 0, 0, 1), lw=2)
            self.ax.add_artist(obstacle)
            V += 1

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

    def plotCar(self, p_xy, car_plot_info):
        '''Plots car along the state trajectory'''

        plt.plot(p_xy[0], p_xy[1], marker='.', color='k', markersize=7)
        for N in car_plot_info:
            car = Polygon(N, fc=(.5, 1, 0, 1), ec=(0, 0, 0, 1), lw=2)
            self.ax.add_artist(car)

        plt.show()












