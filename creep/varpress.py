import numpy as np
from scipy.signal import savgol_filter
from logplotter import find_data
import matplotlib.pyplot as plt

plt.style.use("seaborn")

indents = [0.0, 0.2, 0.4, 0.6, 0.8]
max_iter = 5
diff = []
pzz = []

plt.figure(figsize=(6, 6))
plt.subplot(2, 1, 1)

for indent in indents:
    step = []
    Lz = []
    Pzz = (
        np.loadtxt(
            f"/home/anders/ssd/creep/varpress/average_z_pressure_water_T500_I{indent}.txt"
        )
        * 0.0001
    )
    pzz.append(Pzz)
    for i in range(1, max_iter + 1):
        f = f"/home/anders/ssd/creep/varpress/log.creep_water_T500_I{indent}_{i}"
        data = find_data(f)
        step += data["Step"]
        Lz += data["Lz"]

    Lz = savgol_filter(Lz, 51, 1)
    diff.append(Lz[0] - Lz[-1])
    plt.plot(
        np.asarray(step) * 0.5e-6, Lz, label=f"indent = {indent} Å, Pzz={Pzz:.2f} GPa"
    )

plt.legend()
plt.xlabel("t [ns]")
plt.ylabel("Lz [Å]")

plt.subplot(2, 1, 2)
plt.xlabel("Pzz [GPa]")
plt.ylabel("ΔLz [Å]")
plt.plot(pzz, diff, "o-")
plt.tight_layout()
plt.savefig("varpress.png")
plt.show()
