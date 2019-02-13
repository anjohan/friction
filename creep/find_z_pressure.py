import numpy as np

z_pressure = np.loadtxt("data/z_pressure.txt")

average_z_pressure = np.mean(z_pressure)

print(average_z_pressure)

np.savetxt("data/average_z_pressure.txt", [average_z_pressure], fmt="%f")
