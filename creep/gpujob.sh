#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=8
#SBATCH --gres=gpu:8
#SBATCH --job-name=creep
echo $CUDA_VISIBLE_DEVICES
make GPUS=8 ITERATIONS=200
