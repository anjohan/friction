#!/bin/bash
#SBATCH --job-name=aj    # Job name
#SBATCH --ntasks=23
#SBATCH --time=12:05:00  # Time limit hrs:min:sec

mpirun hostname
