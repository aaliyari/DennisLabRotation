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
```
function: blahblah(..) in dennisLab.py
output format: enhancer BED + promoter BED + O/E + HiC line
chr   start end   chr   start end   O/E   bin_i bin_j no. of contacts
chr6	159525909   159526201	chr6	159465863	159465874	3.29467895217     159465000.0 159525000.0	73.9561526412
```

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
```      
What's next? Design primers to validate this finding: Is this enhancer-promoter pair really in contact in vitro?
```
___

## <a name="week3"></a>_Week 3_

**Hypothesis:** If the enhancer-promoter pair found in the Hi-C data are really in contact in 3D, we should be able to detect them using PCR amplification in Aarthi's Hi-C Libraries. The primers are desinged based on the 3C protocol: [Naumova et al. 2012](http://www.sciencedirect.com/science/article/pii/S1046202312001788)

### Experimental Design:

- **Case**  

      HSD Enhancer = [chr6:348,176-365,475] duplicated in DUSP22b on chr16  
      Promoter = [chr16:10,123,539-10,127,438] located near GRIN2A on chr16
      
- **Control #1**  

      A promoter that is not in contact with the case enhancer (found using Hi-C data and correlation data in FANTOM)  
      Control Promoter #1 = [chr16:66600315-66600370]  
      
- **Control #2**  

      An enhancer-promoter pair that are not in contact (based on Hi-C data and FANTOM database)  
      Control Enhancer #1 = [chr6:170589556-170589600]  
      Control Promoter #2 = [chr6:13274087-13274115]  
      
      
- **Aarthi's Hi-C Library**

       Ask Aarthi for a description!
   
### Steps:

- [x] 1) Desgin primers using [Primer3](http://bioinfo.ut.ee/primer3-0.4.0/primer3/) for all enhancers/promoters based on the protocol described in [Naumova et al. 2012](http://www.sciencedirect.com/science/article/pii/S1046202312001788)

> "To increase specificity of the primers we recommend designing
long primers with high melting temperature (on average the Tm is
90C); the length of 3C primers is 28–30 bp with a GC content of
50%, preferably carrying a single G or C nucleotide on the 30
end. We have found that the use of rather long primers is especially
important for complex genomes, where short 20 bp primers do not
provide necessary specificity and efficiency. Primers are designed
80–150 bp away from the restriction cut site so that the predicted
amplicon will be between 160 and 300 bp in size. We
recommend checking the uniqueness of each primer."              

- [x] 2) PCR bi-directional primers for each enhancer and promoter using gDNA:

            Expected result: should amplify!
            Observed result: they did!
           
- [x] 3) Do one primer-free PCR for control
            
            Expected result: nothing should amplify!
            Observed result: nothing amplified!
                 
- [x] 4) PCR uni-directional primers for each enhancer-promoter pair using Aarthi's Hi-C Libary:
            
            Expected result: should see some amplification
            Observed result: TBD


### Primer Design

- **Case Promoter**  

            Promoter = [chr16:10,123,539-10,127,438] located near GRIN2A on chr16
      
- Designed primers (output from Primer3):

            OLIGO            start  len      tm     gc%   any    3' seq 
            LEFT PRIMER        206   28   66.14   46.43  5.00  2.00 TTAAGGCTTCAGAGATACAGCAGTGAGC
            RIGHT PRIMER       420   28   65.82   46.43  6.00  2.00 AGATTTCTCCCTGGCCTCATGATAGTAG
          
            PRODUCT SIZE: 215, PAIR ANY COMPL: 5.00, PAIR 3' COMPL: 3.00
            TARGETS (start, len)*: 318,6
            
       
        181 CGACAGCTACAATCTCAGATACTATTTAAGGCTTCAGAGATACAGCAGTGAGCAAAATTG
                                     >>>>>>>>>>>>>>>>>>>>>>>>>>>>       
        241 CTGTCAAAGTGCCCACATTCTAGTGGAAAAAGCAATAAATAGATGTATTATTTGTTGCCC
        301 TAAAAAAGTGAAAAGTGAAGCTTCTTTGGTATGTCTCATGCACCATCTAGGGGGTAGGCT
                             ******                                     
        361 CTGCCATACTGGCTGCTGACTTGTTAAAAATACTACTATCATGAGGCCAGGGAGAAATCT
                                            <<<<<<<<<<<<<<<<<<<<<<<<<<<<
        421 GAACTCGGGAAAGTGGTGTGGGGGCCAGAATTTGAGAAGAGAAGAAGCCTACGCTGGAAT
        
___

- **Case Enhancer**  

            HSD Enhancer = [chr6:348,176-365,475] duplicated in DUSP22b on chr16 
      
- Designed primers (output from Primer3):

            OLIGO            start  len      tm     gc%   any    3' seq 
            LEFT PRIMER        297   28   69.95   50.00  5.00  0.00 ATTACCATCTGACTGAAGGGTGCGAGTG
            RIGHT PRIMER       590   28   62.80   46.43  5.00  3.00 CTACCTCTAAACCAATAGCTGCCACTAC
            
            PRODUCT SIZE: 294, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 3.00
            TARGETS (start, len)*: 470,6


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
 
___
 
- **Control Promoter #1**

            A promoter that is not in contact with the case enhancer (found using Hi-C data and correlation data in FANTOM)  
            Control Promoter #1 = [chr16:66600315-66600370]   
      
- Designed primers (output from Primer3):

            OLIGO            start  len      tm     gc%   any    3' seq 
            LEFT PRIMER         99   27   61.02   37.04  4.00  3.00 AGACCACTTAAAACTTGTGTGAATGAC
            RIGHT PRIMER       374   29   60.39   31.03  6.00  2.00 ATAACTGCAGAAAATATGTGGAAGAATAC
           
            PRODUCT SIZE: 276, PAIR ANY COMPL: 5.00, PAIR 3' COMPL: 0.00
            TARGETS (start, len)*: 231,6

    
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
 
___
 
 - **Control Promoter #2**  

            An enhancer-promoter pair that are not in contact (based on Hi-C data and FANTOM database)  
            Control Promoter #2 = [chr6:13274087-13274115]  

- Designed primers (output from Primer3):

            OLIGO            start  len      tm     gc%   any    3' seq 
            LEFT PRIMER         45   29   60.11   34.48  4.00  2.00 TCTCAGTAGAAGTTATTTTCAGGATTAGC
            RIGHT PRIMER       290   28   62.86   39.29  8.00  2.00 AGTTTATAATGGCTCAGGTACCAGATTG
         
            PRODUCT SIZE: 246, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 1.00
            TARGETS (start, len)*: 168,6


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
       
___
 
- **Control Enhancer #1**  

            An enhancer-promoter pair that are not in contact (based on Hi-C data and FANTOM database)  
            Control Enhancer #1 = [chr6:170589556-170589600]  

- Designed primers (output from Primer3):

            OLIGO            start  len      tm     gc%   any    3' seq 
            LEFT PRIMER        100   29   61.24   41.38  4.00  2.00 TACCAAGTAGACGCACTCTTACCATATAC
            RIGHT PRIMER       338   28   59.87   35.71  4.00  1.00 GTTCTCTATCCATGTGAGCTATAATTTG
        
            PRODUCT SIZE: 239, PAIR ANY COMPL: 4.00, PAIR 3' COMPL: 1.00
            TARGETS (start, len)*: 264,6


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
        
____                                                      
                                                              
## <a name="week4"></a>_Week 4_

Do the experiments..

Add some results here..

___

## <a name="week5"></a>_Week 5_  

- [x] Clean up the script: automate everything, user input from terminal etc.
- [x] Write a brief manual for the scirpt and add comments for functions
- [ ] Write the rotation report
- [ ] Practice for the chalk talk on Friday

### Bonus computational task
           
1) Find all (genome-wide, intra and inter-chromosomal) enhancer-promoter contacts caused by HSDs
- HSD enhancers list from Paulina
- Hi-C data from Rao & Huntley et al. 2014, downloaded to:

            cd /share/dennislab/sequencing/public/Rao_Huntley_2014

2) Find the closest genes to affected promoters

- Download the hg19 GTF file from [ENSEBML](ftp://ftp.ensembl.org/pub/grch37/release-87/gtf/homo_sapiens/)
- Add "chr" to first column of the GTF file for compatibility with BEDtools:

            awk '$1="chr"$1' hg19.gtf > hg19_chr.gtf
         
- Convert to BED (BEDtools closest does not work on GTF format) and sort:

            fgrep -w transcript hg19_chr.gtf | sed 's/[";]//g;' | awk '{OFS="\t"; print $1, $4-4,$5,$12,0,$7,$18,$14,$10}' > hg19_gtf2bed.txt
            sort -k1,1 -k2,2n hg19_gtf2bed.txt > hg19_gtf2bed_sorted.txt
            
- Finally find the closest gene to each promoter using BEDtools closest:

            bedtools closest -a promoters_chr6.txt -b hg19_gtf2bed_sorted.txt > closestGens2promoters_example.txt
            
3) Differential gene expression level analysis between human, chimp and rhesus  
- data from [Cain et al. 2011](http://www.genetics.org/content/187/4/1225.supplemental): [FileS2.xls](http://www.genetics.org/highwire/filestream/412763/field_highwire_adjunct_files/12/FileS2.xls.zip)

4) Look for differentially expressed genes between species! Are these differences statistically significant?

___

## <a name="appendix"></a>_Appendix: How to run the scripts_

Script Name: detectContacts_intra.py

      Usage: ./detectContacts_intra.py -raw <raw Hi-C file> -norm <KRnorm file> -enh <enhancers BED file> -prom <promoters BED file> -exp <KRexpected file> -res <resolution> -out <output file name>
      
**Promoter and enhancer BED files should be sorted. If not:**
```sh
sort -k1,1 -k2,2n file.bed > sorted_file.bed
```

Example:

- intrachromosomal:

            ./detectContacts_intra.py -raw chr6_5kb.RAWobserved -norm chr6_5kb.KRnorm -enh enhancers.bed -prom promoters.bed -exp chr6_5kb.KRexpected -res 5000 -out enhPromContacts_chr6_5kb.txt
      
___

Script Name: detectContacts_inter.py

      Usage: ./detectContacts_inter.py -raw <raw Hi-C file> -norm1 <1st chr KRnorm file> -norm2 <2nd chr KRnorm file> -enh <enhancers BED file> -prom <promoters BED file> -res <resolution> -out <output file name>
  
**Promoter and enhancer BED files should be sorted. If not:**
```sh
sort -k1,1 -k2,2n file.bed > sorted_file.bed
```

Example:

- interchromosomal:

            ./detectContacts_inter.py -raw chr1_16_1kb.RAWobserved -norm1 chr1_1kb.KRnorm -norm2 chr16_1kb.KRnorm -enh enhancers.bed -prom promoters.bed -res 1000 -out enhPromContacts_chr1_16_1kb.txt
      
___

Bash scripts for finding the genome wide enhancer-promoter contacts due to HSDs and performing differential gene expression anaylysis can be found in:

            /share/dennislab/sequencing/public/Rao_Huntley_2014/findAllContacts_diff_RNA/test.slurm

