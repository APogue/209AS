#!/usr/bin/env python
# depending on the python distribution release this might error
'''Module containing all graphical objects and supporting functions.'''

__author__ = 'Alexie Pogue'

# libraries
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import copy
import os


# path where images are stored
IMAGE_PATH = './images'




class parkingLot(object):
    '''Graphics object to animate algorithms'''

    def __init__(self, title, lot_matrix, possible_goal_states):
        '''Constructor

        Arguments:
            title - string: title that is shown on top of grid
         '''


        # to show a gradient trajectory, choose blue and pink
        self.TRAJECTORY_START_COLOR = np.array([50, 38, 229])/255.0
        self.TRAJECTORY_END_COLOR = np.array([229, 9, 222])/255.0

        # constant for defining delay between frames
        self.PAUSE_DELAY = 0.05

        # determines cap on simulation states
        self.MAX_STATE_NUMBER = 30

        # constants for defining heading arrow properties
        self.ARROW_LENGTH = 0.1
        self.ARROW_WIDTH = 0.05

        # assign x and y ticks on the grid
        x_axis_size = int(lot_matrix.shape[0]/10)
        y_axis_size = int(lot_matrix.shape[1]/10)
        xticklabels = range(0, x_axis_size) # could be text
        yticklabels = range(0, y_axis_size) # could be text   

        # create a color map to match problem statement
        # Note: currently only supports 4 reward values. Move to a transition color map for more.
        cmap = mpl.colors.ListedColormap(['yellow', 'white'])
        cmap.set_over('green')
        cmap.set_under('red')

        # create discrete bounds to divide the values
        # bounds = np.unique(lot_matrix)[:-1] + 0.5
        # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        # needed to automatically update plot
        plt.ion()

        # plot out rewards
        fig, ax = plt.subplots()    
        c = ax.pcolor(lot_matrix, edgecolors='k', linestyle= 'dashed',
                         linewidths=0.2, cmap=cmap, norm=norm)

        # put the major ticks at the middle of each cell
        ax.set_yticks(np.arange(lot_matrix.shape[0]) + 0.5, minor=False)
        ax.set_xticks(np.arange(lot_matrix.shape[1]) + 0.5, minor=False)

        # set tick labels
        ax.set_xticklabels(xticklabels, minor=False)
        ax.set_yticklabels(yticklabels, minor=False)

        # set title and x/y labels
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')      

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
        plt.plot(goal_state.x+0.5, goal_state.y+0.5, marker='*', color='k', markersize=10)
        
        # save the figure, axes, and possible goal states for use in other methods
        self.fig = fig
        self.ax = ax
        self.possible_goal_states = possible_goal_states

        # reset the starting point
        self.start_marker = None

        # resets key instance variables 
        self.resetVariables()

        # since interactive plotting is on, need to pause in order to see the initial plot
        plt.pause(self.PAUSE_DELAY)


    def resetVariables(self):
        '''Resets all instance variables to default values'''

        # clear objects from plot
        if self.start_marker is not None:
            self.start_marker.remove()
            self.state_arrow.remove()
            self.trajectory_line.remove()
            self.value_line.remove()

            for arrow in self.trajectory_arrows:
                arrow.remove()
        
        # reset graphics objects
        self.state_arrow = None
        self.trajectory_line = None
        self.start_marker = None
        self.trajectory_arrows = []
        self.value_line = None
        
        # reset internal variables
        self.state_number = -1
        self.trajectory_x = []
        self.trajectory_y = []
        self.trajectory = []
        self.trajectory_values = []

    def setStartState(self, start_state):
        '''Plot and initialize the starting state

        Arguments:
            start_state - state: state defined in common.py to denote the starting point
        '''

        # update the state to the start state.
        # Note: moved all start state code to updateState() and only to keep interfaces
        self.updateState(start_state)


    def updateState(self,s):
        '''Update plot to a new state and plot trajectory
        
        Arguments:
            s - state: state defined in common.py to denote the current state
        '''

        # change to the grid world figure
        plt.figure(self.fig.number)

        # add points of the trajectory
        self.trajectory_x.append(s.x+0.5)
        self.trajectory_y.append(s.y+0.5)
        self.trajectory.append(s)

        # check if the starting state has been specified already
        if self.start_marker is None:
            # plot a marker to denote the starting state
            self.start_marker, =  plt.plot(s.x+0.5, s.y+0.5, marker='.', color='k', markersize=10)

            # plot trajectory from the previous state to this state
            self.trajectory_line, = plt.plot(self.trajectory_x, self.trajectory_y, 'k--')    
        else:
            # since arrow updates aren't built in to matplotlib, delete arrow to recreate later
            self.state_arrow.remove()

            # update trajectory with new values
            self.trajectory_line.set_data(self.trajectory_x, self.trajectory_y)

        # calculate the change in x and y to show heading with the arrow object
        dx = self.ARROW_LENGTH*np.cos(s.heading)
        dy = self.ARROW_LENGTH*np.sin(s.heading)

        # create a new arrow pointing in the correct heading
        # Note: store arrow to destroy and recreate later
        self.state_arrow = self.ax.arrow(s.x+0.5, s.y+0.5, dx, dy, width=self.ARROW_WIDTH, edgecolor='k')

        # pause to see the plot update
        plt.pause(self.PAUSE_DELAY)

        # save the current state for future calculations
        self.state = s
        self.state_number += 1



    def runSimulation(self, getNewState, policy, value, start_state, image_base_name=None, image_format='.pdf'):
        '''Given a system, policy, and starting state, animates the simulation to the end

        Arguments:
            getNewState - function: this function describes how a new state is found in the system
            policy - dict of actions: the given policy must have actions that lead to the goal
            value - dict of floats: the value function for the specified policy
            start_state - state: state defined in common.py to denote the start point
            image_base_name - string: the base string that all images of the simulation will have. 
                The script will only save images if a base name is given.
            image_format - string: format of the saved images
        '''

        # reset instance variables
        self.resetVariables()

        # change the current state
        current_state = start_state

        # update plot with the starting state
        self.updateState(current_state)
        if image_base_name is not None:
            image_name = image_base_name + 'Start'
            self.saveFigure(self.fig, image_name, image_format)

        # run simulation while the current state is not the goal state
        # TODO: should there also be a condition for bad policies that will never find a way?
        while not (current_state in self.possible_goal_states) and self.state_number < self.MAX_STATE_NUMBER:
            # get the current action and find a new state based on the system
            current_action = policy[current_state]
            new_state = getNewState(current_state, current_action)

            # update plots with the new state
            self.updateState(new_state)

            # only save image in name is specified
            if image_base_name is not None:
                image_name = image_base_name + str(self.state_number)
                self.saveFigure(self.fig, image_name, image_format)

            # update current state
            current_state = new_state

        # plot a the trajectory as a color gradient
        self.plotTrajectoryGradient()

        # increment state number to allow saving a new figure
        if image_base_name is not None:
            image_name = image_base_name + 'End'
            self.saveFigure(self.fig, image_name, image_format)
            image_name = image_base_name + 'Value'
            self.saveFigure(self.value_fig, image_name, image_format)


    def plotTrajectoryGradient(self):
        '''Plots the state trajectory with gradient colors to show time progression'''

        # total number of states in the trajectory is the current state number
        num_trajectory_states = len(self.trajectory)

        # linearly interpolate all color channels by the number of states
        red = np.linspace(self.TRAJECTORY_START_COLOR[0],self.TRAJECTORY_END_COLOR[0],num_trajectory_states);
        green = np.linspace(self.TRAJECTORY_START_COLOR[1],self.TRAJECTORY_END_COLOR[1],num_trajectory_states);
        blue = np.linspace(self.TRAJECTORY_START_COLOR[2],self.TRAJECTORY_END_COLOR[2],num_trajectory_states);
        
        # create a gradient color set
        gradient_color_set = np.array([red, green, blue]) 

        # plot an arrow 
        for k in range(num_trajectory_states):
            # pull state from trajectory
            s = self.trajectory[k]

            # calculate the change in x and y to show heading with the arrow object
            dx = 0.3*np.cos(s.heading)
            dy = 0.3*np.sin(s.heading)

            # plot an arrow denoting part of the trajectory
            self.trajectory_arrows.append(self.ax.arrow(s.x+0.5, s.y+0.5, dx, dy, width=self.ARROW_WIDTH, 
                facecolor=(gradient_color_set[:,k]), edgeColor=(gradient_color_set[:,k])))


    def saveFigure(self, fig, image_name, image_format):
        '''Modified saving to allow for filename and format specific names

        Arguments:
            fig - matplotlib figure: denotes which figure to save
            image_name - string: full path of the image name to save as
            image_format - string: type of image to save
        '''

        filename = os.path.join(IMAGE_PATH,image_name+image_format)
        fig.savefig(filename)


