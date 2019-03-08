import sys
import numpy as np
import matplotlib.pyplot as plt
from logplotter import find_data
from scipy.signal import savgol_filter

data = None

i = 0
while 1 > 0:
    i += 1
    try:
        next_data = find_data(f"data/log.creep_{i}")
        if data is None:
            data = next_data
        else:
            for key in data.keys():
                data[key] += next_data[key]
    except FileNotFoundError:
        print(f"Could not find data/log.creep_{i}")
        break

if data is None:
    sys.exit("Failed to find any files.")

t = np.array(data["Step"]) * 2e-6
z_top = np.array(data["c_com_top_layer[3]"])
t = t[: min(len(t), len(z_top))]
z_top = z_top[: min(len(t), len(z_top))]

z_smooth = savgol_filter(z_top, len(z_top) // 50 + (1 - (len(z_top) // 50) % 2), 1)

start = len(z_smooth) // 4
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
