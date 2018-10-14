
import numpy as np

# Alexie Pogue PSET 2





class S:  # still confused about the circumstances under which I need a class rather than a function

    def __init__(self, grid_x=6, grid_y=6):
        x_count = range(grid_x)
        y_count = range(grid_y)
        h_count = range(12)
        self.state = [(x, y, h) for x in x_count for y in y_count for h in h_count] # this is a list of tuples

    # def state(self):
    #     return self.state


class A:
    def __init__(self): # maybe you tell it which state you want to be in, then it will output something
        trans = ['forwards', 'backwards', 'none']
        rot = ['right', 'left']

    # def action(self):
    #     return self.trans, self.rot

epsilon = 1e-12
def Psa(Pe, S, a, Sp): # you need to add the situation if you are at the border blocks/ take any unnecessary loops out of the functions


    move = Sp[:2] - S[:2]  # move from state to probable state
    hS = S[2]  # heading of state
    hSp = Sp[2]  # heading of probable state
    clockAngle = np.arange(5 * np.pi / 2, 2 * np.pi / 3, -2 * np.pi / 12)  # heading angles
    spinArray = np.array([[np.cos(i), np.sin(i)] for i in clockAngle])  # heading vectors 2D
    north = np.array([0, 1])
    south = np.array([0, -1])
    east = np.array([1, 0])
    west = np.array([-1, 0])
    none = np.array([0, 0])
    hAngle = np.zeros((12,1))

    cardDirec = [north, south, east, west, none]
    # for i, v in enumerate(spinArray):  # you should take this out and put it somewhere else
    #     if i < 6:
    #         hAngle[i] = np.arccos(np.dot(north, v))
    #     else:
    #         hAngle[i] = 2*np.pi - np.arccos(np.dot(north, v))

    for i in cardDirec:  # how do i make this a while loop, look for a better way to do this
        if np.allclose(move, i):
            break
    due = i

    if np.allclose(due, none):
        tcommand = 'none'
    else:
        if np.arccos(np.dot(due, spinArray[hS])) <= np.pi / 6 + epsilon:
            tcommand = 'forwards'
        elif np.arccos(np.dot(due, spinArray[hS])) >= 5*np.pi / 6 - epsilon:
            tcommand = 'backwards'
        else:
            tcommand = 'error'

    if hSp == (hS-1)%12:
        rcommand = 'left'
    elif hSp == (hS+1)%12:
        rcommand = 'right'
    else:
        rcommand = 'error'

    command = [tcommand, rcommand]

    if command == a:
        return 1 - 2 * Pe
    else:
        return Pe


def trans(Pe, S, a):
    grid_x = 6
    grid_y = 6
    state = S[:2]
    hS    = S[2]
    clockAngle = np.arange(5 * np.pi / 2, 2 * np.pi / 3, -2 * np.pi / 12)  # heading angles
    spinArray = np.array([[np.cos(i), np.sin(i)] for i in clockAngle])  # heading vectors 2D, now it is a list for indexing
    z = np.array([0, 0, 1])  # rotation axis points up
    heading = range(12)
    north = np.array([0, 1])
    south = np.array([0, -1])
    east = np.array([1, 0])
    west = np.array([-1, 0])
    none = np.array([0, 0])
    cardDirec = [north, south, east, west, none]
    cAng = 2*np.pi/12
    Rpos = np.array([[np.cos(cAng), -np.sin(cAng)], [np.sin(cAng), np.cos(cAng)]])
    Rneg = np.array([[np.cos(-cAng), -np.sin(-cAng)], [np.sin(-cAng), np.cos(-cAng)]])
    if a[0] == 'none':
        Sp = S
        return Sp
    else:
        hposS = np.array([(hS - 1) % 12])
        hnegS = np.array([(hS+1) % 12])
        sampleSet = [hS, hposS, hnegS]
        probDist = [1-2*Pe, Pe, Pe]
        sample = np.random.choice(3, 1, replace=True, p=probDist) # choose replacement in case you want to sample more times
        hSp = np.array(sampleSet[np.asscalar(sample)])
        for v in cardDirec:  # how do i make this a while loop, look for a better way to do this
            if np.arccos(np.dot(v, spinArray[np.asscalar(hSp)])) <= np.pi/6 + epsilon:
                break
        facing = v
        if a[0] == 'forwards':
            Spp = state + facing
        else:
            Spp = state - facing
        if Spp[0] > grid_x or Spp[0] < 0 or Spp[1] > grid_y or Spp[1] < 0:
            Spp = state
        hSpnew = hSp
        if a.__len__() == 2:
            if a[1] == 'left':
                hSpnew = np.array([(np.asscalar(hSp) - 1)%12])
            else:
                hSpnew = np.array([(np.asscalar(hSp) + 1)%12])
        Sp = np.concatenate((Spp, hSpnew), axis=0)
        return Sp, hSp, facing




W = 6
L = 6


R = {}

xcount = range(W)
ycount = range(L)
hcount = range(2)
states = [(x, y, h) for x in xcount for y in ycount for h in hcount]

for h in states:
    if h[0] == 0 or h[0] == W or h[1] == 0 or h[1] == L:
        reward = -100
    elif h[1] in range(2,5):
        if h[0] == 2:
            reward = -1
        elif h[0] == 4:
            reward = -1
    elif h[0:2] == (3,4):
        reward = 1
    else:
        reward = 0
    R[h] = reward














# Main Function
if __name__ == '__main__':
    Pe = 0.5
    S = np.array([2, 2, 9])  # I could prerotate to 2 from 1, then tell my robot to go right and end up at 3
    Sp = np.array([2, 2, 0])
    a = ['none']
    print Psa(Pe, S, a, Sp)
    print trans(Pe, S, a)