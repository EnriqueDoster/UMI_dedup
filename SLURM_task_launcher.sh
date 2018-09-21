#!/bin/bash
#SBATCH --partition=shas
#SBATCH --ntasks=1
#SBATCH --qos=normal
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --export=ALL
#SBATCH --mail-user=enriquedoster@gmail.com
#SBATCH --mail-type=ALL

for FILE in dedup_sbatch/*.sh; do
echo ${FILE}
sbatch ${FILE} -o ${FILE}.stdout.txt -e ${FILE}.stderr.txt
sleep 10m # pause to be kind to the scheduler
done
