import numpy as np
import matplotlib.pyplot as plt
from logplotter import find_data
from scipy.signal import savgol_filter

data = find_data("data/log.creep")
t = np.array(data["Step"]) * 2e-6
z_top = np.array(data["c_com_top_layer[3]"])

z_smooth = savgol_filter(z_top, len(z_top) // 50 + (1 - (len(z_top) // 50) % 2), 1)

Nhalf = len(z_smooth) // 2
exponential_bit = z_smooth[:Nhalf] - z_smooth[-1]
a, b = np.polyfit(t[:Nhalf], np.log(exponential_bit), deg=1)
approx_exponential = np.exp(b) * np.exp(a * t)

plt.subplots(2, 1)
plt.subplot(2, 1, 1)
plt.plot(t, z_top, label="raw")
plt.plot(t, z_smooth, label="smoothed")
plt.legend()
plt.xlabel(r"t [ns]")
plt.ylabel(r"z$_{\mathrm{CM}}$ of top layer [Å]")
plt.title(r"z$_{\mathrm{CM}}$ of top layer")

plt.subplot(2, 1, 2)
plt.semilogy(t, z_smooth - z_smooth[-1], label="data")
plt.semilogy(t, approx_exponential, label=f"exp({a:.2f}*t) fit")
plt.legend()
plt.xlabel(r"t [ns]")
plt.ylabel(r"z$_{\mathrm{CM}}$ difference from final position")
plt.title(r"z$_{\mathrm{CM}}$ difference from final position, semilog with fit")
plt.tight_layout()
plt.savefig("z_plot.png")
