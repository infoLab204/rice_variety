import os
import sys


## The program and working directory must be set.

## program setting
BWA="bwa-mem2-2.2.1"
SAMTOOLS="samtools-1.17"
PICARD="picard.jar"
GATK="gatk-package-4.3.0.0-local.jar"


## reference sequence
ref="IRGSP-1.0_genome.fasta "

## working dictionary setting
root_dir="rice"
fastq="FASTQ"
alignment="alignment"
db="db"
recalibration="recalibration"
variants="variants"

samp_name=sys.argv[1]

## Map to Reference
print(f'{BWA}/bwa-mem2 mem -M -t 16 -R "@RG\\tID:{samp_name}\\tLB:{samp_name}\\tSM:{samp_name}\\tPL:ILLUMINA" {ref} {root_dir}/{fastq}/{samp_name}_1.fq.gz {root_dir}/{fastq}/{samp_name}_2.fq.gz > {root_dir}/{alignment}/temp/{samp_name}.mapped.sam ')

## Samtools : SAM to BAM
print(f"{SAMTOOLS}/samtools view -Sb {root_dir}/{alignment}/temp/{samp_name}.mapped.sam > {root_dir}/{alignment}/temp/{samp_name}.mapped.bam")
print(f"rm -rf  {root_dir}/{alignment}/temp/{samp_name}.mapped.sam")

## Samtools sort : Make Sorted BAM
print(f"{SAMTOOLS}/samtools sort -n  -o {root_dir}/{alignment}/temp/{samp_name}.mapped_sored.bam {root_dir}/{alignment}/temp/{samp_name}.mapped.bam")
print(f"rm -rf {root_dir}/{alignment}/temp/{samp_name}.mapped.bam")
print(f"{SAMTOOLS}/samtools fixmate -m  {root_dir}/{alignment}/temp/{samp_name}.mapped_sored.bam  {root_dir}/{alignment}/temp/{samp_name}.fixmated.bam")
print(f"rm -rf {root_dir}/{alignment}/temp/{samp_name}.mapped_sored.bam")
print(f"{SAMTOOLS}/samtools sort -o  {root_dir}/{alignment}/temp/{samp_name}.fixmated.sored.bam  {root_dir}/{alignment}/temp/{samp_name}.fixmated.bam")
print(f"rm -rf {root_dir}/{alignment}/temp/{samp_name}.fixmated.bam")
print(f"{SAMTOOLS}/samtools index  {root_dir}/{alignment}/temp/{samp_name}.fixmated.sored.bam")

## Mark Duplicate : picard tools
print(f"java -jar {PICARD} MarkDuplicates I={root_dir}/{alignment}/temp/{samp_name}.fixmated.sored.bam O={root_dir}/{alignment}/{samp_name}_aligned.bam M={root_dir}/{alignment}/temp/{samp_name}.markdup.metrics.txt")
print(f"rm -rf  {root_dir}/{alignment}/temp/{samp_name}.fixmated.sored.bam ")
 
## Samtools index : Make BAM index
print(f"{SAMTOOLS}/samtools index {root_dir}/{alignment}/{samp_name}_aligned.bam")

## GATK BaseRecalibrator
print(f"java -jar {GATK} BaseRecalibrator -R {ref} -I {root_dir}/{alignment}/{samp_name}_aligned.bam  --known-sites {root_dir}/{db}/oryza_sativa_dbSNP_20230103.vcf.gz  -O {root_dir}/{recalibration}/temp/{samp_name}_recalibrated.table")
print(f"java -jar {GATK} ApplyBQSR  -R {ref} -I {root_dir}/{alignment}/{samp_name}_aligned.bam --bqsr-recal-file {root_dir}/{recalibration}/temp/{samp_name}_recalibrated.table -O {root_dir}/{recalibration}/{samp_name}_recalibrated.bam")
   
## GATK HaplotypeCaller
print(f"java -jar {GATK} HaplotypeCaller -R {ref} -I {root_dir}/{recalibration}/{samp_name}_recalibrated.bam -O {root_dir}/{variants}/temp/{samp_name}_recal.vcf.gz -ERC GVCF")

## GATK GenotypeGVCF
print(f"java -jar {GATK}  GenotypeGVCFs -R {ref}  -V {root_dir}/{variants}/temp/{samp_name}_recal.vcf.gz -O {root_dir}/{variants}/{samp_name}_variant_calling.vcf.gz\n");

