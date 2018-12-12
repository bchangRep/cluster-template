#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -N 12
#SBATCH --ntasks-per-node 4

#echo command to stdout
set -x

# where do I start?
echo $SLURM_SUBMIT_DIR

module load mpi/gcc_openmpi

#Assuming hello.c is in $scratch
cd /scratch
mpicc hello.c

for i in {2..48..2}
do
  echo "With ${i} processes"
  time mpirun --allow-run-as-root -np $i ./a.out
done
