import time
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--tasks", type=int, default=320)
parser.add_argument("--time", type=str, default="1-00:00:00")
parser.add_argument("--gpu", action="store_true")
parser.add_argument("lmpargs", type=str)

args = parser.parse_args()

if args.gpu:
    slurmargs = [f"--ntasks={args.tasks}",
                 f"--gres=gpu:{args.tasks}"]
    jobscript = "lammpsjob_gpu.sh"
else:
    tasks_per_node = 1 if args.tasks==1 else 16
    slurmargs = [f"--ntasks-per-node={tasks_per_node}",
                 f"--nodes={args.tasks//tasks_per_node}"
                ]
    jobscript = "lammpsjob.sh"

slurmargs.append(f"--time='{args.time}'")
command = "sbatch --parsable " + " ".join(slurmargs) \
          + " " + jobscript + " " + args.lmpargs

print(command)
jobid = int(subprocess.check_output(command, shell=True).decode("utf-8"))

logfile = f"slurm-{jobid}.out"

def get_squeue():
    return subprocess.check_output("squeue").decode("utf-8")

print(f"waiting for {jobid}")
while str(jobid) in get_squeue():
    time.sleep(60)

status = subprocess.check_output(f"sacct -j {jobid}", shell=True).decode("utf-8")

if "CANCELLED" in status or "FAILED" in status:
    sys.exit(1)
