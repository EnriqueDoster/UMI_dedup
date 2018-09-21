#!/usr/bin/env python3
## code to read all samples that have been deduped and labeled with a UMI header

# Prints

__author__ = "Enrique Doster"
__copyright__ = ""
__credits__ = ["Enrique Doster"]
__version__ = ""
__maintainer__ = "edoster"
__email__ = "edoster@colostate.edu"

## Usage: python fastq_UMI_header_counting.py -i *.gz


from Bio import SeqIO
import argparse
import glob
import os
import sys
import gzip
import csv
from math import log
import pandas as pd

class Record(object):
	def __init__(self, id, seq, plus, qual):
		self.id = id
		self.seq = seq
		self.plus = plus
		self.qual = qual

def parse_cmdline_params(cmdline_params):
	info = "Removes duplicate FASTQ entries from a FASTQ file"
	parser = argparse.ArgumentParser(description=info)
	parser.add_argument('-i', '--input_files', nargs='+', required=True,
        	                help='Use globstar to pass a list of sequence files, (Ex: *.fastq)')
	parser.add_argument('-o', '--output_file', required=False,
        	                help='Specify output directory for deduped fastq files')
	return parser.parse_args(cmdline_params)

def write_dict_to_csv(out_file, dict):
	with open(out_file,'w') as out:
		write_out = csv.writer(out,delimiter=',')
		header = "Sample,UMI_dup_count,count"
		write_out.writerow(("Sample","UMI_dup_count","count"))
		for sample, val in dict.items():
			print(sample)
			print(val)
			for k, v in val.items():
				row = (str(sample) + "," + str(k) + "," + str(v))
				write_out.writerow((sample,k,v))

if __name__ == "__main__":
	opts = parse_cmdline_params(sys.argv[1:])
	files = opts.input_files
	output_file = opts.output_file
	UMI_all_samples = {}
	for f in files:
		sample_name = os.path.basename(str(f)).split('.', 1)[0]
		UMI_count_dic = {} #UMI_count_dic {num_dup: count}}
		print(sample_name)
		if ".gz" in str(f):
			with gzip.open(f, "rt") as handle:
				records = (r for r in SeqIO.parse(handle, "fastq"))
				for r in records:
					UMI = r.description.split(' ')[1].split(':')[3]
					UMI_count = r.description.split(' ')[2]
					try:
						UMI_count_dic[UMI_count] += 1
					except KeyError:
						UMI_count_dic.setdefault(UMI_count, 1)
		else:
			records = (r for r in SeqIO.parse(f, "fastq"))
			for r in records:
				UMI = r.description.split(' ',1)[1].split(':')[3]
				UMI_count = r.description.split(' ')[2]
				try:
					UMI_count_dic[UMI_count] += 1
				except KeyError:
					UMI_count_dic.setdefault(UMI_count, 1)
		#print(UMI_count_dic)
		UMI_all_samples[sample_name] = UMI_count_dic ## { sample_name : {UMI size : count}}
	write_dict_to_csv(output_file, UMI_all_samples)
