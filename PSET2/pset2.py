
import numpy as np

# Alexie Pogue PSET 2

W=6 # are these global variables? That's bad right?
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
        return Sp


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


def angle_calc(S):
    goal = np.array([3, 4])
    position_state = S[:2]
    if np.allclose(position_state, goal): #to avoid divide by zero if on the goal state
        return "you've made it"
    else:
        heading = S[2]
        heading_back = (heading + 6) % 12
        if heading in np.arange(11,14)%12:
            facing = 'north'
        elif heading in range(2, 5):
            facing = 'east'
        elif heading in range(5,8):
            facing = 'south'
        else:
            facing = 'west'
        heading_vector = np.array([heading, heading_back])
        look_ahead_n = np.array([position_state + north])
        look_ahead_s = np.array([position_state + south])
        look_ahead_e = np.array([position_state + east])
        look_ahead_w = np.array([position_state + west])
        look_ahead_position = {'north': look_ahead_n, 'south': look_ahead_s,
                           'east': look_ahead_e, 'west': look_ahead_w}
        goal_vector = goal - position_state
        norm_goal_vector = goal_vector / np.linalg.norm(goal_vector)
        look_ahead_2 = np.array([[]]) # 2D array
        if heading in np.arange(11, 14)%12 or heading in range(5, 8):
            if goal_vector[1] > 0:
                look_ahead = look_ahead_position['north']
                due = 'north'
            elif goal_vector[1] == 0:
                look_ahead = look_ahead_position['north']
                look_ahead_2 = look_ahead_position['south']
                due = 'north'
                due2 = 'south'
            else:
                look_ahead = look_ahead_position['south']
                due = 'south'
        else:
            if goal_vector[0] > 0:
                look_ahead = look_ahead_position['east']
                due = 'east'
            elif goal_vector[0] == 0:
                look_ahead = look_ahead_position['east']
                look_ahead_2 = look_ahead_position['west']
                due = 'east'
                due2 = 'west'
            else:
                look_ahead = look_ahead_position['west']
                due = 'west'
        if np.allclose(look_ahead, goal): #to avoid divide by zero if next to the goal state (and due that direction)
            if facing == due:
                command = ['forwards']
            else:
                command = ['backwards']
            return command
        else:
            look_ahead_vectors = np.concatenate((look_ahead, look_ahead_2), axis=1)
            look_ahead_vectors = np.reshape(look_ahead_vectors, (look_ahead_vectors.shape[1]/2, 2))
            goal_vectors_ahead = goal - look_ahead_vectors
            heading_angles = np.array([[]])
            for m in range(look_ahead_vectors.shape[0]):
                norm_goal_vector_ahead = goal_vectors_ahead[m]/np.linalg.norm(goal_vectors_ahead[m])
                angle = np.empty((1, 2))
                for n, v in np.ndenumerate(heading_vector):
                    angle[0][n] = np.arccos(np.dot(norm_goal_vector_ahead, rot_array[v]))
                heading_angles = np.append(heading_angles, angle, axis=(m-1))
            min_angle = np.amin(heading_angles)
            if heading_angles.shape[0] == 1:
                h = 0
                if facing == due:
                    translation_command = 'forwards'
                else:
                    translation_command = 'backwards'
            elif heading_angles.shape[0] == 2:
                if min_angle in heading_angles[0]:
                    heading_angles = np.delete(heading_angles, 1, axis=0)
                    h = 0
                    if facing == due:
                        translation_command = 'forwards'
                    else:
                        translation_command = 'backwards'
                else:
                    heading_angles = np.delete(heading_angles, 0, axis=0)
                    h = 1
                    if facing == due2:
                        translation_command = 'forwards'
                    else:
                        translation_command = 'backwards'
            if min_angle < np.pi / 12 - epsilon:
                command = [translation_command]
            else:
                copy = np.squeeze(heading_angles)
                if min_angle == copy[0]:
                    input = heading
                else:
                    input = heading_back
                cross_heading = np.concatenate((rot_array[np.asscalar(input)], np.zeros(1)), axis=0)
                cross_next_goal = np.concatenate((goal_vectors_ahead[h][:], np.zeros(1)), axis=0)
                rotation = np.cross(cross_heading, cross_next_goal)
                if rotation[2] < 0:
                    rotation_c = 'right'
                else:
                    rotation_c = 'left'
                command = [translation_command,  rotation_c]
            return heading_angles*180/np.pi, due, min_angle*180/np.pi, command

# Main Function
if __name__ == '__main__':
    S = np.array([3, 3, 11])  # I could prerotate to 2 from 1, then tell my robot to go right and end up at 3
    Sp = np.array([3, 5, 9])
    action = ['none']
    print trans(.3, S, action)
    print Psa(.3, S, action, Sp)
    # print R(S)
    # print policy0(np.array([4, 5, 4]))
    print angle_calc(S)