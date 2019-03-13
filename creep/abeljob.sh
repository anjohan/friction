#!/bin/sh
# Number of tasks (MPI ranks):
#SBATCH --time='0-04:00:00'
#SBATCH --account=nn9272k
#SBATCH --nodes=8
# #SBATCH --account=trocks
# #SBATCH --nodes=20
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=anjohan@uio.no
#SBATCH --mem-per-cpu=3600M
source /cluster/bin/jobsetup
#module load intelmpi.intel
module load intel/2018.1
module load intelmpi.intel

make data/restart.creep_passivated_0
