
import numpy as np

# Alexie Pogue PSET 2


class S:  # still confused about the circumstances under which I need a class rather than a function

    def __init__(self, grid_x=6, grid_y=6):
        x_count = range(grid_x)
        y_count = range(grid_y)
        h_count = range(12)
        self.state = np.array([[x, y, h] for x in x_count for y in y_count for h in h_count]) # this is a list of tuples

    # def state(self):
    #     return self.state


class A:
    def __init__(self): # maybe you tell it which state you want to be in, then it will output something
        trans = ['forwards', 'backwards', 'none']
        rot = ['right', 'left']

    # def action(self):
    #     return self.trans, self.rot


def Psa(Pe, S, a, Sp): # you need to add the situation if you are at the border blocks

    move = Sp[:2] - S[:2]  # move from state to probable state
    hS = S[2]  # heading of state
    hSp = Sp[2]  # heading of probable state
    clockAngle = np.arange(5 * np.pi / 2, 2 * np.pi / 3, -2 * np.pi / 12)  # heading angles
    spinArray = np.array([[np.cos(i), np.sin(i)] for i in clockAngle])  # heading vectors 2D
    z = np.array([0, 0, 1])  # rotation axis points up
    north = np.array([0, 1])
    south = np.array([0, -1])
    east = np.array([1, 0])
    west = np.array([-1, 0])
    none = np.array([0, 0])
    cardDirec = [north, south, east, west, none]

    for i in cardDirec:  # how do i make this a while loop, look for a better way to do this
        if np.allclose(move, i):
            break
    due = i

    if np.allclose(due, none):
        tcommand = 'none'
    else:
        if np.arccos(np.dot(due, spinArray[hS])) <= np.pi / 6 + 1e-8:
            tcommand = 'forwards'
        elif np.arccos(np.dot(due, spinArray[hS])) >= 5*np.pi / 6 - 1e-8:
            tcommand = 'backwards'
        else:
            tcommand = 'error'

    hzS = np.concatenate((spinArray[hS], np.zeros(1)), axis=0)
    hzpS = np.concatenate((spinArray[hSp], np.zeros(1)), axis=0)
    rot = np.arccos(np.dot(hzS, hzpS))

    if -2e-8 < rot < 2e-8:
        rotAngle = 0
    else:
        angle1 = np.cross(hzS, hzpS)
        angle2 = angle1 / np.linalg.norm(angle1)
        angle3 = np.dot(angle2, z)
        rotAngle = angle3 * rot

    if rotAngle == 0:
        command = [tcommand]
    else:
        if np.absolute(rotAngle + np.pi/6) < 1e-8:
            rcommand = 'right'  # CW
        elif np.absolute(rotAngle - np.pi / 6) < 1e-8:
            rcommand = 'left'  # CCW
        else:
            rcommand = 'error'
        command = [tcommand, rcommand]

    if command == a:
        return 1 - 2 * Pe
    else:
        return Pe


def trans(Pe, S, a):
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
    if a == 'none':
        Sp = S
        return Sp
    else:
        hposS = np.array([heading[(hS+1)%12]])
        hnegS = np.array([heading[(hS-1)%12]])
        posS   = np.concatenate((state, hposS), axis=0)
        negS   = np.concatenate((state, hnegS), axis=0)
        sampleSet = [S, posS, negS]
        probDist = [1-2*Pe, Pe, Pe]
        sample = np.random.choice(3, 1, replace=True, p=probDist) # choose replacement in case you want to sample more times
        Spp = sampleSet[np.asscalar(sample)]
        return Spp  # this is the possibly prerotated state

    # if a == ['forwards']:
    #
    # if a == ['forwards','right']:
    # if a == ['forwards','left']:
    # if a == ['backwards']:
    # if a == ['backwards','right']:
    # if a == ['backwards', 'left']:








# Main Function
if __name__ == '__main__':
    Pe = .1
    S = np.array([2, 1, 0])  # I could prerotate to 2 from 1, then tell my robot to go right and end up at 3
    Sp = np.array([1, 1, 3])
    a = ['backwards', 'right']
    print Psa(Pe, S, a, Sp)
    print trans(Pe, S, a)