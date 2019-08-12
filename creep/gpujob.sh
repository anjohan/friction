#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=3
#SBATCH --gres=gpu:3
#SBATCH --job-name=creep
#SBATCH --cpus-per-task=2
echo $CUDA_VISIBLE_DEVICES
make GPUS=3 ITERATIONS=50 data/restart.creep_T$1_50
