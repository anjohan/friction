#SHELL := /bin/bash

host=$(shell hostname)

ifeq (${host},hp)
	lmpcmd = mpirun lmp
else ifeq (${host},bigfacet)
	lmpcmd = mpirun -n $(GPUS) /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq ($(shell hostname | grep -o smaug),smaug)
	lmpcmd = mpirun ~/lammps/build/lmp
else
	lmpcmd = mpirun -np 32 lmp
endif

.PRECIOUS: log.% dump.%

all: log.hysteresis
log.hysteresis: in.hysteresis in.common_regions restart.amorphous
	$(lmpcmd) -in in.hysteresis
restart.amorphous: in.make_amorphous in.common_variables in.potential
	$(lmpcmd) -in in.make_amorphous

clean:
	rm -rf *.txt dump.* log.* slurm*
