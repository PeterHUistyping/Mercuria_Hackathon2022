'''
based on:
https://doi.org/10.1016/j.tre.2011.05.011


F = fuel consumption (gallons)
s = speed (knots)
d = travel distance (nautical miles)
rF = fuel consumption per unit time 

rF = c0 + c1*s^mu

F = c0*d/s + c1*d*s**(mu-1)

dF/ds = -c0*d/s**2 + c1*d*(mu-1)*s**(mu-2)
s_star = (c0/(c1*(mu-1)))**(1/mu)
'''
import numpy as np
from scipy.stats import linregress
from matplotlib import pyplot as plt

speed = np.arange(10, 30, .5)


def fuel_consumption(c0, c1, mu, d, s):
    return c0*d/s + c1*d*s**(mu-1)


def speed_max_efficiency(c0, c1, mu):
    return (c0/(c1*(mu-1)))**(1/mu)


def fuel_cons_per_time(c0, c1, speed, mu):
    return c0 + c1*speed**mu


def gen_sample_data(n, min_speed, max_speed, c0, c1, mu):
    speeds = np.random.rand(n)*(max_speed-min_speed) + min_speed
    rf = c0 + c1*speeds**mu
    sigma = rf.mean() / 10
    rf += np.random.normal(0, sigma, len(rf))
    # plt.scatter(speeds, rf)
    # plt.show()
    return speeds, rf


def fit_sample_data(speed, rf, mu):
    # rf = c0 + c1(s**mu)
    print(len(rf))
    print(len(speed))
    model = linregress(speed**mu, rf)
    c0 = model.intercept
    c1 = model.slope
    return c0, c1


c0 = 699
c1 = 0.004238
mu = 4
d = 800


print(f'vessel max efficiency speed = {speed_max_efficiency(c0, c1, mu):.1f}')

# plt.plot(speed, fuel_consumption(c0, c1, mu, d, speed))
# plt.show()

speed, rf = gen_sample_data(50, 15, 25, c0, c1, 4)
c0, c1 = fit_sample_data(speed, rf, mu)
print(f'c0 = {c0:.3f}, c1 = {c1:.5f}')
speed_fit = np.arange(10, 30, .5)
rf_fit = fuel_cons_per_time(c0, c1, speed_fit, mu)
plt.scatter(speed, rf)
plt.plot(speed_fit, rf_fit)
plt.show()
