#!/bin/bash
#SBATCH --partition=normal
#SBATCH --ntasks=6
#SBATCH --gres=gpu:6
#SBATCH --job-name=aj
echo $CUDA_VISIBLE_DEVICES
#make GPUS=6

mkdir -p build
cd build
cmake .. -DGPUS=6
make
