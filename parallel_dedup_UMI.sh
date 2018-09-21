#!/usr/bin/env bash
# Run the script from the location of the sam files and script must be in a different directory
# Use: parallel -j 1 "../parallel_dedup_UMI.sh {}" ::: *R1.fastq.gz
# parallel -j 1 "../parallel_100dedup_UMI.sh {}" ::: *R1_001.fastq.gz

#in_dir='/media/AngusWorkspace/FC_meat/'
#out_dir='media/AngusWorkspace/FC_meat/deduped_100/'

out_dir='dedup_sbatch' # no forward slash on out_dir

samplename=$( basename $1 | sed -r 's/R1.+//' )
input_dir=$(dirname $1)

echo "${samplename}"


python bin/dedup_sbatch_creator.py -f ${in_dir}${samplename}R1_001.fastq.gz -r ${in_dir}${samplename}R2_001.fastq.gz -o ${out_dir} -s bin/dedup_100UMI_fastq.py
