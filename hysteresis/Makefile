SHELL := /bin/bash
indir = .
outdir = data
host = $(shell hostname)

$(shell mkdir -p $(outdir))

lmpcmd = mpirun lmp_intel_cpu_intelmpi -var INDIR $(indir) -var OUTDIR $(outdir)
lmpcmd_one = mpirun -n 1 lmp_intel_cpu_intelmpi -var INDIR $(indir) -var OUTDIR $(outdir)


.SECONDARY:
all: $(outdir)/dump.hysteresis_water.bin

$(outdir)/dump.hysteresis_%.bin: $(indir)/in.hysteresis $(outdir)/restart.system_% $(outdir)/in.potential_%
	$(lmpcmd) -var TIMESTEP $(if $(findstring SiO2,$*),0.002,0.0005) -var SUFFIX $* -in $<

$(outdir)/restart.system_water: $(indir)/in.add_water $(outdir)/restart.system_for_water $(outdir)/in.potential_for_water $(outdir)/dump.water
	$(lmpcmd_one) -var SUFFIX for_water -in $<

$(outdir)/xyz.water: $(outdir)/add_water.inp
	packmol < $<

$(outdir)/dump.water: $(indir)/xyz2dump.py $(outdir)/xyz.water $(outdir)/restart.system_for_water
	python3 $< $$(cat $(outdir)/num_atoms) $(outdir)/xyz.water $@

$(outdir)/add_water.inp: $(indir)/in.write_packmol $(outdir)/restart.system_for_water
	$(lmpcmd_one) -var SUFFIX for_water -in $<

$(outdir)/restart.system_passivated: $(indir)/in.passivate $(outdir)/restart.system_for_passivation $(outdir)/in.potential_for_passivation
	$(lmpcmd_one) -var SUFFIX for_passivation -in $<
$(outdir)/restart.system_%: $(indir)/in.make_system $(outdir)/in.potential_% $(outdir)/data.amorphous_%
	$(lmpcmd) -var SUFFIX $* -in $<

$(outdir)/data.amorphous: $(indir)/in.make_amorphous $(indir)/in.common_variables $(indir)/in.potential
	$(lmpcmd) -in $<

$(outdir)/data.amorphous_SiO2: $(outdir)/data.amorphous
	cp $< $@
$(outdir)/data.amorphous_%: $(outdir)/data.amorphous
	python3 $(indir)/data_addH.py $< $@

$(outdir)/in.potential_SiO2: $(indir)/in.potential
	cp $< $@
$(outdir)/in.potential_%: $(indir)/in.potential_SiO2H2O
	cp $< $@

clean:
	rm -rf *.txt dump.* log.* slurm* data/ build/
