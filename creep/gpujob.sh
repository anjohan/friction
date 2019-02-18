#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=7
#SBATCH --gres=gpu:7
#SBATCH --job-name=creep
echo $CUDA_VISIBLE_DEVICES
make GPUS=7 ITERATIONS=200
