# Rice_variety : A method of identifying false positives in the variety-specific variant calling of rice    
### Sunhee Kim and Chang-Yong Lee    
The rice_variety represents Python scripts that analyze the variants called using different variant calling models to propose a method for finding false positive variants using typical and introgressed samples of two strains in rice.    

We compared the performance of different variant calling models by constructing confusion matrices using the sets of variants called by different models. The constructed confusion matrices were evaluated in three different metrics: precision, recall, and F1 score. Based on the results of the performance comparison, we proposed a method to construct the dbFP, which is a collection of false positive variants. We showed that the dbFP identified the false positives from the called variants. The validity of the proposed dbFP was tested against the dbSNP and non-negligible false positives were found. We have provided the Python scripts with datasets for the readers to reproduce the results discussed in the manuscript.    

## Data sets
1.	Reference sequences of Japonica and Indica
    - Nipponbare reference genome (IRGSP 1.0) : https://www.ebi.ac.uk/ena/browser/view/GCA_001433935.1
    - Indica reference genome (ASM465v1) : https://www.ebi.ac.uk/ena/browser/view/GCA_000004655.2
2.	The dbSNP of Japonica and Indica
    - Japonica dbSNP : https://ftp.ebi.ac.uk/pub/databases/eva/rs_releases/release_6/by_species/oryza_sativa/IRGSP1.0/    
    - Indica dbSNP: https://ftp.ebi.ac.uk/pub/databases/eva/rs_releases/release_6/by_species/oryza_sativa/GCA_000005425.2    
3. 	The typical samples of Japonica and Indica, or the introgressed samples of Japonica and Indica
    - https://www.ebi.ac.uk/biosamples/samples/SAMEG4750728
4. Gene annotation
    - Japonica gene annotation : https://rapdb.dna.affrc.go.jp/download/archive/irgsp1/IRGSP-1.0_representative_2024-07-12.tar.gz    
    - Indica gene annotation  : https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-59/gff3/oryza_indica/Oryza_indica.ASM465v1.59.chr.gff3.gz    
6.	VCF files
    - The result of variants calling with the Japonica reference : https://doi.org/10.5281/zenodo.8381893
    - The result of variants calling with the Indica reference : https://doi.org/10.5281/zenodo.8383314

  
## Python scripts for analyzing variant calling results
1. Download “rice_variety.py” module from the github repository and import the module
    ```
    import rice_variety
    ```
3. Python scripts for constructing the confusion matrix and evaluating performance metrics    
    ```
   rice_variety.confusion_matrix( “actual sample variants”, “predicted sample variants”, “strain_type”, “region_type”)
    ```
    - actual sample variants : actual variant calling file
    - predicted sample variants: predicted variant calling file
    - strain_type : indica or japonica
    - region_type : coding region or noncoding region

   (eg) rice_variety.confusion_matrix(“rice_Nip_jadbSNP_purebred_japonica.vcf”, “rice_Nip_jadbSNP_indica50_mixed.vcf”,”japonica”, ”coding_region”)
<br><br><br>
4. Python scripts for constructing the dbFP and identifying false positives    
    ```
   rice_variety.dbFP( “pure samples variants”,"dbFP_output","strain_type")
    ```
    - pure samples variants: purebred indica and purebred japonica variant calling file
    - dbFP_output: indica_dbFP or japonica_dbFP
    - strain_type : indica or japonica

    (eg) rice_variety.dbFP (“rice_Nip_jadbSNP_purebred_indica_purebred_japonica.vcf.gz”,"dbFP_japonica", "japonica")
<br><br><br>

5. Python scripts for constructing the confusion matrix using dbFP and evaluating performance metrics
    ```
    rice_variety.dbFP_confusion_matrix(“actual sample variants”, “predicted sample variants”, “strain_type”, “region_type”, “dbFP”)
    ```
    - actual sample variants : actual variant calling file
    - predicted sample variants: predicted variant calling file
    - strain_type : indica or japonica
    - region_type : coding region or noncoding region
    - dbFP : japonica_dbFP or indica_dbFP
  
    (eg) rice_variety.dbFP_confusion_matrix(“rice_Nip_jadbSNP_purebred_japonica.vcf”, “rice_Nip_jadbSNP_indica50_mixed.vcf”, ”japonica”, ”coding_region”,“japonica_dbFP”)
<br><br><br>

6.  Python scripts for constructing the coding region and noncoding region
    ```
    rice_variety.coding_noncoding(“GFF_file”, “reference”, ”strain_type”)
    ```
    - GFF_file : japonica or indica annotation file
    - reference : japonica or indica reference 
    - strain_type : indica or japonica
  
    (eg) rice_variety.coding_noncoding (“Oryza_sativa.IRGSP-1.0.56.gff3”, "IRGSP-1.0_genome.fasta",“japonica”)
<br><br><br>
  
7. Python scripts for estimating error rates of dbSNP     
    ```
   rice_variety.error_rate( “sample_name”, “reference”, “name of database”,”strain_type”)
    ```
    - sample_name : sample
    - reference : japonica or indica reference 
    - name of database : indica or japonica of dbSNP
    - strain_type : indica or japonica

    (eg) rice_variety.error_rate("RWG-006","IRGSP-1.0_genome.fasta","oryza_sativa.vcf","japonica")
