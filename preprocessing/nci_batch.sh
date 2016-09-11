#!/usr/bin/env bash
#PBS -P ge3
#PBS -q express
#PBS -l walltime=00:30:00,mem=64GB,ncpus=3,jobfs=200GB
#PBS -l wd

module rm intel-fc intel-cc
module load python/2.7.6
module load python/2.7.6-matplotlib
module load gdal/1.11.1-python
module load openmpi/1.8
# the uncover-ml directory should be in PYTHONPATH
export PYTHONPATH=/g/data/ge3/sudipta/uncover-ml:$PYTHONPATH
# the python command needs full path of the python script
mpirun -np 3 python preprocessing/batch_job.py -i ../../covariates/national/ -o ../../covariates/national_LCC/ -m ../../covariates/masks/model_mask.tif -r bilinear -e '-2362974.47956 -5097641.80634 2251415.52044 -1174811.80634'