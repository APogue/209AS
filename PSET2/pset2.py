
import numpy as np
from time import clock
import visuals
from visuals import gridWorld
# CODE DEBUG VERSION

# Alexie Pogue PSET 2


class gridWorlds:
    '''Creates a Grid World object based on grid L and W'''
    # necessary attributes used by functions
    discount = 0.9
    epsilon = 1e-12
    error = 1
    north = np.array([0, 1])
    south = np.array([0, -1])
    east = np.array([1, 0])
    west = np.array([-1, 0])
    none = np.array([0, 0])
    card_direc = [north, south, east, west, none]
    clock_angle = np.arange(5 * np.pi / 2, 2 * np.pi / 3, -2 * np.pi / 12)  # heading angles
    rot_array = np.array([[np.cos(i), np.sin(i)] for i in clock_angle])  # heading vectors 2D
    a = []

    def __init__(self, W, L, h, Pe, desired_goal):
        self.Pe = Pe
        self.W = W
        self.L = L
        self.h = h
        self.W_count = range(W)
        self.L_count = range(L)
        self.h_count = range(h)
        self.S = np.array([[x, y, h] for x in self.W_count for y in self.L_count for h in self.h_count])
        self.policy_0 = {}
        self.policy_i = {}
        self.goal_states = []
        self.reward = 0
        self.desired_goal = desired_goal

    def goal(self, heading):
    # used to change goal states
        if heading == 'all':
            self.goal_states = set((3, 4, h) for h in self.h_count)
        else:
            self.goal_states = set((3, 4, h) for h in range(6, 7))
        return self.goal_states

    def A(self):
    # action space
        self.a = [['forwards'], ['forwards', 'right'], ['forwards', 'left'], ['backwards'], ['backwards', 'right'], ['backwards', 'left'], ['none']]
        return self.a

    def R(self, single_state):
    # reward function, returns a reward for a single state input
        goal_states = self.goal(self.desired_goal)
        h = single_state
        if h[0] <= 0 or h[0] >= (self.W-1) or h[1] <= 0 or h[1] >= (self.L-1):
            self.reward = -100
        elif h[1] in range(2, 5):
            if h[0] == 2:
                self.reward = -10
            elif h[0] == 4:
                self.reward = -10
            elif tuple(h) in goal_states:
                self.reward = 100
            else:
                self.reward = 0
        else:
            self.reward = 0
        return self.reward
    def p_sa(self, single_state1, single_a1, Sp):
    # transition function given a single state input and single action input, output is probability
        correct = 1-2*self.Pe
        incorrect = self.Pe
        state = single_state1[:2]
        state_p = Sp[:2]
        move = state_p - state  # move from state to probable state
        state_h = single_state1[2]              # heading of state
        state_ph = Sp[2]           # heading of probable state

        def heading_check():
            if single_a1.__len__() == 2:
                if single_a1[1] == 'left':
                    if state_ph == (state_h - 1) % 12:
                        return correct
                    else:
                        return incorrect
                if single_a1[1] == 'right':
                    if state_ph == (state_h + 1) % 12:
                        return correct
                    else:
                        return incorrect
            else:
                if state_h == state_ph:
                    return correct
                else:
                    return incorrect
        if single_a1[0] == 'none' and np.allclose(single_state1, Sp):
            return correct
        elif single_a1[0] == 'none' and np.allclose(single_state1, Sp) is False:
            return 0
        elif np.linalg.norm(move) <= 1:
            return heading_check()
        else:
            return 0

    def transition_function(self, Pe1, single_state2, single_a2):
    # single state input and s' output depeding on probability distribution
        p_state = single_state2[:2]
        h_state = single_state2[2]
        if single_a2[0] == 'none': # this will return a tuple choose a container
            Sp = single_state2
            return Sp
        else:
            hpos_rot = (h_state - 1) % self.h
            hneg_rot = (h_state+1) % self.h
            sample_set = [h_state, hpos_rot, hneg_rot]
            prob_dist = [1-2*Pe1, Pe1, Pe1]
            sample = np.random.choice(3, 1, replace=True, p=prob_dist)
            ph_state = np.array([sample_set[np.asscalar(sample)]])
            for v in self.card_direc:  # how do i make this a while loop, look for a better way to do this
                if np.arccos(np.dot(v, self.rot_array[np.asscalar(ph_state)])) <= np.pi/6 + self.epsilon:
                    break
            facing = v
            if single_a2[0] == 'forwards':
                pp_state = p_state + facing
            else:
                pp_state = p_state - facing
            if pp_state[0] > self.W-1 or pp_state[0] < 0 or pp_state[1] > self.L-1 or pp_state[1] < 0:
                pp_state = p_state
            ph_state_new = ph_state
            if single_a2.__len__() == 2:
                if single_a2[1] == 'left':
                    ph_state_new = np.array([(np.asscalar(ph_state_new) - 1)%self.h])
                else:
                    ph_state_new = np.array([(np.asscalar(ph_state) + 1)%self.h])
            Sp = np.concatenate((pp_state, ph_state_new), axis=0)
            return Sp

    def policy_pi0(self, single_state4):
    # initial policy, returns a single action given a single state input
        goal = np.array([3, 4])
        position_state = single_state4[:2]
        if np.allclose(position_state, goal): #to avoid divide by zero if on the goal state
            self.action0 = ['none']
            return self.action0
        else:
            heading = single_state4[2]
            heading_back = (heading + 6) % self.h
            if heading in np.arange(11, 14) % self.h:
                facing = 'north'
            elif heading in range(2, 5):
                facing = 'east'
            elif heading in range(5, 8):
                facing = 'south'
            else:
                facing = 'west'
            heading_vector = np.array([heading, heading_back])
            look_ahead_n = np.array([position_state + self.north])
            look_ahead_s = np.array([position_state + self.south])
            look_ahead_e = np.array([position_state + self.east])
            look_ahead_w = np.array([position_state + self.west])
            look_ahead_position = {'north': look_ahead_n, 'south': look_ahead_s,
                                 'east': look_ahead_e, 'west': look_ahead_w}
            goal_vector = goal - position_state
            look_ahead_2 = np.array([[]])  # 2D array
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
                    self.action0 = ['forwards']
                else:
                    self.action0 = ['backwards']
                return self.action0
            else:
                look_ahead_vectors = np.concatenate((look_ahead, look_ahead_2), axis=1)
                look_ahead_vectors = np.reshape(look_ahead_vectors, (look_ahead_vectors.shape[1]/2, 2))
                goal_vectors_ahead = goal - look_ahead_vectors
                heading_angles = np.array([[]])
                for m in range(look_ahead_vectors.shape[0]):
                    norm_goal_vector_ahead = goal_vectors_ahead[m]/np.linalg.norm(goal_vectors_ahead[m])
                    angle = np.empty((1, 2))
                    for n, v in np.ndenumerate(heading_vector):
                        angle[0][n] = np.arccos(np.dot(norm_goal_vector_ahead, self.rot_array[v]))
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
                if min_angle < np.pi / 12 - self.epsilon:
                    self.action0 = [translation_command]
                else:
                    copy = np.squeeze(heading_angles)
                    if min_angle == copy[0]:
                        input = heading
                    else:
                        input = heading_back
                    cross_heading = np.concatenate((self.rot_array[np.asscalar(input)], np.zeros(1)), axis=0)
                    cross_next_goal = np.concatenate((goal_vectors_ahead[h][:], np.zeros(1)), axis=0)
                    rotation = np.cross(cross_heading, cross_next_goal)
                    if rotation[2] < 0:
                        rotation_c = 'right'
                    else:
                        rotation_c = 'left'
                    self.action0 = [translation_command,  rotation_c]
                return self.action0

    def policy_matrix(self):
        # turns the single policy output into a dict
        self.policy_0 = {tuple(x): self.policy_pi0(x) for x in self.S}
        return self.policy_0

    def policy_evaluation(self, policy):
        # returns the evaluation of a policy, value is a 4D array
        error = 1
        policy_i = policy
        value = np.zeros([self.L, self.W, self.h, 1])
        goal_states = self.goal(self.desired_goal)
        while error > self.epsilon:
            prev_value = np.copy(value)
            for state in self.S:
                value_func = np.zeros(3)
                action = policy_i[tuple(state)]
                statek_plus1 = state
                if tuple(state) not in goal_states:
                #if state in self.S:
                    pre_rotate_right = (np.array([0, 0, 1]) + statek_plus1)%self.h
                    pre_rotate_left = (np.array([0, 0, -1]) + statek_plus1)%self.h
                    statek = self.transition_function(0, statek_plus1, action)
                    statek_left = self.transition_function(0, pre_rotate_left, action)
                    statek_right = self.transition_function(0, pre_rotate_right, action)
                    probable_states = np.array([statek, statek_left, statek_right])
                    for v, s_ in enumerate(probable_states):
                        value_func[v] = np.dot(self.p_sa(statek_plus1, action, s_), (self.R(statek_plus1) + self.discount*value[s_[0]][s_[1]][s_[2]]))
                else:
                    value_func[0] = self.R(statek_plus1)
                value[statek_plus1[0]][statek_plus1[1]][statek_plus1[2]] = sum(value_func)
            error = np.array(np.amax([(value[x][y][z] - prev_value[x][y][z])**2 for x in self.L_count for y in self.W_count for z in self.h_count]))
        return value

    def policy_extraction(self, value):
        # used to extract policies from policy and value iteration, output is a dict
        policy_i = {}
        a = self.A()
        for state in self.S:
            Q_state = np.zeros(3)
            Q_value = np.zeros(7)
            statek_plus1 = state
            pre_rotate_right = (np.array([0, 0, 1]) + statek_plus1) % self.h
            pre_rotate_left = (np.array([0, 0, -1]) + statek_plus1) % self.h
            for p, action in enumerate(a):
                statek = self.transition_function(0, statek_plus1, action)
                statek_left = self.transition_function(0, pre_rotate_left, action)
                statek_right = self.transition_function(0, pre_rotate_right, action)
                probable_states = np.array([statek, statek_left, statek_right])
                for v, s_ in enumerate(probable_states):
                    Q_state[v] = np.dot(self.p_sa(statek_plus1, action, s_),
                                           (self.R(statek_plus1) + self.discount * value[s_[0]][s_[1]][s_[2]]))
                Q_value[p] = sum(Q_state)
            policy_i[tuple(state)] = a[np.asscalar(np.argmax(Q_value))]
        return policy_i

    def policy_iteration(self, policy0):
        # optimal policy, output is a dict
        policy = policy0
        old_policy = 1
        new_policy = {}
        while cmp(old_policy, new_policy) != 0:
            old_policy = dict.copy(policy)
            value = self.policy_evaluation(policy)
            new_policy = self.policy_extraction(value)
            policy = new_policy
        return policy

    def value_iteration(self):
        # returns a 4D array of optimal values
        error = 1
        value_star = np.zeros([self.L, self.W, self.h, 1])
        goal_states = self.goal(self.desired_goal)
        a = self.A()
        while error > self.epsilon:
            prev_value = np.copy(value_star)
            for state in self.S:
                Q_state = np.zeros(3)
                Q_value = np.zeros(7)
                statek_plus1 = state
                if tuple(state) not in goal_states:
                #if state in self.S:
                    pre_rotate_right = (np.array([0, 0, 1]) + statek_plus1) % self.h
                    pre_rotate_left = (np.array([0, 0, -1]) + statek_plus1) % self.h
                    for p, action in enumerate(a):
                        statek = self.transition_function(0, statek_plus1, action)
                        statek_left = self.transition_function(0, pre_rotate_left, action)
                        statek_right = self.transition_function(0, pre_rotate_right, action)
                        probable_states = np.array([statek, statek_left, statek_right])
                        for v, s_ in enumerate(probable_states):
                            Q_state[v] = np.dot(self.p_sa(statek_plus1, action, s_),
                                                (self.R(statek_plus1) + self.discount * value_star[s_[0]][s_[1]][s_[2]]))
                        Q_value[p] = sum(Q_state)
                else:
                    Q_value[0] = self.R(statek_plus1)
                value_star[statek_plus1[0]][statek_plus1[1]][statek_plus1[2]] = np.amax(Q_value)
            error = np.array(np.amax([(value_star[x][y][z] - prev_value[x][y][z])**2 for x in self.L_count for y in self.W_count for z in self.h_count]))
        optimal_policy = self.policy_extraction(value_star)
        return optimal_policy, value_star


