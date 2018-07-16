#!/bin/bash
#SBATCH --job-name=aj    # Job name
#SBATCH --exclude=smaug-a2,smaug-c4,smaug-c6,smaug-d1,smaug-d2,smaug-d6
#SBATCH --ntasks=128
#SBATCH --time=12:05:00  # Time limit hrs:min:sec

mpirun hostname
