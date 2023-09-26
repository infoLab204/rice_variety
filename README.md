# dbFP: A method of identifying false positives in the strain-specific variant calling of rice    
### Sunhee Kim and Chang-Yong Lee    
The dbFP represents Python scripts that analyze the variants called using different variant calling models to propose a method for finding false positive variants using purebred and non-purebred samples of two strains in rice.    

We compared the performance of different variant calling models by constructing confusion matrices using the sets of variants called by different models. The constructed confusion matrices were evaluated in three different metrics: precision, recall, and F1 score. Based on the results of the performance comparison, we proposed a method to construct the dbFP, which is a collection of false positive variants. We showed that the dbFP identified the false positives from the called variants. The validity of the proposed dbFP was tested against the dbSNP and non-negligible false positives were found. We have provided the Python scripts with datasets for the readers to reproduce the results discussed in the manuscript.    

## Data sets
1.	Reference sequences of Japonica and Indica
    - Nipponbare reference genome (IRGSP 1.0) : https://www.ebi.ac.uk/ena/browser/view/GCA_001433935.1
    - Indica reference genome (ASM465v1) : https://www.ebi.ac.uk/ena/browser/view/GCA_000004655.2
2.	The dbSNP of Japonica and Indica
    - Japonica dbSNP : https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-57/variation/vcf/oryza_sativa/oryza_sativa.vcf.gz
    -	indica dbSNP: https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-57/variation/vcf/oryza_indica/oryza_indica.vcf.gz
3. 	The purebred samples of Japonica and Indica
4.	The non-purebred samples of Japonica and Indica
5.	VCF files


## Python scripts for analyzing variant calling results
1. Python scripts for constructing the confusion matrix and evaluating performance metrics    
    ```
    strain_dbFP.confusion_matrix( “actual sample variants”, “predicted sample variants”)
    ```
   (eg) strain_dbFP.confusion_matrix(“japonica_variants.vcf”, “mixed_indica25_variants.vcf”)

2. Python scripts for constructing the dbFP and identifying false positives    
    ```
    strain_dbFP.dfFP( “pure samples variants”)
    ```
    (eg) strain_dbFP.dfFP (“pureindica_purejaponica_variants vcf”)

3. Python scripts for estimating error rates of dbSNP     
    ```
    strain_dbFP.error_rate( “sample_name”, “reference”, “name of database”)
    ```
    (eg) strain_dbFP.error_rate("RWG-006","IRGSP-1.0_genome.fasta","oryza_sativa.vcf")
