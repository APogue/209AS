"""

Extended kalman filter plotting code

"""

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#no noise
#noise
#circle
#straight
#change R and Q
#show eigenvalues
#seed with high covariance and watch the plot converge
# in the 6 state case, when you rely too much on the model it fucks up, because you are estimating velocity
# you can make it better by modeling the slip
# an option is to sample the state at a higher rate (zoh between samples) because the slip changes every time step, and is amplified it can't catch up to the error
# use an unscented filter
# use accelerometer data for higher order integration

state_number = 'five states'

if state_number == 'five states':
    mod = __import__('pset3_EKF_5state', fromlist=['car_simulation'])
    mod2 = __import__('pset3_EKF_5state', fromlist=['EKF'])
else:
    mod = __import__('pset3_EKF_6state', fromlist=['car_simulation'])
    mod2 = __import__('pset3_EKF_6state', fromlist=['EKF'])

car_sim = getattr(mod, 'car_simulation')
EKF_sim = getattr(mod2, 'EKF')



def plot_covariance_ellipse(z_hat, sigma_hat):
    w,v = np.linalg.eig(sigma_hat)
    print('all')
    print(w)
    Pxy = sigma_hat[0:2, 0:2]
    eigval, eigvec = np.linalg.eig(Pxy)

    if eigval[0] >= eigval[1]:
        bigind = 0
        smallind = 1
    else:
        bigind = 1
        smallind = 0

    t = np.arange(0, 2 * math.pi + 0.1, 0.1)
    print('some')
    print(eigval)
    a = math.sqrt(np.absolute(eigval[bigind]))
    b = math.sqrt(np.absolute(eigval[smallind]))
    x = [a * math.cos(it) for it in t]
    y = [b * math.sin(it) for it in t]
    angle = math.atan2(eigvec[bigind, 1], eigvec[bigind, 0])
    R = np.array([[math.cos(angle), math.sin(angle)],
                  [-math.sin(angle), math.cos(angle)]])
    fx = R.dot(np.array([[x, y]]))
    px = np.array(fx[0, :] + z_hat[0][0]).flatten()
    py = np.array(fx[1, :] + z_hat[0][1]).flatten()
    plt.plot(px, py, "--r")
    plt.ylim(250, 700)
    plt.xlim(280, 320)

def main():
    k = 0
    input1 = 1.5
    input2 = 4
    sim_time = 30 # the car travels at 20 mm per second
    # input1 = 6
    # input2 = 6
    # sim_time = 6 # the car travels at 20 mm per second
    wheel_radius = 20
    wheel_base = 85
    time_step = .01
    x_i = 200
    y_i = 600
    theta_i = np.pi
    width = 500
    length = 750
    car = car_sim(wheel_radius, input1, input2, wheel_base, time_step, sim_time, x_i, y_i, theta_i, width, length)
    car_state = car.get_simulation()
    car_sensor_readout = car.get_sensor_simulation()
    estimator = EKF_sim(input1, input2, time_step, wheel_base, wheel_radius, sim_time, x_i, y_i, theta_i, width, length)

    if state_number == 'five states':
        z_hat_list = np.zeros((1, 5))
        # State Vector [x y yaw v]'
        xEst = np.array([[x_i, y_i, theta_i, 0, 0]])
        PEst = np.eye(5)
    else:
        z_hat_list = np.zeros((1, 6))
        # State Vector [x y yaw v]'
        xEst = np.array([[x_i, y_i, theta_i, 0, 0, 0]])
        PEst = np.eye(6)

    # history
    xTrue = xEst
    hxEst = xEst
    hxTrue = xTrue

    show_animation = False
    show_animation2 = True
    show_animation3 = False

    print(__file__ + " start!!")
    while k < car.loops:

        z_bar = estimator.time_propagation_update()
        F_t, W_t = estimator.time_linearization()
        sigma_bar = estimator.covariance_update()
        h_z = estimator.get_observation_model(k)
        H_t = estimator.observation_linearization()
        k_gain = estimator.kalman_gain_value()
        error = estimator.error_calculation(car_sensor_readout[k])
        z_hat = np.array([estimator.conditional_mean()])
        z_hat_list = np.concatenate((z_hat_list, z_hat), axis=0)
        sigma_hat = estimator.observation_update_covariance()

        hxEst = np.vstack((hxEst, z_hat))
        hxTrue = np.vstack((hxTrue, car_state[k]))


        if show_animation:
            plt.cla()
            plt.plot(np.array(hxTrue[:, 0]).flatten(),
                     np.array(hxTrue[:, 1]).flatten(), "-b")
            plt.plot(np.array(hxEst[:, 0]).flatten(),
                     np.array(hxEst[:, 1]).flatten(), "-r")
            #plot_covariance_ellipse(z_hat, sigma_hat)
            #plt.ylim(0, 700)
            #plt.xlim(280, 320)
            #plt.axis("equal")
            plt.grid(True)
            plt.pause(.009)

        k = k + 1



    xdata, ydata = hxTrue[:, 0].flatten(), hxTrue[:, 1].flatten()
    xdata2, ydata2 = hxEst[:, 0].flatten(), hxEst[:, 1].flatten()

    data = hxTrue
    data2 = hxEst
    error = np.absolute(data-data2)
    for k, i in np.ndenumerate(error[:, 2]):
        error[k, 2] = i % (2*np.pi)
        if i > np.pi:
            i -= 2 * np.pi
            error[k, 2] = i
    max_error = np.amax(error, axis = 0)
    ave_error = np.average(error, axis = 0)
    rmsd = np.std(error, axis = 0)
    Q = estimator.Q
    R = estimator.R
    vel = estimator.r*(input1 + input2)/2
    angVel = estimator.r*(input1 - input2)/estimator.L

    print('max error')
    print(max_error)

    print('ave error')
    print(ave_error)

    print('rmse')
    print(rmsd)

    print('Q')
    print(Q)
    print('R')
    print(R)

    print('x, y, v, theta, w')
    print(np.array([x_i, y_i, vel, theta_i, angVel]))




    if show_animation2:

        fig, ax = plt.subplots()
        ax.grid()
        ln, = ax.plot([], [], '-b', animated=True)
        ln2, = ax.plot([], [], '-r', animated=True)

        def init():
            ax.set_xlim(0, 200)
            ax.set_ylim(500, 700)
            return ln, ln2,

        def update(i):
            x = xdata[:i]
            y = ydata[:i]
            print(ydata)
            x2 = xdata2[:i]
            y2 = ydata2[:i]
            ln.set_data(x, y)
            ln2.set_data(x2, y2)
            #ax.set_ylim(0, hxTrue[i][0])
            return ln, ln2,
        #
        ani = FuncAnimation(fig, update, interval=10, frames= int(car.loops) + 1,
                            init_func=init, blit=True, repeat = False)

        ani.save('Images/firstAni.gif', writer='imagemagick')

        plt.show()

    elif show_animation3:
        #
        # setup figure
        # https://stackoverflow.com/questions/17895698/updating-the-x-axis-values-using-matplotlib-animation
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1)
        # ax1.square()
        ax1.grid()
        # set up viewing window (in this case the 25 most recent values)
        repeat_length = (np.shape(hxTrue)[0] + 1) / 100
        print(np.shape(hxTrue))
        print(repeat_length)
        ax1.set_xlim([np.amin(hxTrue[:][0]), np.amax(hxTrue[:][0])])
        #ax1.set_xlim([298, 302])
        ax1.set_ylim([0, repeat_length])

        # set up list of images for animation

        im1, = ax1.plot([], [], color=(0, 0, 1), label='car position')
        im2, = ax1.plot([], [], color=(0, 1, 0), label='EKF tracking')
        ax1.legend()
        plt.xlabel('x (mm)')
        plt.ylabel('y (mm)')
        plt.title('EKF Localization')

        def func(n):
            im1.set_xdata(xdata[:n])
            im1.set_ydata(ydata[:n])
            im2.set_xdata(xdata2[:n])
            im2.set_ydata(ydata2[:n])
            lim = ax1.set_ylim(0, ydata[n+1])
            x = np.concatenate((xdata[:n+1], xdata2[:n+1]), axis=0)
            lim2 = ax1.set_xlim(np.amin(x-.005), np.amax(x+.005))
            return im1,im2

        ani1 = FuncAnimation(fig1, func, interval=10, frames=int(car.loops), blit=False)

        ani1.save('Images/firstAni.gif', writer='imagemagick')
        plt.show()

    else:
        fig= plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.grid()
        ax.plot(xdata, ydata, label = 'car position')
        ax.plot(xdata2, ydata2, label = 'EKF tracking')
        plt.xlabel('x (mm)')
        plt.ylabel('y (mm)')
        plt.title('EKF Localization')
        ax.legend()
        plt.savefig('Images/decreasenoisezohfactor50.svg')
        plt.show()

if __name__ == '__main__':
    main()

    #
    # c1 = .00001 # this is for reduce noise factor 20
    # c2 = .00001
    # c3 = 1
    # c4 = 1
    # c5 = 1
    # c6 = 0

    # c1 = .015 # this is for system with all the noise
    # c2 = .015
    # c3 = 100
    # c4 = 1000
    # c5 = 3
    # c6 = .001
























