import numpy as np

normal_force = np.loadtxt("normal_force.txt")

average_normal_force = np.mean(normal_force[len(normal_force) // 2:])

print(average_normal_force)

np.savetxt("average_normal_force.txt", [average_normal_force], fmt="%f")
