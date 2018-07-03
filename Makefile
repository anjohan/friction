SHELL := /bin/bash

all: log.pull
log.pull: in.pull average_normal_force.txt in.potential
	mpirun lmp -var normal_force $$(cat average_normal_force.txt) -in in.pull
average_normal_force.txt: log.down find_normal_force.py
	python find_normal_force.py
log.down: in.down in.common_regions in.common_variables in.potential
	mpirun lmp -in in.down
