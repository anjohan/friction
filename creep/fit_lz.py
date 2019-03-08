import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

R = 8.31 # J/mol/K
T = 500 # K

t, lz = np.loadtxt("data/lz.dat", unpack=True)

def prediction(t, t0, h0, factor):
    return h0 - factor*np.log(1 + t/t0)

parameters, covariances = curve_fit(prediction, t, lz)

t0, h0, factor = parameters

lz_predict = prediction(t, t0, h0, factor)

plt.plot(t, lz, label="data")
plt.plot(t, lz_predict, label="$h_0 - C*\log(1+t/t_c)$")
plt.legend()
plt.xlabel("$t [ns]")
plt.ylabel("$L_z$")
plt.savefig("lz.png")
