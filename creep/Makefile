#SHELL := /bin/bash

GPUS ?= 4
host=$(shell hostname)
lammps=$(shell find ~ -name lmp 2> /dev/null)
$(shell mkdir -p data)
ITERATIONS ?= 30

ifeq (${host},hp)
	lmpcmd = mpirun lmp
else ifeq (${host},bigfacet)
	lmpcmd = mpirun -n $(GPUS) /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $(GPUS) ~/kokkos_lammps/build/lmp -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $$$$(expr $$$$(nproc) / 2) ~/lammps/build/lmp -sf gpu -pk gpu $(GPUS)
else ifeq (${host},barrier)
	lmpcmd = mpirun -n $(GPUS) lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq ($(shell hostname | grep -o smaug),smaug)
	lmpcmd = mpirun ~/lammps/build/lmp
else
	lmpcmd = mpirun $(lammps)
endif

.PRECIOUS: log.% dump.%

define defcreep =
data/restart.creep_$(1): data/restart.creep_$$(shell expr $(1) - 1) in.creep data/average_z_pressure.txt in.potential
	$(lmpcmd) -var z_pressure $$$$(cat data/average_z_pressure.txt) -var ITERATION $(1) -in in.creep
endef

all: data/restart.creep_$(ITERATIONS)

iters = $(shell seq 1 $(ITERATIONS))

$(foreach iter,$(iters),$(eval $(call defcreep,$(iter))))

data/average_z_pressure.txt: find_z_pressure.py data/restart.creep_0
	python3 $<
data/restart.creep_0: in.down in.common_regions in.common_variables
	$(lmpcmd) -var VARIANT 0 -in in.down

data/restart.creep_passivated_0: in.down in.common_regions in.common_variables
	$(lmpcmd) -var VARIANT 1 -in in.down

data/restart.passivated: in.passivate in.common_regions in.common_variables
	mpirun -n 1 $(lammps) -in $<

clean:
	rm -rf data
