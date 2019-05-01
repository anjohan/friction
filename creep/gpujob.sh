#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=8
#SBATCH --gres=gpu:8
#SBATCH --job-name=creep
#SBATCH --cpus-per-task=2
echo $CUDA_VISIBLE_DEVICES
make GPUS=8 ITERATIONS=1000 data/restart.creep_1000
