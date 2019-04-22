import numpy as np

with open("data/data.setup_passivated", "r") as infile:
    for i in range(5):
        infile.readline()
    xmin, xmax = map(float, infile.readline().split()[:2])
    ymin, ymax = map(float, infile.readline().split()[:2])
    zmin, zmax = map(float, infile.readline().split()[:2])

data = np.loadtxt("./data/xyz.water", unpack=True, skiprows=2)
number_of_atoms = len(data[0])

new_data = np.column_stack((np.arange(1, number_of_atoms + 1), *data))

np.savetxt(
        "./data/data.setup_water",
        new_data,
        fmt="%d %d %g %g %g",
        header=f"""created by xyz2data.py

{number_of_atoms} atoms
3 atom types

{xmin} {xmax} xlo xhi
{ymin} {ymax} ylo yhi
{zmin} {zmax} zlo zhi

Masses

1 28.08
2 15.9994
3 1.00794

Atoms
""", comments="")
