import numpy as np
import sys

suffix = ""

if len(sys.argv) > 1:
    suffix = sys.argv[1]

z_pressure = np.loadtxt(f"data/z_pressure{suffix}.txt")

average_z_pressure = np.mean(z_pressure)

print(average_z_pressure)

np.savetxt(f"data/average_z_pressure{suffix}.txt", [average_z_pressure], fmt="%f")
