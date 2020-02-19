#SHELL := /bin/bash

GPUS ?= 4
host=$(shell hostname)
lammps ?= $(shell find ~ -name lmp 2> /dev/null)
$(shell mkdir -p data)
ITERATIONS ?= 50
TEMPS ?= 400 450 500 550
INDENTS ?= 0.0 0.2 0.4 0.6 0.8 1.0

ifeq (${host},dell)
	lmpcmd ?= mpirun lmp
	lammps ?= lmp
else ifeq (${host},bigfacet)
	lmpcmd ?= mpirun -n $(GPUS) lmp -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $(GPUS) ~/kokkos_lammps/build/lmp -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
	#lmpcmd = mpirun -n $$$$(expr $$$$(nproc) / 2) ~/lammps/build/lmp -sf gpu -pk gpu $(GPUS)
else ifeq (${host},barrier)
	lammps ?= lmp -k on g 1 -sf kk -pk kokkos newton on neigh half binsize 7.5
	lmpcmd ?= mpirun -n 1 $(lammps)
	#lmpcmd = mpirun -n $(GPUS) lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5
else ifeq ($(shell hostname | grep -o smaug),smaug)
	lmpcmd ?= mpirun ~/lammps/build/lmp
else
	lmpcmd ?= mpirun $(lammps)
endif

.SECONDARY:

define defcreep =
data/restart.creep_T%_I$(1)_$(2): data/restart.creep_T%_I$(1)_$$(shell expr $(2) - 1) in.creep data/average_z_pressure_T%_I$(1).txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 0 -var z_pressure $$$$(cat data/average_z_pressure_T$$*_I$(1).txt) -var ITERATION $(2) -var INDENT $(1) -in in.creep
data/restart.creep_passivated_T%_I$(1)_$(2): data/restart.creep_passivated_T%_I$(1)_$$(shell expr $(2) - 1) in.creep data/average_z_pressure_passivated_T%_I$(1).txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 1 -var z_pressure $$$$(cat data/average_z_pressure_passivated_T$$*_I$(1).txt) -var ITERATION $(1) -var INDENT $(1) -in in.creep
data/restart.creep_water_T%_I$(1)_$(2): data/restart.creep_water_T%_I$(1)_$$(shell expr $(2) - 1) in.creep data/average_z_pressure_water_T%_I$(1).txt
	$(lmpcmd) -var TEMP $$* -var VARIANT 2 -var z_pressure $$$$(cat data/average_z_pressure_water_T$$*_I$(1).txt) -var ITERATION $(2) -var INDENT $(1) -in in.creep
endef

define defpress =
data/average_z_pressure_T%_I$(1).txt: find_z_pressure.py data/restart.creep_T%_I$(1)_0
	python3 $$< $$* $(1)
data/average_z_pressure_passivated_T%_I$(1).txt: find_z_pressure.py data/restart.creep_passivated_T%_I$(1)_0
	python3 $$< _passivated $$* $(1)
data/average_z_pressure_water_T%_I$(1).txt: find_z_pressure.py data/restart.creep_water_T%_I$(1)_0
	python3 $$< _water $$* $(1)
data/restart.creep_T%_I$(1)_0: in.down in.common_regions in.common_variables data/data.setup
	$(lmpcmd) -var TEMP $$* -var VARIANT 0 -var INDENT $(1) -in $$<
data/restart.creep_passivated_T%_I$(1)_0: in.down in.common_regions in.common_variables data/data.setup_passivated
	$(lmpcmd) -var TEMP $$* -var VARIANT 1 -var INDENT $(1) -in $$<
data/restart.creep_water_T%_I$(1)_0: in.down in.common_regions in.common_variables data/data.setup_water
	$(lmpcmd) -var TEMP $$* -var VARIANT 2 -var INDENT $(1) -in $$<
endef

all: $(foreach indent,$(INDENTS),$(foreach temp,$(TEMPS),data/restart.creep_T$(temp)_I$(indent)_$(ITERATIONS)))

water500: $(foreach indent,$(INDENTS),data/restart.creep_water_T500_I$(indent)_$(ITERATIONS))

iters = $(shell seq 1 $(ITERATIONS))

$(foreach indent,$(INDENTS),$(foreach iter,$(iters),$(eval $(call defcreep,$(indent),$(iter)))))
$(foreach indent,$(INDENTS),$(eval $(call defpress,$(indent))))




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
