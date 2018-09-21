## Python script that receives a sample's forward and reverse read locations, creates SBATCH script

## Import packages
import argparse
import os
import sys
import gzip
import io

#USAGE : python sbatch_assembly_master.py -f ~/Dropbox/Reference_resources/Useful_code/Python/test_R1.gz -r ~/Dropbox/Reference_resources/Useful_code/Python/test_R2.gz -o test/

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--forward', type=str, required=True,
    	                help='Forward input file')
parser.add_argument('-r', '--reverse', type=str, required=True,
    	                help='Reverse input file')
parser.add_argument('-o', '--output', required=True,
    	                help='Specify output directory for SBATCH script files')
parser.add_argument('-s', '--script', required=True,
    	                help='Specify PATH of script to be run')



if __name__ == "__main__":
    args = parser.parse_args()
    if not os.path.exists(args.output):
        print("outdir path doesn't exist. trying to make")
        os.makedirs(args.output)
    print(args.forward.split('/')[-1].split('_')[0])
    samplename = str(args.forward.split('/')[-1].split('_R1')[0])
    print(samplename)
    with open(args.output + '/' + samplename + '_SLURM_script.sh', 'w') as fout:
        ## First, write the SBATCH information
        shebang = '#!/bin/bash'
        line2 = '#SBATCH --job-name=launcher%j \n \
        #SBATCH --partition=shas'
        line3 = '#SBATCH --output=dedup_log%j'
        line4 = '#SBATCH --time=10:00:00'
        fout.write('{}\n{}\n{}\n{}\n'.format(shebang,line2,line3,line4)) # Write out all necessary information for slurm at top of script
        # Load modules
        purge_mod = 'module purge'
        mod_jkd = 'module load jdk/1.8.0'
        mod_singularity = 'module load singularity/2.5.2'
        mod_gcc = 'module load gcc/6.1.0'
        mod_mpi = 'module load openmpi/2.0.1'
        #execute mod_singularity
        #exec_singularity = 'srun singularity run /scratch/summit/edoster@colostate.edu/EnriqueDoster-MEG-summit-assembly-master-latest.simg'
        # Change to output directory
        cd_out_dir= ('cd {}'.format(args.output))
        fout.write('{}\n{}\n{}\n{}\n{}\n{}\n'.format(purge_mod,mod_jkd,mod_singularity,mod_gcc, mod_mpi, cd_out_dir)) # Write out all necessary information for slurm at top of script
        dedup = ('singularity exec /scratch/summit/edoster@colostate.edu/EnriqueDoster-MEG-summit-assembly-master-latest.simg python3 {} -f {} -r {} -o {}'.format( args.script,args.forward, args.reverse,args.output))
        fout.write('{}\n'.format(dedup))
