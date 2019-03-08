import numpy as np
import ase
from ase.visualize import view
from ase.spacegroup import crystal, Spacegroup


a = b = 4.9134
c = 5.4052
alpha = beta = 90
gamma = 120
Si = ase.Atom("Si", [0.4699, 0, 2 / 3])
O = ase.Atom("O", [0.4141, 0.2681, 0.1188 + 2 / 3])
spacegroup = Spacegroup(154)
cell = crystal([Si, O], spacegroup=spacegroup, cellpar=[a, b, c, alpha, beta, gamma])

ase.io.write("alpha-quartz.eps", cell, rotation="10x,-10y", show_unit_cell=2)

cell = cell.repeat([2, 2, 1])
cell.set_cell([[a, 0, 0], [0, b * np.sqrt(3), 0], [0, 0, c]])
cell.wrap()
ase.geometry.get_duplicate_atoms(cell, delete=True)

ase.io.write("alpha-quartz-orthogonal.eps", cell, rotation="10x,-10y", show_unit_cell=2)

for eps in ["alpha-quartz.eps", "alpha-quartz-orthogonal.eps"]:
    with open(eps, "r") as infile:
        code = infile.read()
    with open(eps, "w") as outfile:
        outfile.write(code.replace("1.000 setlinewidth", "0.100 setlinewidth"))

positions = cell.get_positions()
atomic_numbers = cell.get_atomic_numbers()
basis_vectors = cell.get_cell()

with open("orthogonal_alpha_quartz.data", "w") as outfile:
    outfile.write("# Orthogonal alpha quartz supercell\n\n")
    outfile.write(
        f"{len(positions)} atoms\n"
        "2 atom types\n"
        "\n"
        f"0.0 {basis_vectors[0,0]} xlo xhi\n"
        f"0.0 {basis_vectors[1,1]} ylo yhi\n"
        f"0.0 {basis_vectors[2,2]} zlo zhi\n"
        "\n"
        "Atoms\n"
        "\n"
    )
    for i, atomic_number in enumerate(atomic_numbers):
        atom_type = 1 if atomic_number == 14 else 2
        outfile.write(f"{i+1} {atom_type} " + " ".join(map(str, positions[i])) + "\n")
