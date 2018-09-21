#!/usr/bin/env python3

__author__ = "Chris Dean and Enrique Doster"
__copyright__ = ""
__credits__ = ["Chris Dean and Enrique Doster"]
__version__ = ""
__maintainer__ = "edoster"
__email__ = "edoster@colostate.edu"
__status__ = "Cows go moo."

from Bio.SeqIO.QualityIO import FastqGeneralIterator
import argparse
import os
import sys
import gzip
import io

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--forward', type=str, required=True,
    	                help='Forward input file')
parser.add_argument('-r', '--reverse', type=str, required=True,
    	                help='Reverse input file')
parser.add_argument('-o', '--output', required=False,
    	                help='Specify output directory for deduped fastq files')

if __name__ == "__main__":
	args = parser.parse_args()

	fumi = {}  # forward {umi: {read[0:25]: count}}
	rumi = {}  # reverse {umi: {read[0:25]: count}}
	readpairs = {}  # {read_header_prefix: (fread, fqual, rread, rqual)}
	seen = set()
	with io.TextIOWrapper(io.BufferedReader(gzip.open(args.forward, 'rb'))) as f, \
	io.TextIOWrapper(io.BufferedReader(gzip.open(args.reverse, 'rb'))) as r:
		for (ftitle, fread, fqual), (rtitle, rread, rqual) in zip(FastqGeneralIterator(f), FastqGeneralIterator(r)):
			read_header_prefix = ftitle.split(' ')[0]
			assert(read_header_prefix == rtitle.split(' ')[0])  # Is mate pair, if fails run through trimmomatic first
			readpairs.setdefault(read_header_prefix, (fread, fqual, rread, rqual))
			try:
				fumi[fread[0:10]][fread[10:100]] += 1
			except KeyError:
				try:
					fumi[fread[0:10]].setdefault(fread[10:100], 1)
				except KeyError:
					fumi.setdefault(fread[0:10], {fread[10:100]: 1})
			try:
				rumi[rread[0:10]][rread[10:100]] += 1
			except KeyError:
				try:
					rumi[rread[0:10]].setdefault(rread[10:100], 1)
				except KeyError:
					rumi.setdefault(rread[0:10], {rread[10:100]: 1})

	samplename = args.forward.split('/')[-1].split('_R1')[0]
	print("Working on sample",samplename)
	with gzip.open(args.output + '/' + samplename + '_100dedup_R1.fastq.gz', 'wb') as fout, \
	gzip.open(args.output + '/' + samplename + '_100dedup_R2.fastq.gz', 'wb') as rout:
		for header, values in readpairs.items():
			fkey = values[0][0:100]
			rkey = values[2][0:100]
			if fkey in seen or rkey in seen:
				continue
			else:
				seen.add(fkey)
				seen.add(rkey)
				fout.write('@{}\n{}\n+\n{}\n'.format(
					header + ' 1:N:0:' + fkey + ' ' + str(fumi[fkey[:10]][fkey[10:]]),
					values[0][10:],
					values[1][10:]
				).encode())
				rout.write('@{}\n{}\n+\n{}\n'.format(
					header + ' 2:N:0:' + rkey + ' ' + str(rumi[rkey[:10]][rkey[10:]]),
					values[2][10:],
					values[3][10:]
				).encode())
