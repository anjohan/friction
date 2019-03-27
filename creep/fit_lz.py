import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from logplotter import find_data

R = 8.31 # J/mol/K
T = 500 # K

i = 0
t = []
lz = []
while True:
    i += 1
    print(i)
    try:
        data = find_data(f"data/log.creep_{i}")
        t += data["Step"]
        lz += data["Lz"]
    except FileNotFoundError:
        break

t = np.asarray(t)*2e-6
lz = np.asarray(lz)

N = len(t)
window_length = N//40 + (N//40)%2 + 1
lz_smooth = savgol_filter(lz, window_length, 3)

# t, lz = np.loadtxt("data/lz.dat", unpack=True)

def prediction(t, t0, h0, factor):
    return h0 - factor*np.log(1 + t/t0)

parameters, covariances = curve_fit(prediction, t, lz_smooth)

t0, h0, factor = parameters

lz_predict = prediction(t, t0, h0, factor)

plt.plot(t, lz, label="raw data")
plt.plot(t, lz_smooth, label="smoothed")
plt.plot(t, lz_predict, label="$h_0 - C\cdot\log(1+t/t_c)$")
plt.legend()
plt.xlabel("$t$ [ns]")
plt.ylabel("$L_z$ [Å]")
plt.savefig("lz.png")

np.savetxt("data/lz_fit.dat", np.column_stack((t, lz, lz_smooth, lz_predict))[::100], header="t lz smooth fit")
