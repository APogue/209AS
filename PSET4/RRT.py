from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import math
import copy
import numpy as np
from PSET4.collision_detection import myCar
from PSET4.collision_detection import Obstacle
from PSET4.collision_detection import parkingLot
import numpy as np

from PSET4.visuals2 import visualEnvironment

show_animation = True

class RRT():

    """
    Class for RRT Planning
    """

    def __init__(self, car, lot_dict, instanceList, obstacle_plot_info, lot_plot_info, bla1, \
            bla2, bla3, start, goal, randArea, expandDis=10.0, goalSampleRate=5, maxIter=100):
        """
        Setting Parameter

        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]

        """
        self.start = Node(start[0], start[1], start[2]) # not going to take orientation into account, the robot will point in the direction of the path
        self.end = Node(goal[0], goal[1], goal[2])
        self.minrand = randArea[0] # this is the parking lot size
        self.maxrand1 = randArea[1]
        self.maxrand2 = 700
        self.expandDis = expandDis
        self.goalSampleRate = goalSampleRate
        self.maxIter = maxIter
        self.car = car
        self.lot_dict = lot_dict
        self.instanceList = instanceList
        self.obstacle_plot_info = obstacle_plot_info
        self.lot_plot_info = lot_plot_info
        self.obsdict1 = bla1
        self.obsdict2 = bla2
        self.obsdict3 = bla3




    def Planning(self, animation=True):
        """
        Pathplanning

        animation: flag for animation on or off
        """
        p = 0
        self.nodeList = [self.start]
        while True:
            # Random Sampling
            if random.randint(0, 100) > self.goalSampleRate: # this periodically changes the node to qG
                rnd = [random.uniform(self.minrand, self.maxrand1), random.uniform(
                    self.minrand, self.maxrand2)]
            else:
                rnd = [self.end.x, self.end.y, self.end.theta]

            # Find nearest node
            nind = self.GetNearestListIndex(self.nodeList, rnd)
            # print(nind)

            # expand tree
            nearestNode = self.nodeList[nind]
            theta = math.atan2(rnd[1] - nearestNode.y, rnd[0] - nearestNode.x)

            newNode = copy.deepcopy(nearestNode)
            newNode.x += self.expandDis * math.cos(theta)
            newNode.y += self.expandDis * math.sin(theta)
            newNode.theta = theta
            newNode.parent = nind

            #update car position and check for collision

            k = 50
            nodeSet_x = np.linspace(nearestNode.x, newNode.x, num = k)
            nodeSet_y = np.linspace(nearestNode.y, newNode.y, num = k)
            #nodeSet_pxy = np.hstack((nodeSet_x,nodeSet_y))
            nodeSet_pxy = [np.array([nodeSet_x[i],nodeSet_y[i],1]) for i in range(k)]

            #nodeSet_pxy = [np.array([10,100, 0]), np.array([4,5,0])]
            #print(nodeSet_pxy)


            v = 1
            for N in range(20):
                self.car.p_xy = np.array(nodeSet_pxy[N])
                self.car.heading = newNode.theta
                if self.car.check_collision():
                    v = 0
            print(v)
            if v == 0:
                continue
            print(v)

            # if collisionCheck(nodeSet_pxy):
            #     continue


            self.nodeList.append(newNode)
            #print("nNodelist:", len(self.nodeList))

            # check goal
            dx = newNode.x - self.end.x
            dy = newNode.y - self.end.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= self.expandDis:
                print("Goal!!")
                break
            if animation:
                self.DrawGraph(rnd)



        path = [[self.end.x, self.end.y, self.end.theta]]
        lastIndex = len(self.nodeList) - 1
        while self.nodeList[lastIndex].parent is not None:
            node = self.nodeList[lastIndex]
            path.append([node.x, node.y])
            lastIndex = node.parent
        path.append([self.start.x, self.start.y])

        return path

    def GetNearestListIndex(self, nodeList, rnd):
        dlist = [(node.x - rnd[0]) ** 2 + (node.y - rnd[1])
                 ** 2 for node in nodeList]
        minind = dlist.index(min(dlist))
        return minind


    def DrawGraph(self, rnd=None):
        """
        Draw Graph
        """
        # plt.clf()
        # if rnd is not None:
        #     plt.plot(rnd[0], rnd[1], "^k")
        # ax, fig = plt.subplots()
        for node in self.nodeList:
            if node.parent is not None:
                plt.plot([node.x, self.nodeList[node.parent].x], [
                         node.y, self.nodeList[node.parent].y], "-g")

        plt.plot(self.start.x, self.start.y, "xr")
        plt.plot(self.end.x, self.end.y, "xr")
        plt.axis([-20, 520, -20, 720])
        plt.gca().set_aspect('equal', adjustable='box')
        #plt.grid(True)
        plt.pause(0.01)
        plt.savefig('decreasenoisezohfactor50.pdf')



class Node():
    """
    RRT Node
    """

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.parent = None



def main():
    print("start simple RRT path planning")

    # ====Search Path with RRT====
    # instantiate the car (length, width)
    car = myCar(80, 85, 0)
    # car point on wheel axle
    car.p_xy = np.array([50, 50, 1])
    # car heading angle, velocity and angular velocity
    car.vel = 1
    car.ang_vel = 1

    # create the parking lot instance
    lot = parkingLot(500, 700)
    lot_dict = lot.lot_dictionary()
    lot_plot_info = lot.lot_plot_info()


    # create the parking lot instance
    lot = parkingLot(500, 700)
    lot_dict = lot.lot_dictionary()
    lot_plot_info = lot.lot_plot_info()

    obstacle1 = Obstacle(np.array([400, 200, 1]), 50, 100, np.pi / 3)
    obstacle2 = Obstacle(np.array([200, 200, 1]), 50, 50, 0 * np.pi / 3)
    obstacle3 = Obstacle(np.array([10, 100, 1]), 60, 30, -np.pi / 3)

    instancelist = [obstacle1.obstacle_dictionary(), obstacle2.obstacle_dictionary(),
                    obstacle3.obstacle_dictionary()]
    bla1 = obstacle1.obstacle_dictionary()
    bla2 = obstacle2.obstacle_dictionary()
    bla3 = obstacle3.obstacle_dictionary()
    # obstacle vertices for plotting
    obstacle1_plot_info = obstacle1.obstacle_plot_info()
    obstacle2_plot_info = obstacle2.obstacle_plot_info()
    obstacle3_plot_info = obstacle3.obstacle_plot_info()
    # stack the vertices information
    obstacle_plot_info = np.vstack(([obstacle1_plot_info], [obstacle2_plot_info],
                                    [obstacle2_plot_info]))
    # color the obstacles
    face_color = ((0, 0, 0, 1), (0, 1, 1, 1), (0, 1, 1, 1))

    rrt = RRT(car, lot_dict, instancelist, obstacle_plot_info, bla1, bla2,
              bla3, lot_plot_info, start=[100, 100, 0], goal=[150, 580, 0], randArea=[450, 450])

    '''Environment containing the car and the obstacles'''

    # car target
    h_count = np.arange(60) * np.pi / 180
    possible_goal_states = set((350, 580, h) for h in h_count)
    visual = visualEnvironment('RRT Algorithm', lot_plot_info, possible_goal_states)

    # plot the obstacles
    visual.plotObstacle(obstacle_plot_info, face_color)

    # plot the car trajectory
    visual.trajectory = rrt.Planning(animation=show_animation)
    # visual.plotTrajectoryGradient()
    # visual.plotCar(car.p_xy, [car.car_plot_info()])








if __name__ == '__main__':
    main()
