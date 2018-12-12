from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy
import numpy as np
from PSET4.collision_detection import myCar
from PSET4.collision_detection import Obstacle
from PSET4.collision_detection import parkingLot
import numpy as np



# to bring the RRT path to Goal:

# coin toss to periodically connect alphai to qG. 99/100 times connect to nearest neighbor, 1/100 times try to connect
# it to qG

# collision checking:

# lavalle 5.3.4 checking a path segment- sample the path interval to determine whether it is in collision
# efficient checking first check T(1), T(0), T(1/2), T(1/4), T(3/4), T(1/8)... 5.2 Van der Corput

# to properly sample, the checker needs to determine the distance between the closest two points on obstacle
# and car, which would clear the path to the next sample

# that strategy is not taken here and would be considered future work

# proper nearest neighbor metric for Dubins or Reeds Shepp path is time-to-point, because the car can turn
# in place, (MR 13.3 pg 542) an ititial constraint-free path will be formed. This is then turned into a
# feasible path that respects motion contraints. First connect path from q(0) to q(1), if in collision,
# divide the path and connect q(0) to q(1/2) and q(1/2) to q(1), if either segment is in collision then
# divide that path and so on and so forth. Each point that must be added is a via point.



class RRT():
    """
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacleList, randArea, expandDis=1.0, goalSampleRate=5, maxIter=500):
        """
        Setting Parameter

        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:Ramdom Samping Area [min,max]

        """
        self.start = Node(start[0], start[1]) # not going to take orientation into account, the robot will point in the direction of the path
        self.end = Node(goal[0], goal[1])
        self.minrand = randArea[0] # this is the parking lot size
        self.maxrand = randArea[1]
        self.expandDis = expandDis
        self.goalSampleRate = goalSampleRate
        self.maxIter = maxIter
        self.obstacleList = obstacleList

    def Planning(self, animation=True):
        """
        Pathplanning

        animation: flag for animation on or off
        """

        self.nodeList = [self.start]
        while True:
            # Random Sampling
            if random.randint(0, 100) > self.goalSampleRate: # this periodically changes the node to qG
                rnd = [random.uniform(self.minrand, self.maxrand), random.uniform(
                    self.minrand, self.maxrand)]
            else:
                rnd = [self.end.x, self.end.y]

            # Find nearest node
            nind = self.GetNearestListIndex(self.nodeList, rnd)
            # print(nind)

            # expand tree
            nearestNode = self.nodeList[nind]
            theta = math.atan2(rnd[1] - nearestNode.y, rnd[0] - nearestNode.x)

            newNode = copy.deepcopy(nearestNode)
            newNode.x += self.expandDis * math.cos(theta)
            newNode.y += self.expandDis * math.sin(theta)
            newNode.parent = nind

            if not self.__CollisionCheck(newNode, self.obstacleList):
                continue

            self.nodeList.append(newNode)

            # check goal
            dx = newNode.x - self.end.x
            dy = newNode.y - self.end.y
            d = math.sqrt(dx * dx + dy * dy)
            if d <= self.expandDis:
                print("Goal!!")
                break

            if animation:
                self.DrawGraph(rnd)

        path = [[self.end.x, self.end.y]]
        lastIndex = len(self.nodeList) - 1
        while self.nodeList[lastIndex].parent is not None:
            node = self.nodeList[lastIndex]
            path.append([node.x, node.y])
            lastIndex = node.parent
        path.append([self.start.x, self.start.y])

        return path
