import sys

startid = int(sys.argv[1])+1
infilename, outfilename = sys.argv[2:]

with open(infilename, "r") as infile, open(outfilename, "w") as outfile:
    num_atoms = int(infile.readline())
    infile.readline()

    outfile.write("ITEM: TIMESTEP" + "\n"
                  "0" + "\n"
                  "ITEM: NUMBER OF ATOMS" + "\n"
                  "" + str(num_atoms) + "\n"
                  "ITEM: BOX_BOUNDS pp pp pp" + "\n"
                  "0.0 10000.0" + "\n"
                  "0.0 10000.0" + "\n"
                  "0.0 10000.0" + "\n"
                  "ITEM: ATOMS id type x y z" + "\n")
    id = startid
    for line in infile:
        t, x, y, z = map(eval, line.split())
        outfile.write("%d %d %g %g %g\n" % (id, t, x, y, z))
        id += 1
