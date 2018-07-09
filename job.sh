#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=4
#SBATCH --gres=gpu:4
#SBATCH --job-name=aj
echo $CUDA_VISIBLE_DEVICES
make
