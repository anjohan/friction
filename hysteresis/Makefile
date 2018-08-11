SHELL := /bin/bash
indir = .
outdir = data
host = $(shell hostname)

$(shell mkdir -p $(outdir))

ifeq (${host},hp)
	lmpcmd = mpirun lmp -var INDIR $(indir) -var OUTDIR $(outdir)
else ifeq (${host},bigfacet)
	lmpcmd = mpirun -n $(GPUS) /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g $(GPUS) -sf kk -pk kokkos newton on neigh half binsize 7.5 -var INDIR $(indir) -var OUTDIR $(outdir)
else ifneq ($(findstring smaug, $(host)),)
	lmpcmd = mpirun ~/lammps/build/lmp -var INDIR $(indir) -var OUTDIR $(outdir)
else ifneq ($(findstring compute, $(host)),)
	lmpcmd = mpirun lmp_intel_cpu_intelmpi -var INDIR $(indir) -var OUTDIR $(outdir)
else ifneq ($(findstring login, $(host)),)
	lmpcmd = mpirun lmp_intel_cpu_intelmpi -var INDIR $(indir) -var OUTDIR $(outdir)
else
	$(error HOST NOT RECOGNISED)
endif

$(info LAMMPS command: $(lmpcmd))

.PRECIOUS: log.% dump.% data.% restart.%
all: $(outdir)/log.hysteresis_SiO2 $(outdir)/restart.system_for_passivation

$(outdir)/log.hysteresis_%: $(indir)/in.hysteresis $(outdir)/restart.system_%
	$(lmpcmd) -var SUFFIX $* -in $(indir)/in.hysteresis
$(outdir)/restart.system_%: $(indir)/in.make_system $(outdir)/in.potential_% $(outdir)/data.amorphous_%
	$(lmpcmd) -var SUFFIX $* -in $(indir)/in.make_system
$(outdir)/data.amorphous_SiO2: $(outdir)/data.amorphous
	cp $< $@
$(outdir)/data.amorphous_%: $(outdir)/data.amorphous
	python $(indir)/data_addH.py $< $@
$(outdir)/data.amorphous: $(indir)/in.make_amorphous $(indir)/in.common_variables $(indir)/in.potential
	$(lmpcmd) -in $(indir)/in.make_amorphous
$(outdir)/in.potential_SiO2: $(indir)/in.potential
	cp $< $@
$(outdir)/in.potential_%: $(indir)/in.potential_SiO2H2O
	cp $< $@

clean:
	rm -rf *.txt dump.* log.* slurm* data/ build/
