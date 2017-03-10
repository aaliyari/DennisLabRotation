# Dennis Lab Rotation

Start date: Monday February 13, 2017  
End date: Friday March 17, 2017
# Goals:
### Computational:

      Identify novel enhancer-promoter interactions caused by Human Specific Duplications (HSDs) using Hi-C data

### Experimental:

      Validate any found contacts using 3C + PCR
      
___

## Table of contents
1. [Week One: Warm Up](#week1)
2. [Week Two: Optimize the code](#week2)
3. [Week Three: Look for novel contacts](#week3)
4. [Week Four: Experiments!](#week4)
5. [Week Five: Wrap up](#week5)
6. [Appendix: How to run the scripts](#appendix)

___

## <a name="week1"></a>_Week 1_

- [x] Warm up!

- Get a sample list of promoters from [FANTOM](http://pressto.binf.ku.dk/): all chr6 promoters (BED format)
- Some HSD enhancers on chr6 (DUSP22) from Paulina (BED format)
- Hi-C matrix from [Rao & Huntley et al. 2014](http://www.cell.com/abstract/S0092-8674(14)01497-4)  
GEO accesion link: [GSE63525](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63525) (5kb resolution for now)
  
- [x] Write a python script to normalize the Hi-C matrix

- Normalization method used: KRnorm (used in Rao & Huntley et al. 2014)
```
Each entry M_ij of the raw Hi-C matrix should be divided by its corresponding values in the normalization vector file (*.KRnorm)
```
- For details, please see this [readme](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE63525&format=file&file=GSE63525%5FGM12878%5Fcombined%5FREADME%2Ertf), available in the above mentioned GEO link.
```
function: normalize_HiC(HiC_raw_file, KRnorm_file, resolution) in dennisLab.py
```

- [x] Find the number of contacts between each pair of promoters and enhancers using the normalized Hi-C matrix
- **All files should be sorted, for instance:**
```sh
sort -k1,1n -k2,2n normalized_HiC.txt > sorted_normalized_HiC.txt
```
```
function: blahblah(..) in dennisLab.py
output format: enhancer BED + promoter BED + O/E + HiC line
chr   start end   chr   start end   O/E   bin_i bin_j no. of contacts
chr6	159525909   159526201	chr6	159465863	159465874	3.29467895217     159465000.0 159525000.0	73.9561526412
```
## remember to omit -/+ in the code, it's redundant.

- The 6th column in the output file is the observed/expected value for each pair of contacting loci in the Hi-C matrix, which is a measure of the contact's significance. Expected values are provided as a seperate file (*.KRexpected) and are available for intrachromosomal contacts only.

___
     
## <a name="week2"></a>_Week 2_

- [x] Optimize the python script for finding enhancer-promoter contacts
- Utilizing the sorted property of the input files (enhancer BED, promoted BED and Hi-C matrix), the function goes through the Hi-C file only once, reading it line by line. This is vital for the overall speed considering size of the Hi-C files (several Gigabytes).

- [x] Run the script hoping to find some novel enhancer-promoter interactions due to HSDs!
- Download Hi-C data from Rao & Huntley et al. 2014, available on Cabernet
    - Human lymphoblastoid cells (GM12878)
    
            cd /share/dennislab/sequencing/public/Rao_Huntley_2014

- HSD region of interest: DUSP22
```
Ancestral -> chr6:chr6:196,309-429,124
Duplication -> chr16:33,293,711-33,465,325
```
**This is an interchromosomal duplication, so we need to look at the Hi-C matrix containing contacts between chromoome 6 and 16 located in (replace * with desired resolution):**
```
/share/dennislab/sequencing/public/Rao_Huntley_2014/GM12878_combined_interchromosomal/*_resolution_interchromosomal/chr6_chr16
```
- Input:  

  1) DUSP22 HSD enhancers on chr6 (BED format)  
  2) All promoters on chr16 from FANTOM (BED format)  
  3) Hi-C raw matrix (.RAWobserved)  
  4) Normalization vectors for both chromosomes (.KRnorm)  

- Output:  

      **Interacting enhancer-promoter pairs!**

- Result:  

      **There are enhancers in the DUSP22b HSD region on chr16 that show faint contacts with a few promoters near GRIN2A gene on chr16, which is an autism-related gene! (They are ~10Mb apart, so no reason to get super excited.)**
      
      *What's next? Design primers to validate this finding: Is this enhancer-promoter pair really in contact in vitro?*

___

## <a name="week3"></a>_Week 3_

**Hypothesis:** If the enhancer-promoter pair found in the Hi-C data are really in contact in 3D, we should be able to detect them using PCR amplification in Aarthi's Libraries. The primers are desinged based on the 3C protocol: [Naumova et al. 2012](http://www.sciencedirect.com/science/article/pii/S1046202312001788)

### Primer Design
case:  
promoter = [chr16:10,123,539-10,127,438]
primers:

OLIGO            start  len      tm     gc%   any    3' seq 
LEFT PRIMER        206   28   66.14   46.43  5.00  2.00 TTAAGGCTTCAGAGATACAGCAGTGAGC
RIGHT PRIMER       420   28   65.82   46.43  6.00  2.00 AGATTTCTCCCTGGCCTCATGATAGTAG
SEQUENCE SIZE: 695
INCLUDED REGION SIZE: 695

PRODUCT SIZE: 215, PAIR ANY COMPL: 5.00, PAIR 3' COMPL: 3.00
TARGETS (start, len)*: 318,6
```sh
    1 CTCTCTTAAGCTCAAGACTTTTTATTTTGTGTTTTTTACATTGATGAGTTATAAAGGGGT
                                                                  

   61 CTCTCTCATCTTTCCCTTCTTTTTACCTTCTTCTTTGCTGAATCTCTGCTCTCTGGCCAG
                                                                  

  121 GAGTCATTACATAGAAACTTAAGTGCAGGGTGATCATCTATTAACTCAGCAAATAGTTAT
                                                                  

  181 CGACAGCTACAATCTCAGATACTATTTAAGGCTTCAGAGATACAGCAGTGAGCAAAATTG
                               >>>>>>>>>>>>>>>>>>>>>>>>>>>>       

  241 CTGTCAAAGTGCCCACATTCTAGTGGAAAAAGCAATAAATAGATGTATTATTTGTTGCCC
                                                                  

  301 TAAAAAAGTGAAAAGTGAAGCTTCTTTGGTATGTCTCATGCACCATCTAGGGGGTAGGCT
                       ******                                     

  361 CTGCCATACTGGCTGCTGACTTGTTAAAAATACTACTATCATGAGGCCAGGGAGAAATCT
                                      <<<<<<<<<<<<<<<<<<<<<<<<<<<<

  421 GAACTCGGGAAAGTGGTGTGGGGGCCAGAATTTGAGAAGAGAAGAAGCCTACGCTGGAAT
                                                                  

  481 CGCACTTAGTTCACGTCACTTCCCAGATCTGGCTTCCAATGGCCTCTTCTCACCCTCTAA
                                                                  

  541 ATAAAATACGTAAATCCTCAATGTGGCCTTTACAATCTGCCTCTTTTAATCCTTCTCTGC
                                                                  

  601 AGCCACAATGACTTCTATGATGGTCTTCCAATACCCTGAGCCTGTTCCCACCTCAGGGTC
```
___

enhancer = [chr6:348,176-365,475]  
primers:  

OLIGO            start  len      tm     gc%   any    3' seq 
LEFT PRIMER        297   28   69.95   50.00  5.00  0.00 ATTACCATCTGACTGAAGGGTGCGAGTG
RIGHT PRIMER       590   28   62.80   46.43  5.00  3.00 CTACCTCTAAACCAATAGCTGCCACTAC
SEQUENCE SIZE: 1082
INCLUDED REGION SIZE: 1082

PRODUCT SIZE: 294, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 3.00
TARGETS (start, len)*: 470,6
```sh
    1 CCATCCTGAGTTATTAATAATTTTATTAAGAATATGCTTTCAACACGCTTGTATTTATAT
                                                                  

   61 ATGTACTTAACAAGAAATCACCAAGACTGCAGCGGGCAGTTCCTCTTCCCTTTCCTTTTC
                                                                  

  121 ATTGCCCAGAGAAAGGGAGAAAAAAAAACAACACTGCATTTGACTTGTCACTTGGAGGCT
                                                                  

  181 TAATTCCCTTCTTACATGCAGCAGTGGGGTCTCCTTCCGCCCTCAGGCACAGCTTGCTTT
                                                                  

  241 GAGACTTGCAGTATCACAATTAGTGTTCTCTTGCAGCTTGGACTTAACCAGCTTAAATTA
                                                              >>>>

  301 CCATCTGACTGAAGGGTGCGAGTGCTGGGTCTGCATGTGTTTCTTTCCATCAGGGGAAAG
      >>>>>>>>>>>>>>>>>>>>>>>>                                    

  361 ATTTGCCAGTGCATGTTTGAACATCTGCAAGTTTGGGTTTATTTTGGCTCCAAATCTGTA
                                                                  

  421 TGCAAACTGTTGGTCATAAAGAGTTAGAAGTTCACAGCGAACCTTCCTGAAGCTTCTAGT
                                                       ******     

  481 TCAGTTTTTAGAGCTTGATGTTGGAAGAGATCTATTTCAGCAGGTGCCTGAAAGTATAGG
                                                                  

  541 GAGTTCAATATTCTAATTGCGTGTAGTGGCAGCTATTGGTTTAGAGGTAGGTTTAGCAGA
                            <<<<<<<<<<<<<<<<<<<<<<<<<<<<          

  601 AAAGACATTTTGGATGGGGTCATTTCTGTGCATGTCCTGTGTACACAGGCCTGATTTTAA
                                                                  

  661 AAGCTATATAGGCCGGGTGGGGTGGCTCACGCCTGTCATCCCAGCAATTTGGGAGGCCGA
                                                                  

  721 GGTAGGTGGATCACTTGAGGTCAGGAGTTCAAGACCAGCCTGGCCATCATGGTGAAACCC
                                                                  

  781 TGTCTCTACTAAAAATACAAAAAATTAGCTGGGCGTGGTGGCAGGTGCCTGTAATCCCAG
                                                                  

  841 CTACTTGGGAAGCTGAGGCAGGAGAATCGCTTAAACCCAGGAAGTGGAGGTTGCAGTGAG
                                                                  

  901 CAGAGATCACACCATTGCACTCCAGCCTCCGCAATAAGAGTGAAACTCCGTCTGGAAAAC
                                                                  

  961 AAACAAACAAAAACCTAGATGATGGGGGTGAGGTTAGGGGGATGCTTTTTGGGTTAATAA
                                                                  

 1021 TTCCTTCAAGGAATAATGTTTGGAGGACAGGGCTTGGAAAAGTGCTAATCCCAGCAAGAG
 ```
 
 ___
 control (pair not in contact)
 enhancer: chr6	170589556	170589600
 OLIGO            start  len      tm     gc%   any    3' seq 
LEFT PRIMER        100   29   61.24   41.38  4.00  2.00 TACCAAGTAGACGCACTCTTACCATATAC
RIGHT PRIMER       338   28   59.87   35.71  4.00  1.00 GTTCTCTATCCATGTGAGCTATAATTTG
SEQUENCE SIZE: 540
INCLUDED REGION SIZE: 540

PRODUCT SIZE: 239, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 1.00
TARGETS (start, len)*: 264,6
```sh

    1 ATTCAGCTGTTCCTCAGGAAACGATTTACCTTCCCTCTGCCTTTTCTGTAAAATGCATGG
                                                                  

   61 ACTGAGGAATTACTAATGCATAACACTTTGTTTGCTGGATACCAAGTAGACGCACTCTTA
                                             >>>>>>>>>>>>>>>>>>>>>

  121 CCATATACAGGGCTGTATCTAGGCAGCCAGTTATTAGAATAAAAACAGAATACTATGTTC
      >>>>>>>>                                                    

  181 ATCCGCTCAGATAATCCCTGTGTTTGGCTTCATGTTATGGTTCGAAACTCCTAGTGACAT
                                                                  

  241 TGGTAAGAGTGAACACGAGAATGAAGCTTCTTTCATGATGAAATGTCCTGAGTGTGTGTC
                             ******                               

  301 TGTGTGTTCTCAAATTATAGCTCACATGGATAGAGAACGTTTTCTTGCTTCAGCCTCAAG
                <<<<<<<<<<<<<<<<<<<<<<<<<<<<                      

  361 TGGGGATTGGGTTGCAGTGGTGAACCAGGGCCAACACAGCCCGCCCTCTTTGAGGTTGCA
                                                                  

  421 GTCTCCTGGGACACACGCCCACTAAACAAACAGCTACACGAATTAATCATGCCACAGGGC
                                                                  

  481 AAACTGCAAGAGCACCATCACGTGCGGCAGGTAACCCAGGCGGGTCATTTTCGTGGCGGA
  ```
  
  ___
  
  promoter: chr6	13274087	13274115
  
  OLIGO            start  len      tm     gc%   any    3' seq 
LEFT PRIMER         45   29   60.11   34.48  4.00  2.00 TCTCAGTAGAAGTTATTTTCAGGATTAGC
RIGHT PRIMER       290   28   62.86   39.29  8.00  2.00 AGTTTATAATGGCTCAGGTACCAGATTG
SEQUENCE SIZE: 366
INCLUDED REGION SIZE: 366

PRODUCT SIZE: 246, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 1.00
TARGETS (start, len)*: 168,6
```

    1 AATGTCTTGCCTCCCGTCCCCACGCCAGCCGCCACTTCCTCAACTCTCAGTAGAAGTTAT
                                                  >>>>>>>>>>>>>>>>

   61 TTTCAGGATTAGCCTTCCTCAGTCGTGGGGGAACCCTACGCTTTGCCTAGGTCTCTAGGA
      >>>>>>>>>>>>>                                               

  121 ATGTGTGTTTACTTTTTTCTGCCCAAGGGGTACCCTTTAAAGTTTCCAAGCTTAATATTC
                                                     ******       

  181 TATATAATGAATTCAGAGCTTTTTCAAAGCATTTCCAAGGTCAGGGAAGCATTTGGCTTG
                                                                  

  241 TAGGATGTCTTCCTTTCGGCCCCAATCTGGTACCTGAGCCATTATAAACTTCCCATTGTT
                            <<<<<<<<<<<<<<<<<<<<<<<<<<<<          

  301 GGAGAGAAAGATAAACAGCCAGGTGAACCTGTACAACTTACTCACAGCCCGCTGCTGTAC
  ```
  ___
  promoter (control): chr16	66600315	66600370
  
OLIGO            start  len      tm     gc%   any    3' seq 
LEFT PRIMER         99   27   61.02   37.04  4.00  3.00 AGACCACTTAAAACTTGTGTGAATGAC
RIGHT PRIMER       374   29   60.39   31.03  6.00  2.00 ATAACTGCAGAAAATATGTGGAAGAATAC
SEQUENCE SIZE: 524
INCLUDED REGION SIZE: 524

PRODUCT SIZE: 276, PAIR ANY COMPL: 5.00, PAIR 3' COMPL: 0.00
TARGETS (start, len)*: 231,6
```sh
    1 GAGGAGAATAAGATGATCTCTGAAGTCTCTCCATGTTAGTATTAGATGAAGCACAGGGAG
                                                                  

   61 CAATCCGAGTACCCTAGCAAGAGAGGAATCTGGTGGGCAGACCACTTAAAACTTGTGTGA
                                            >>>>>>>>>>>>>>>>>>>>>>

  121 ATGACAGGAGTGGGGACCATGGTTAGGGCAGTGACACTTGTCTTTCTTTCCAGGTGTTTG
      >>>>>                                                       

  181 CACTTGTGACAGCAGTATGCTGTCTTGCCGACGGGGCCCTTATTTACCGGAAGCTTCTGT
                                                        ******    

  241 TCAATCCCAGCGGTCCTTACCAGAAAAAGCCTGTGCATGAAAAAAAAGAAGTTTTGTAAT
                                                                  

  301 TTTATATTACTTTTTAGTTTGATACTAAGTATTAAACATATTTCTGTATTCTTCCACATA
                                                   <<<<<<<<<<<<<<<

  361 TTTTCTGCAGTTATTTTAACTCAGTATAGGAGCTAGAGGAAGAGATTTCCGAAGTCTGCA
      <<<<<<<<<<<<<<                                              

  421 CCCCGCGCAGAGCACTACTGTAACTTCCAAGGGAGCGCTGGGAGCAGCGGGATCGGGTTT
  ```
____                                                      
                                                              
## <a name="week4"></a>_Week 4_
  
___

## <a name="week5"></a>_Week 5_  
  
___

## <a name="appendix"></a>_Appendix: How to run the scripts_
  
  
