#SHELL := /bin/bash

host=$(shell hostname)
lammps=$(shell find ~ -name lmp 2> /dev/null)

ifeq (${host},hp)
	lmpcmd = mpirun lmp
else ifeq (${host},bigfacet)
	lmpcmd = mpirun -n $(GPUS) /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq (${host},barrier)
	lmpcmd = mpirun -n 1 lmp_kokkos_cuda_mpi -k on g 1 -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq ($(shell hostname | grep -o smaug),smaug)
	lmpcmd = mpirun ~/lammps/build/lmp
else
	lmpcmd = mpirun $(lammps)
endif

.PRECIOUS: log.% dump.%

all: restart.creeped_10000
restart.creeped_10000: in.creep average_normal_force.txt in.potential
	$(lmpcmd) -var normal_force $$(cat average_normal_force.txt) -in in.creep
average_normal_force.txt: normal_force.txt find_normal_force.py
	python find_normal_force.py
normal_force.txt: in.down in.common_regions
	$(lmpcmd) -in in.down

clean:
	rm -rf *.txt dump.* log.* slurm*
