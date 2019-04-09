#!/bin/sh
# Number of tasks (MPI ranks):
#SBATCH --account=nn9272k
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=anjohan@uio.no
#SBATCH --mem-per-cpu=3600M
source /cluster/bin/jobsetup
#module load intelmpi.intel
module load intel/2018.1
module load intelmpi.intel

lammps=$(find ~ -name lmp 2> /dev/null)

mpirun $lammps $@
