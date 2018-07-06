#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --job-name=aj
echo $CUDA_VISIBLE_DEVICES
make
