import numpy as np
import sys

suffix = ""

if len(sys.argv) > 3:
    geometry = sys.argv[1]
    temp = int(sys.argv[2])
    indent = sys.argv[3]
else:
    temp = int(sys.argv[1])
    indent = sys.argv[2]

z_pressure = np.loadtxt(f"data/z_pressure{suffix}_T{temp}_I{indent}_{geometry}.txt")

average_z_pressure = np.mean(z_pressure)

print(average_z_pressure)

np.savetxt(
    f"data/average_z_pressure{suffix}_T{temp}_I{indent}_{geometry}.txt",
    [average_z_pressure],
    fmt="%f",
)
