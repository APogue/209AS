
import numpy as np

# Alexie Pogue PSET 2

W=6
L=6
x_count = range(W)
y_count = range(L)
h_count = range(12)
epsilon = 1e-12
north = np.array([0, 1])
south = np.array([0, -1])
east = np.array([1, 0])
west = np.array([-1, 0])
none = np.array([0, 0])
card_direc = [north, south, east, west, none]
clock_angle = np.arange(5 * np.pi / 2, 2 * np.pi / 3, -2 * np.pi / 12)  # heading angles
rot_array = np.array([[np.cos(i), np.sin(i)] for i in clock_angle])  # heading vectors 2D
S = np.array([[x, y, h] for x in x_count for y in y_count for h in h_count])

class A:
    def __init__(self): # maybe you tell it which state you want to be in, then it will output something
        trans = ['forwards', 'backwards', 'none']
        rot = ['right', 'left']


def heading_check(Pe, a, state_h, state_ph):
    correct = 1-2*Pe
    incorrect = Pe
    if a.__len__() == 2:
        if a[1] == 'left':
            if state_ph == (state_h - 1) % 12:
                return correct
            else:
                return incorrect
        if a[1] == 'right':
            if state_ph == (state_h + 1) % 12:
                return correct
            else:
                return incorrect
    else:
        if state_h == state_ph:
            return correct
        else:
            return incorrect


def Psa(Pe, S, a, Sp):
    correct = 1-2*Pe
    incorrect = Pe
    state = S[:2]
    state_p = Sp[:2]
    move = state_p - state  # move from state to probable state
    state_h = S[2]              # heading of state
    state_ph = Sp[2]           # heading of probable state

    for k in card_direc:          # change to while loop
        if np.allclose(move, k):
            break
    due = k
    if a[0] == 'none' and np.allclose(due, none):
        return correct
    elif a[0] == 'forwards':
        if np.allclose(state, state_p):
            if state[0] == 0 and state_h in range(8, 11):
                return heading_check(Pe, a, state_h, state_ph)
            elif state[0] == W - 1 and state_h in range(2, 5):
                return heading_check(Pe, a, state_h, state_ph)
            elif state[1] == 0 and state_h in range(5, 8):
                return heading_check(Pe, a, state_h, state_ph)
            elif state[1] == L-1 and state_h in np.arange(11, 14)%12:
                return heading_check(Pe, a, state_h, state_ph)
        elif np.arccos(np.dot(due, rot_array[state_h]))<= np.pi/6 + epsilon:
            return heading_check(Pe, a, state_h, state_ph)
    elif a[0] == 'backwards':
        if np.allclose(state, state_p):
            if state[0] == 0 and state_h in range(2, 5):
                return heading_check(Pe, a, state_h, state_ph)
            elif state[0] == W - 1 and state_h in range(8, 11):
                return heading_check(Pe, a, state_h, state_ph)
            elif state[1] == 0 and state_h in np.arange(11, 14)%12:
                return heading_check(Pe, a, state_h, state_ph)
            elif state[1] == L-1 and state_h in range(5, 8):
                return heading_check(Pe, a, state_h, state_ph)
        elif np.arccos(np.dot(due, rot_array[state_h])) >= 5*np.pi / 6 - epsilon:
            return heading_check(Pe, a, state_h, state_ph)
    else:
        return incorrect

def trans(Pe, S, a):
    p_state = S[:2]
    h_state = S[2]
    if a[0] == 'none': # this will return a tuple choose a container
        Sp = S
        return Sp
    else:
        hpos_rot = (h_state - 1) % 12
        hneg_rot = (h_state+1) % 12
        sample_set = [h_state, hpos_rot, hneg_rot]
        prob_dist = [1-2*Pe, Pe, Pe]
        sample = np.random.choice(3, 1, replace=True, p=prob_dist)
        ph_state = np.array([sample_set[np.asscalar(sample)]])
        for v in card_direc:  # how do i make this a while loop, look for a better way to do this
            if np.arccos(np.dot(v, rot_array[np.asscalar(ph_state)])) <= np.pi/6 + epsilon:
                break
        facing = v
        if a[0] == 'forwards':
            pp_state = p_state + facing
        else:
            pp_state = p_state - facing
        if pp_state[0] > (W-1) or pp_state[0] < 0 or pp_state[1] > (L-1) or pp_state[1] < 0:
            pp_state = p_state
        ph_state_new = ph_state
        if a.__len__() == 2:
            if a[1] == 'left':
                ph_state_new = np.array([(np.asscalar(ph_state_new) - 1)%12])
            else:
                ph_state_new = np.array([(np.asscalar(ph_state) + 1)%12])
        Sp = np.concatenate((pp_state, ph_state_new), axis=0)
        return Sp, ph_state, facing


def R(S):
    h=S
    if h[0] == 0 or h[0] == (W-1) or h[1] == 0 or h[1] == (L-1):
        reward = -100
    elif h[1] in range(2, 6):
        if h[0] == 2:
            reward = -1
        elif h[0] == 4:
            reward = -1
        elif h[0] == 3 and h[1] == 4:
            reward = 1
    else:
        reward = 0
    return reward



# Main Function
if __name__ == '__main__':
    S = np.array([3, 5, 11])  # I could prerotate to 2 from 1, then tell my robot to go right and end up at 3
    Sp = np.array([3, 5, 9])
    action = ['forwards', 'left']
    print trans(.3, S, action)
    print Psa(.3, S, action, Sp)
    print R(S)