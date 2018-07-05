SHELL := /bin/bash

ifeq (${HOSTNAME},hp)
	nice =
	threads =
else
	nice = nice -n 11
	threads = -np 32
endif

.PRECIOUS: log.* dump.*

all: log.pull
log.pull: in.pull average_normal_force.txt in.potential
	$(nice) mpirun $(threads) lmp -var normal_force $$(cat average_normal_force.txt) -in in.pull
average_normal_force.txt: log.down find_normal_force.py
	python find_normal_force.py
log.down: in.down in.common_regions in.common_variables in.potential
	$(nice) mpirun $(threads) lmp -in in.down
