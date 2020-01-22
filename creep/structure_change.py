import ase
from ase.io.lammpsrun import read_lammps_dump_binary
from ase.io.xyz import write_xyz
from ase.spacegroup import crystal, Spacegroup
import numpy as np
from dscribe.descriptors import SOAP
from tqdm import tqdm
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

steps = np.arange(0, 101000, 100000)
steps = np.arange(0, 74400000, 100000)
steps = np.arange(0, 23800000, 100000)

a = b = 4.9134
c = 5.4052
alpha = beta = 90
gamma = 120
Si = ase.Atom("Si", [0.4699, 0, 2 / 3])
O = ase.Atom("O", [0.4141, 0.2681, 0.1188 + 2 / 3])
spacegroup = Spacegroup(154)
cell = crystal([Si, O], spacegroup=spacegroup, cellpar=[a, b, c, alpha, beta, gamma])

soapgen = SOAP(species=["Si", "O", "H"], rcut=2.5, nmax=2, lmax=2, periodic=True)

quartz_soaps = soapgen.create(cell)

# for i, N in enumerate(cell.get_atomic_numbers()):
#     print(N, quartz_soaps[i])

print(quartz_soaps.shape)
# print(np.std(quartz_soaps[:3], axis=0))
# print(np.std(quartz_soaps[3:], axis=0))

Si_soap = quartz_soaps[0]
O_soap = quartz_soaps[-1]
quartz_soaps = np.zeros((15, len(Si_soap)))
quartz_soaps[14] = Si_soap
quartz_soaps[8] = O_soap
quartz_soap_norms = np.linalg.norm(quartz_soaps, axis=1).reshape((-1, 1))
print(quartz_soap_norms.min())
quartz_soaps /= quartz_soap_norms


def handle_step(step):
    infile = f"/home/anders/data/dump.water_T500_nodrift.{step}.bin"
    outfile = (
        f"/home/anders/data/dump.water_T500_struc_{step}.xyz"
    )

    with open(infile, "rb") as f:
        atoms = read_lammps_dump_binary(
            f, colnames=["id", "type", "x", "y", "z", "vx", "vy", "vz"]
        )

    Ns = atoms.get_atomic_numbers()
    Ns[Ns == 1] = 14
    Ns[Ns == 2] = 8
    Ns[Ns == 3] = 1
    atoms.set_atomic_numbers(Ns)
    soaps = soapgen.create(atoms)
    soap_norms = np.linalg.norm(soaps, axis=1).reshape((-1, 1))

    indices = Ns[Ns > 1]
    soapcomps = np.ones_like(Ns, dtype=float)
    soapcomps[Ns > 1] = np.sum(
        quartz_soaps[indices] * soaps[Ns > 1] / soap_norms[Ns > 1], axis=1
    )

    atoms.set_array("strucdiff", 1 - soapcomps)

    with open(outfile, "w") as f:
        write_xyz(f, atoms)


for step in tqdm(steps[rank::size]):
    handle_step(step)
