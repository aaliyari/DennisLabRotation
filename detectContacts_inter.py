#! /usr/bin/env python
import linecache
import os
import argparse
from os.path import basename

def normalize_HiC(HiC_raw_file, KRnorm_file1, KRnorm_file2, resolution):
    
    # Normalizes Hi-C matrix using normalization files. Used method: KRnorm
    
    print("\n\tNormalizing Hi-C matrix, this could take a while..")
    output = open("normalized_HiC.txt", "w")
    HiC_raw = open(HiC_raw_file)
    counter = 0
    while 1:
        
        HiC_line = HiC_raw.readline()
        if not HiC_line:
            break
        i,j, M_ij = (float(x) for x in HiC_line.split())
        KR_line_i = float(linecache.getline(KRnorm_file1, int(i/resolution)+1))
        KR_line_j = float(linecache.getline(KRnorm_file2, int(j/resolution)+1))
        norm_M_ij = M_ij/(KR_line_i*KR_line_j)
        output.write(str(i) + "\t" + str(j) + "\t" + str(norm_M_ij) + "\n")
        if counter % 100000 == 0: print(counter)
        counter += 1


def find_Contacts(enhancerBED, promoterBED, HiC_file, resolution, res, outputFile):
    
    # Main function for finding enhancer-promoter contacts
    
    print("\n\tfinding enhancer-promoter contacts in HiC data...")
    
    output = open(outputFile, "w")
    
    HiC = open(HiC_file, "r")
    line = HiC.readline()
    enhancers = open(enhancerBED)
    while 1:
        enhLine = enhancers.readline()
        if not enhLine: break
        if enhLine[0] == '#': continue
        enhLine = enhLine.split()
        enhBegin = int(enhLine[1])
        enhBegin = int(enhBegin/resolution) * resolution
        promoters = open(promoterBED)
        while 1:
            promLine = promoters.readline()
            if not promLine: break
            if promLine[0] == '#': continue
            promLine = promLine.split()
            promBegin = int(promLine[1])
            promBegin = int(promBegin/resolution) * resolution
            promEnhPair1 = str(enhBegin) + '.0\t' + str(promBegin) + '.0'
            promEnhPair2 = str(promBegin) + '.0\t' + str(enhBegin) + '.0'
            while 1:
                bin_i, bin_j, M_ij = (float(x) for x in line.split())
                condition1 = (enhBegin == bin_i and promBegin == bin_j)
                condition2 = (enhBegin == bin_j and promBegin == bin_i)
                if condition1:
                    distance = bin_j - bin_i
                    expected = 1
                    obs_over_exp = str(float(M_ij/expected))
                    output.write(enhLine[0]+'\t'+enhLine[1]+'\t'+enhLine[2]+'\t' \
                                 +promLine[0]+'\t'+promLine[1]+'\t'+promLine[2]+'\t'+obs_over_exp+'\t'+line)
                    break
                if condition2:
                    distance = bin_j - bin_i
                    expected = float(linecache.getline(expectedFile, int(distance/resolution) + 1))
                    expected = 1
                    obs_over_exp = str(float(M_ij/expected))
                    output.write(enhLine[0]+'\t'+enhLine[1]+'\t'+enhLine[2]+'\t' \
                                 +promLine[0]+'\t'+promLine[1]+'\t'+promLine[2]+'\t'+obs_over_exp+'\t'+line)
                    break
                
                breakCondition = ((enhBegin < bin_i and enhBegin < bin_j) \
                                  or (promBegin < bin_i and promBegin < bin_j))
                                  if breakCondition: # when bins don't exist in HiC matrix
                                      break
                                  
                                  line = HiC.readline()
                                      if not line: break


parser = argparse.ArgumentParser(description='Detect interchromosomal enhancer-promoter contacts')

parser.add_argument('-raw', type=str, help='raw Hi-C file')
parser.add_argument('-norm1', type=str, help='KRnorm file for 1st chr')
parser.add_argument('-norm2', type=str, help='KRnorm file for 2nd chr')
parser.add_argument('-enh', type=str, help='enhancers BED file')
parser.add_argument('-prom', type=str, help='promoters BED file')
parser.add_argument('-res', type=int, help='resolution e.g. 5000')
parser.add_argument('-out', type=str, help='output file name')

args = parser.parse_args()

normalize_HiC(args.raw, args.norm1, args.norm2, args.res)
os.system("sort -k1,1n -k2,2n normalized_HiC.txt > sorted_normalized_HiC.txt")
find_Contacts(args.enh, args.prom, "sorted_normalized_HiC.txt", args.res, args.res, args.out)
