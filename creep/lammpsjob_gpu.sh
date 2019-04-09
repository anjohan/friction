#!/bin/bash
#SBATCH --partition=normal
#SBATCH --job-name=creep
#SBATCH --cpus-per-task=2
echo $CUDA_VISIBLE_DEVICES

mpirun -n ${SLURM_NTASKS} /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g ${SLURM_NTASKS} -sf kk -pk kokkos newton on neigh half binsize 7.5 $@

