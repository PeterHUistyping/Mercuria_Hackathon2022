'''
p = propulsion power (kw)
dwt = tonnage
s = speed (nautical miles per hour (kn))
mu = propeller law power

POWER REGRESSION:
    p = c0 + c1 * dwt + c1 * s**mu + epsilon

'''
import numpy as np
import pandas as pd
import itertools
import statsmodels.api as sm
from scipy.stats import linregress
from matplotlib import pyplot as plt

mu_tanker = 3.4 # MAN propulsion manual Table 2.05
mu_bulker = 3.1 # MAN propulsion manual Table 2.05

speed = np.arange(10, 30, .5)


def power_required(c, dwt, s, mu):
    return c[0] + c[1] * dwt + c[2] * s**mu


def gen_X_y(df, mu):
    weights = df['dwt'].tolist()
    speeds = [int(s[:-2]) for s in df.columns if s != 'dwt']
    X = np.ndarray((len(speeds)*len(weights), 2))
    X[:, 0] = sorted(weights * len(speeds))
    X[:, 1] = speeds * len(weights)
    df.index = df['dwt']
    y = []
    for i in range(len(X)):
        y.append(df.loc[X[i, 0], f'{int(X[i, 1])}kn'])
    y = np.array(y)
    X[:, 1] = np.power(X[:, 1], mu)
    return X, y


def regress(df, mu):
    # c = [c0, c1, c2]
    X, y = gen_X_y(df, mu)
    X = sm.add_constant(X)
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())
    c = results.params.round(4).tolist()
    return c

df_tanker = pd.read_csv('regression_data/tanker_propulsion_power.csv')
df_bulker = pd.read_csv('regression_data/bulk_carrier_propulsion_power.csv')
print(df_tanker)

c_tanker = regress(df_tanker, mu_tanker)
c_bulker = regress(df_bulker, mu_bulker)
print('c_tanker = ',c_tanker)
print('c_bulker = ',c_bulker)

# c0 = 699
# c1 = 0.004238
# mu = 4
# d = 800


# print(f'vessel max efficiency speed = {speed_max_efficiency(c0, c1, mu):.1f}')

# # plt.plot(speed, fuel_consumption(c0, c1, mu, d, speed))
# # plt.show()

# speed, rf = gen_sample_data(50, 15, 25, c0, c1, 4)
# c0, c1 = fit_sample_data(speed, rf, mu)
# print(f'c0 = {c0:.3f}, c1 = {c1:.5f}')
# speed_fit = np.arange(10, 30, .5)
# rf_fit = fuel_cons_per_time(c0, c1, speed_fit, mu)
# plt.scatter(speed, rf)
# plt.plot(speed_fit, rf_fit)
# plt.show()

