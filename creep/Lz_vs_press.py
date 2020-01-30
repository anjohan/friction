from logplotter import find_data
import matplotlib.pyplot as plt
import numpy as np

indents = [0.0, 0.2, 0.4, 0.6]

for indent in indents:
    time = []
    Lz = []
    press = (
        np.loadtxt(
            f"/home/anders/ssd/creep/varpress/average_z_pressure_water_T500_I{indent}.txt"
        )
        / 10
    )

    i = 1
    while True:
        try:
            filename = (
                f"/home/anders/ssd/creep/varpress/log.creep_water_T500_I{indent}_{i}"
            )
            print(filename)
            data = find_data(filename)
        except FileNotFoundError:
            break
        print(indent, i)
        i += 1
        time += data["Step"]
        Lz += data["Lz"]

    time = np.asarray(time) * 0.5e-6
    Lz = np.asarray(Lz)

    plt.plot(time, Lz, label=f"Pzz = {press:.0f} MPa")

plt.legend()
plt.grid()
plt.xlabel("t [ns]")
plt.xlabel("Lz [Å]")
plt.show()
