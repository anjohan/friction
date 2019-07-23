#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=4
#SBATCH --gres=gpu:4
#SBATCH --job-name=creep
#SBATCH --cpus-per-task=2
echo $CUDA_VISIBLE_DEVICES
make GPUS=4
