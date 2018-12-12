#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -N 12
#SBATCH --ntasks-per-node 4

#echo command to stdout
set -x

# where do I start?
echo $SLURM_SUBMIT_DIR

module load mpi/gcc_openmpi

cd /scratch
cp ~/examples/mpi/pi_mc.c ./
mpicc -o a.out /scratch/pi_mc.c -lm

#Edited to run perfect square of processes

echo "1 processes"
time mpirun -np 1 --hostfile ./machine_list ./a.out 100000
  
echo "4 processes"
time mpirun -np 4 --hostfile ./machine_list ./a.out 100000
  
echo "9 processes"
time mpirun -np 9 --hostfile ./machine_list ./a.out 100000
  
echo "16 processes"
time mpirun -np 16 --hostfile ./machine_list ./a.out 100000
  
echo "25 processes"
time mpirun -np 25 --hostfile ./machine_list ./a.out 100000
  
echo "36 processes"
time mpirun -np 36 --hostfile ./machine_list ./a.out 100000
