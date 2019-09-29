#SHELL := /bin/bash

GPUS ?= 4
host=$(shell hostname)
lammps=$(shell find ~ -name lmp 2> /dev/null)
$(shell mkdir -p data)
ITERATIONS ?= 50
TEMPS = 400 450 500 550

ifeq (${host},hp)
	lmpcmd = mpirun lmp
	lammps = lmp
else ifeq (${host},bigfacet)
	lmpcmd = mpirun -n $(GPUS) lmp -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $(GPUS) ~/kokkos_lammps/build/lmp -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $$$$(expr $$$$(nproc) / 2) ~/lammps/build/lmp -sf gpu -pk gpu $(GPUS)
else ifeq (${host},barrier)
	lammps = lmp -k on g 1 -sf kk -pk kokkos newton on neigh half binsize 7.5
	lmpcmd = mpirun -n 1 $(lammps)
	#lmpcmd = mpirun -n $(GPUS) lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq ($(shell hostname | grep -o smaug),smaug)
	lmpcmd = mpirun ~/lammps/build/lmp
else
	lmpcmd = mpirun $(lammps)
endif

.PRECIOUS: log.% dump.%

define defcreep =
data/restart.creep_T%_$(1): data/restart.creep_T%_$$(shell expr $(1) - 1) in.creep data/average_z_pressure_T%.txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 0 -var z_pressure $$$$(cat data/average_z_pressure_T$$*.txt) -var ITERATION $(1) -in in.creep
data/restart.creep_passivated_T%_$(1): data/restart.creep_passivated_T%_$$(shell expr $(1) - 1) in.creep data/average_z_pressure_passivated_T%.txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 1 -var z_pressure $$$$(cat data/average_z_pressure_passivated_T$$*.txt) -var ITERATION $(1) -in in.creep
data/restart.creep_water_T%_$(1): data/restart.creep_water_T%_$$(shell expr $(1) - 1) in.creep data/average_z_pressure_water_T%.txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 2 -var z_pressure $$$$(cat data/average_z_pressure_water_T$$*.txt) -var ITERATION $(1) -in in.creep
endef

all: $(foreach temp,$(TEMPS),data/restart.creep_T$(temp)_$(ITERATIONS))

iters = $(shell seq 1 $(ITERATIONS))

$(foreach iter,$(iters),$(eval $(call defcreep,$(iter))))

data/average_z_pressure_T%.txt: find_z_pressure.py data/restart.creep_T%_0
	python3 $< $*
data/average_z_pressure_passivated_T%.txt: find_z_pressure.py data/restart.creep_passivated_T%_0
	python3 $< _passivated $*
data/average_z_pressure_water_T%.txt: find_z_pressure.py data/restart.creep_water_T%_0
	python3 $< _water $*

data/restart.creep_T%_0: in.down in.common_regions in.common_variables data/data.setup
	$(lmpcmd) -var TEMP $* -var VARIANT 0 -in $<

data/restart.creep_passivated_T%_0: in.down in.common_regions in.common_variables data/data.setup_passivated
	$(lmpcmd) -var TEMP $* -var VARIANT 1 -in $<

data/restart.creep_water_T%_0: in.down in.common_regions in.common_variables data/data.setup_water
	$(lmpcmd) -var TEMP $* -var VARIANT 2 -in $<

data/data.setup: in.setup in.common_regions in.common_variables in.common_groups
	$(lmpcmd) -in $<

data/data.setup_withH: addH_data.py data/data.setup
	python $^ $@

data/data.setup_passivated: in.passivate data/data.setup_withH
	mpirun -n 1 $(lammps) -in $<

data/add_water.inp: in.write_packmol data/data.setup_passivated
	$(lammps) -in $<

data/xyz.water: data/add_water.inp
	packmol < $<

data/data.setup_water: xyz2data.py data/xyz.water
	python $<

clean:
	rm -rf data
