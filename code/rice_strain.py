import os

def confusion_matrix(actual, predicted) :
    os.system(f'zcat {actual} | grep -v "^#"| cut -f1,2|uniq > actual_uniq_pos')
    os.system(f'zcat {predicted} | grep -v "^#" | cut -f1,2|uniq > predicted_uniq_pos')

    os.system("sdiff japonica_coding_region  actual_uniq_pos > analysis_data")
    os.system("awk '{if(NF==4) print $0;}' analysis_data > Real_Yes_junk")
    cmd_line='{printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"awk '{cmd_line} ' Real_Yes_junk > Real_Yes")
    os.system("rm Real_Yes_junk")
    os.system('grep -e "|" -e "<" analysis_data > Real_onlycoding_junk')

    cmd1='{if(NF==3) printf("%s\\t%s\\n",$1,$2);'
    cmd2='else if(NF==5) printf("%s\\t%s\\n",$1,$2);}'
    cmd3='{if(NF==3) printf("%s\\t%s\\n",$2,$3);'
    cmd4='else if(NF==5) printf("%s\\t%s\\n",$4,$5);}'
    os.system(f"awk '{cmd1} {cmd2} ' Real_onlycoding_junk > Real_onlycoding")
    os.system("rm Real_onlycoding_junk")
    os.system("rm analysis_data")
    
    os.system("sdiff japonica_coding_region  predicted_uniq_pos > analysis_data")
    os.system("awk '{if(NF==4) print $0;}' analysis_data > predicted_Yes_junk")
    cmd_line='{printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"awk '{cmd_line}'  predicted_Yes_junk > predicted_Yes")
    os.system("rm predicted_Yes_junk")
    os.system('grep -e "|" -e "<" analysis_data > predicted_onlycoding_junk')
    os.system(f"awk '{cmd1} {cmd2} ' predicted_onlycoding_junk > predicted_onlycoding")
    os.system("rm predicted_onlycoding_junk")
    os.system("rm analysis_data")

    os.system("sdiff Real_Yes  predicted_Yes  > analysis_data")
    os.system("awk '{if(NF==4) print $0;}' analysis_data > TP_junk")
    cmd_line='{printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"awk '{cmd_line}'  TP_junk > TP")
    os.system("rm TP_junk ")
    os.system('grep -e "|" -e "<" analysis_data > FN_junk')
    os.system(f"awk '{cmd1} {cmd2}' FN_junk > FN")
    os.system("rm FN_junk")
    os.system('grep -e "|" -e ">" analysis_data > FP_junk')
    os.system(f"awk '{cmd3} {cmd4} ' FP_junk > FP")
    os.system("rm FP_junk")
    os.system("rm analysis_data")

    os.system("sdiff Real_onlycoding  predicted_onlycoding  > analysis_data")
    os.system("awk '{if(NF==4) print $0;}' analysis_data > TN_junk")

    cmd_line='{printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"awk '{cmd_line} ' TN_junk > TN")
    os.system("rm TN_junk")

    ## confusion matrix
    TP=int(os.popen("wc -l TP").readline().split()[0])
    FN=int(os.popen("wc -l FN").readline().split()[0])
    FP=int(os.popen("wc -l FP").readline().split()[0])
    TN=int(os.popen("wc -l TN").readline().split()[0])
    print(f"TP:{TP} FN:{FN} FP:{FP} TN:{TN}")

    
    Precision=TP/(TP+FP)
    Recall=TP/(TP+FN)
    F1= 2*(Recall*Precision)/(Recall+Precision)
    print(f"Precision : {Precision:.2f}")
    print(f"Recall : {Recall:.2f}")
    print(f"F1-score : {F1:.2f}")

def error_rate(sample, reference_file, database, dbtype) :
    # program
    SAMTOOLS="/home/king/tools/samtools-1.17"

    os.system("mkdir erate")
    os.system(f"{SAMTOOLS}/samtools mpileup -Bf {reference_file} {sample}_aligned.bam > erate/{sample}_error\n");
       
    infile_name="erate/"+sample+"_error"  # mileup output file load
    infile=open(infile_name,"r")

    
    outfile_name="erate/"+sample+"_error_analysis"
    outfile=open(outfile_name,"w")

    line=infile.readline()
    line_list=line.strip().split("\t")

    while line !="" :
        if line_list[3]!="0" :
            d=line_list[4].find("^")   # start of read segment 
            while d !=-1 :
                line_list[4]=line_list[4].replace(line_list[4][d:d+2],"")
                d=line_list[4].find("^")

            line_list[4]=line_list[4].replace("$","")   # end of a read segment
            line_list[4]=line_list[4].replace("*","")   #
            line_list[4]=line_list[4].replace(".","")   # match to the refernece base on the forward strand
            line_list[4]=line_list[4].replace(",","")   # match to the reference base on the reverse strand

            if line_list[4]!="" :
                indelnum=0
                indelnum=indelnum+line_list[4].count("+")   # insertion from the reference
                indelnum=indelnum+line_list[4].count("-")   # deletion from the reference
                tmpgeno=line_list[4]
                i=tmpgeno.find("+")
                while i!=-1 :
                    if tmpgeno[i+1:i+3].isdigit()==True :
                        n=int(tmpgeno[i+1:i+3])
                        tmpgeno=tmpgeno.replace(tmpgeno[i:i+3+n],"")
                    else :
                        n=int(tmpgeno[i+1:i+2])
                        tmpgeno=tmpgeno.replace(tmpgeno[i:i+2+n],"")
                    i=tmpgeno.find("+")
                i=tmpgeno.find("-")
                while i!=-1 :
                    if tmpgeno[i+1:i+3].isdigit()==True :
                        n=int(tmpgeno[i+1:i+3])
                        tmpgeno=tmpgeno.replace(tmpgeno[i:i+3+n],"")         
                    else :
                        n=int(tmpgeno[i+1:i+2])
                        tmpgeno=tmpgeno.replace(tmpgeno[i:i+2+n],"")
                    i=tmpgeno.find("-")           
                mnum=len(tmpgeno)+indelnum
                outfile.write(f"{line_list[0]}\t{line_list[1]}\t{line_list[2]}\t{line_list[3]}\t{mnum}\t{line_list[4]}\n")
        line=infile.readline()
        line_list=line.strip().split("\t")

    os.system(f"rm -rf erate/{sample}_error")
    infile.close()
    outfile.close()
    
    ## database information 
    db_name=database

    snp_extract='grep -v "^#" '+db_name + " | cut -f1,2 | uniq > "+dbtype+"_uniq_pos"    
    os.system(snp_extract)
    

    sample_name="erate/"+sample+"_error_analysis"
    sample_extract="cut -f1,2 "+sample_name+">"+"erate/"+sample+"_error_analysis_uniq_pos"     
    os.system(sample_extract)


    sdiff_exe="sdiff "+dbtype+"_uniq_pos  "+"erate/"+sample+"_error_analysis_uniq_pos "+ "> erate/"+sample+"_"+dbtype+"_analysis"
    os.system(sdiff_exe)

    #rm_cmd=f"rm -rf {dbtype}_uniq_pos"
    #os.system(rm_cmd)
    rm_cmd=f"rm -rf erate/{sample}_error_analysis_uniq_pos"
    os.system(rm_cmd)

    sdiff_extract="awk '{if(NF==4) print $0;}' "+"erate/"+sample+"_"+dbtype+"_analysis"+" > "+"erate/"+sample+"_"+dbtype+"_common"
    os.system(sdiff_extract)

    rm_cmd=f"rm -rf erate/{sample}_{dbtype}_analysis"  
    os.system(rm_cmd)

    eff_variant="cut -f1,2 "+"erate/"+sample+"_"+dbtype+"_common" + " > "+ "erate/"+sample+"_"+dbtype+"_variant_pos"
    os.system(eff_variant)
    
    rm_cmd=f"rm -rf erate/{sample}_{dbtype}_common"  
    os.system(rm_cmd)
    
    
    sample_name="erate/"+sample+"_error_analysis"
    eff_name="erate/"+sample+"_"+dbtype+"_variant_pos"
    sample_infile=open(sample_name,"r")
    eff_infile=open(eff_name,"r")
   
    error_rate_file="erate/"+sample+"_"+dbtype+"_error_rate" 
    error_rate=open(error_rate_file,"w")

    eff_num=0
    mismatch_num=0

    while True :
        eff_base=eff_infile.readline()

        if eff_base=="" :
            break

        eff_list=eff_base.strip().split("\t")
        
        while True :
            base_sample=sample_infile.readline()

            if base_sample=="" :
                break

            base_list=base_sample.split('\t') 

            mismatch_num=mismatch_num+int(base_list[4])

            if eff_list[0]==base_list[0] and eff_list[1]==base_list[1] :
                eff_num=eff_num+int(base_list[4])
                break

    error_rate.write(f"{sample}\t{(mismatch_num-eff_num)/mismatch_num}")


    rm_cmd=f"rm -rf {sample_name}"
    os.system(rm_cmd)
    rm_cmd="erate/"+sample+"_"+dbtype+"_variant_pos"
    os.system(f"rm -rf {rm_cmd}")

    sample_infile.close()
    eff_infile.close()
    error_rate.close()

# end of error_rate()


def dbFP(purebred_variants,dbFP_database) :
    indica=['RWG-006', 'RWG-013', 'RWG-022', 'RWG-030', 'RWG-047', 'RWG-056', 'RWG-060', 'RWG-068', 'RWG-073', 'RWG-109', 'RWG-112', 'RWG-121', 'RWG-122', 'RWG-123', 'RWG-124', 'RWG-125', 'RWG-126', 'RWG-131', 'RWG-021', 'RWG-071', 'RWG-072', 'RWG-048', 'RWG-238', 'RWG-119', 'RWG-118', 'RWG-120', 'RWG-067', 'RWG-070', 'RWG-116', 'RWG-036', 'RWG-049', 'RWG-061', 'RWG-064']
    japonica=['RWG-152', 'RWG-157', 'RWG-169', 'RWG-170', 'RWG-171', 'RWG-173', 'RWG-175', 'RWG-176', 'RWG-177', 'RWG-185', 'RWG-188', 'RWG-192', 'RWG-195', 'RWG-199', 'RWG-228', 'RWG-229', 'RWG-230', 'RWG-254', 'RWG-255', 'RWG-256', 'RWG-257', 'RWG-260', 'RWG-261', 'RWG-266', 'RWG-267', 'RWG-268', 'RWG-273', 'RWG-280', 'RWG-285', 'RWG-322', 'RWG-345', 'RWG-356', 'RWG-358','RWG-327','RWG-342','RWG-348','RWG-364','RWG-368']
    header=['RWG-006', 'RWG-013', 'RWG-021', 'RWG-022', 'RWG-030', 'RWG-036', 'RWG-047', 'RWG-048', 'RWG-049', 'RWG-056', 'RWG-060', 'RWG-061', 'RWG-064', 'RWG-067', 'RWG-068', 'RWG-070', 'RWG-071', 'RWG-072', 'RWG-073', 'RWG-109', 'RWG-112', 'RWG-116', 'RWG-118', 'RWG-119', 'RWG-120', 'RWG-121', 'RWG-122', 'RWG-123', 'RWG-124', 'RWG-125', 'RWG-126', 'RWG-131', 'RWG-152', 'RWG-157', 'RWG-169', 'RWG-170', 'RWG-171', 'RWG-173', 'RWG-175', 'RWG-176', 'RWG-177', 'RWG-185', 'RWG-188', 'RWG-192', 'RWG-195', 'RWG-199', 'RWG-228', 'RWG-229', 'RWG-230', 'RWG-238', 'RWG-254', 'RWG-255', 'RWG-256', 'RWG-257', 'RWG-260', 'RWG-261', 'RWG-266', 'RWG-267', 'RWG-268', 'RWG-273', 'RWG-280', 'RWG-285', 'RWG-322', 'RWG-327', 'RWG-342', 'RWG-345', 'RWG-348', 'RWG-356', 'RWG-358', 'RWG-364', 'RWG-368']


    strain=[]
    for i in japonica :
        strain.append(header.index(i))
  

    for i in indica :
        strain.append(header.index(i))

    infile=open(purebred_variants,"r")
    outfile=open(dbFP_database,"w")

    row=infile.readline()
    while row[0]=="#":
        row=infile.readline()

    remove_set={"0/0","0|0","./.",".|."}
    print(row)
    #for _ in range(10) :

    while True :
        if row =="" :
            break

        row_list=row.split("\t")
        genotype=[]
        for i in row_list[9:] :
            genotype.append(i.split(":")[0])

        variants=[]
        for idx in strain :
            variants.append(genotype[idx])
        japonica_variants=list(variants[:len(japonica)])
        indica_variants=list(variants[len(japonica):])
    
        japonica_variants=[i for i in japonica_variants if i not in remove_set]
        indica_variants=[i for i in indica_variants if i not in remove_set]
    
        if len(japonica_variants) >=1 and len(indica_variants)>=1 :
            variants_check=3
        elif len(japonica_variants)>=1 and len(indica_variants)==0 :
            variants_check=1
        elif len(japonica_variants)==0 and len(indica_variants)>=1 :
            variants_check=2
        else :
            variants_check=4

        outfile.write(row_list[0]+"\t"+row_list[1]+"\t"+row_list[3]+"\t"+row_list[4]+"\t"+str(variants_check)+"\n") 
        row=infile.readline()

