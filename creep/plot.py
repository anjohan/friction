import numpy as np
import matplotlib.pyplot as plt
from logplotter import find_data
from scipy.signal import savgol_filter

data = find_data("data/log.creep", verbose=True)
t = np.array(data["Step"]) * 2e-6
z_top = np.array(data["c_com_top_layer[3]"])
t = t[: min(len(t), len(z_top))]
z_top = z_top[: min(len(t), len(z_top))]

z_smooth = savgol_filter(z_top, len(z_top) // 50 + (1 - (len(z_top) // 50) % 2), 1)

start = len(z_smooth) // 10
linear_bit = z_smooth[start:]
a, b = np.polyfit(t[start:], linear_bit, deg=1)
approx_linear = a * t + b

plt.plot(t, z_top, label="raw")
plt.plot(t, z_smooth, label="smoothed")
plt.plot(t, approx_linear, label="linear fit")
plt.legend()
plt.xlabel(r"t [ns]")
plt.ylabel(r"z$_{\mathrm{CM}}$ of top layer [Å]")
plt.title(r"z$_{\mathrm{CM}}$ of top layer")
plt.tight_layout()
plt.savefig("z_plot.png")
