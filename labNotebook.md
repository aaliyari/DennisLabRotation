# Dennis Lab Rotation

Start date: Monday February 13, 2017  
End date: Friday March 17, 2017

___

## Week 1:

- [x] Warm up!


      - Get a sample list of promoters from [FANTOM](http://pressto.binf.ku.dk/): all chr6 promoters - BED format
      - Some HSD enhancers on chr6 (DUSP22) from Paulina
      - Hi-C matrix from [Rao & Huntley et al. 2014](http://www.cell.com/abstract/S0092-8674(14)01497-4) (5kb resolution for now)
        GEO accesion number: [GSE63525](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE63525)     
  
  
- [x] write a python script to normalize the Hi-C matrix
- normalization method used: KRnorm (used in Rao & Huntley et al. 2014)

Each entry of M_ij of the raw Hi-C matrix should be divided by its corresponding values in the normalization vector file (*.KRnorm). For details, see this [readme](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE63525&format=file&file=GSE63525%5FGM12878%5Fcombined%5FREADME%2Ertf)

- function name: normalize_HiC(HiC_raw_file, KRnorm_file, resolution)
      
- [x] find the number of contacts between promoters and enhancers using the normalized Hi-C matrix
```sh
sort -k1,1n -k2,2n normalized_HiC.txt > sorted_normalized_HiC.txt
```

        output format: enhancer BED + promoter BED + O/E + HiC line
        chr   start   end   chr   start   end   O/E   bin_i   bin_j   no. of contacts
     
## Week 2

- [ ] 

## Week 3
### Primer Design
# remember to pick the reverse strand
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
                                                                
