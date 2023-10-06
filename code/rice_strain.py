import os

def confusion_matrix(actual, predicted, strain, region) :
    if ".gz" in actual :
        os.system(f'zcat {actual} | grep -v "^#"| cut -f1,2|uniq > actual_uniq_pos')
    else :
        os.system(f'grep -v "^#" {actural} | cut -f1,2|uniq > actual_uniq_pos')
    if ".gz" in predicted :
        os.system(f'zcat {predicted} | grep -v "^#" | cut -f1,2|uniq > predicted_uniq_pos')
    else :
        os.system(f'grep -v "^#" {predicted} | cut -f1,2|uniq > predicted_uniq_pos')

    os.system(f"sdiff {strain}_{region}  actual_uniq_pos > analysis_data")
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
    
    os.system(f"sdiff {strain}_{region}  predicted_uniq_pos > analysis_data")
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
    # program setting
    SAMTOOLS="samtools-1.17"

    #os.system("mkdir erate")
    os.system(f"{SAMTOOLS}/samtools mpileup -Bf {reference_file} {sample}_aligned.bam > {sample}_error\n");
       
    infile_name=sample+"_error"  # mileup output file load
    infile=open(infile_name,"r")

    
    outfile_name=sample+"_error_analysis"
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

    os.system(f"rm -rf {sample}_error")
    infile.close()
    outfile.close()
    
    ## database information 
    db_name=database

    snp_extract='grep -v "^#" '+db_name + " | cut -f1,2 | uniq > "+dbtype+"_uniq_pos"    
    os.system(snp_extract)
    

    sample_name=sample+"_error_analysis"
    sample_extract="cut -f1,2 "+sample_name+">"+sample+"_error_analysis_uniq_pos"     
    os.system(sample_extract)


    sdiff_exe="sdiff "+dbtype+"_uniq_pos  "+sample+"_error_analysis_uniq_pos "+ "> "+sample+"_"+dbtype+"_analysis"
    os.system(sdiff_exe)

    #rm_cmd=f"rm -rf {dbtype}_uniq_pos"
    #os.system(rm_cmd)
    rm_cmd=f"rm -rf {sample}_error_analysis_uniq_pos"
    os.system(rm_cmd)

    sdiff_extract="awk '{if(NF==4) print $0;}' "+sample+"_"+dbtype+"_analysis"+" > "+sample+"_"+dbtype+"_common"
    os.system(sdiff_extract)

    rm_cmd=f"rm -rf {sample}_{dbtype}_analysis"  
    os.system(rm_cmd)

    eff_variant="cut -f1,2 "+sample+"_"+dbtype+"_common" + " > "+sample+"_"+dbtype+"_variant_pos"
    os.system(eff_variant)
    
    rm_cmd=f"rm -rf {sample}_{dbtype}_common"  
    os.system(rm_cmd)
    
    
    sample_name=sample+"_error_analysis"
    eff_name=sample+"_"+dbtype+"_variant_pos"
    sample_infile=open(sample_name,"r")
    eff_infile=open(eff_name,"r")
   
    error_rate_file=sample+"_"+dbtype+"_error_rate" 
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
    rm_cmd=sample+"_"+dbtype+"_variant_pos"
    os.system(f"rm -rf {rm_cmd}")

    sample_infile.close()
    eff_infile.close()
    error_rate.close()

# end of error_rate()


def dbFP(purebred_variants, dbFP_database, dbFP_type) :
    indica=['RWG-006', 'RWG-013', 'RWG-022', 'RWG-030', 'RWG-047', 'RWG-056', 'RWG-060', 'RWG-068', 'RWG-073', 'RWG-109', 'RWG-112', 'RWG-121', 'RWG-122', 'RWG-123', 'RWG-124', 'RWG-125', 'RWG-126', 'RWG-131', 'RWG-021', 'RWG-071', 'RWG-072', 'RWG-048', 'RWG-238', 'RWG-119', 'RWG-118', 'RWG-120', 'RWG-067', 'RWG-070', 'RWG-116', 'RWG-036', 'RWG-049', 'RWG-061', 'RWG-064']
    japonica=['RWG-152', 'RWG-157', 'RWG-169', 'RWG-170', 'RWG-171', 'RWG-173', 'RWG-175', 'RWG-176', 'RWG-177', 'RWG-185', 'RWG-188', 'RWG-192', 'RWG-195', 'RWG-199', 'RWG-228', 'RWG-229', 'RWG-230', 'RWG-254', 'RWG-255', 'RWG-256', 'RWG-257', 'RWG-260', 'RWG-261', 'RWG-266', 'RWG-267', 'RWG-268', 'RWG-273', 'RWG-280', 'RWG-285', 'RWG-322', 'RWG-345', 'RWG-356', 'RWG-358','RWG-327','RWG-342','RWG-348','RWG-364','RWG-368']
    header=['RWG-006', 'RWG-013', 'RWG-021', 'RWG-022', 'RWG-030', 'RWG-036', 'RWG-047', 'RWG-048', 'RWG-049', 'RWG-056', 'RWG-060', 'RWG-061', 'RWG-064', 'RWG-067', 'RWG-068', 'RWG-070', 'RWG-071', 'RWG-072', 'RWG-073', 'RWG-109', 'RWG-112', 'RWG-116', 'RWG-118', 'RWG-119', 'RWG-120', 'RWG-121', 'RWG-122', 'RWG-123', 'RWG-124', 'RWG-125', 'RWG-126', 'RWG-131', 'RWG-152', 'RWG-157', 'RWG-169', 'RWG-170', 'RWG-171', 'RWG-173', 'RWG-175', 'RWG-176', 'RWG-177', 'RWG-185', 'RWG-188', 'RWG-192', 'RWG-195', 'RWG-199', 'RWG-228', 'RWG-229', 'RWG-230', 'RWG-238', 'RWG-254', 'RWG-255', 'RWG-256', 'RWG-257', 'RWG-260', 'RWG-261', 'RWG-266', 'RWG-267', 'RWG-268', 'RWG-273', 'RWG-280', 'RWG-285', 'RWG-322', 'RWG-327', 'RWG-342', 'RWG-345', 'RWG-348', 'RWG-356', 'RWG-358', 'RWG-364', 'RWG-368']


    strain=[]
    for i in japonica :
        strain.append(header.index(i))
  

    for i in indica :
        strain.append(header.index(i))
    
    if ".gz" in purebred_variants :
        cmd_line=f"gzip -d {purebred_variants}"
        os.system(cmd_line)

    file_name=purebred_variants.split(".gz")[0]
    infile=open(file_name,"r")

    out_file_name=dbFP_database+"_junk"
    outfile=open(out_file_name,"w")
    
    row=infile.readline()
    while row[0]=="#":
        row=infile.readline()

    remove_set={"0/0","0|0","./.",".|."}
    
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
     
    if dbFP_type=="japonica" :
        cmd_line="awk '{if($5==2) printf(\"%s\\t%s\\n\",$1,$2);}' " + f"{out_file_name}" +" >" +f"{dbFP_database}"
        os.system(f"{cmd_line}")
    elif dbFP_type=="indica" :
        cmd_line="awk '{if($5==1) printf(\"%s\\t%s\\n\",$1,$2);}' " + f"{out_file_name}" +" >" +f"{dbFP_database}"
        os.system(f"{cmd_line}")
    else :
        print("dbFP_type error")
    
    cmd_line=f"rm -rf {out_file_name}"
    os.system(cmd_line)




def dbFP_confusion_matrix(actual, predicted,strain,region,dbFP) :
    if ".gz" in actual :
        os.system(f'zcat {actual} | grep -v "^#"| cut -f1,2|uniq > actual_uniq_pos')
    else :
        os.system(f'grep -v "^#" {actural} | cut -f1,2|uniq > actual_uniq_pos')
    if ".gz" in predicted :
        os.system(f'zcat {predicted} | grep -v "^#" | cut -f1,2|uniq > predicted_uniq_pos')
    else :
        os.system(f'grep -v "^#" {predicted} | cut -f1,2|uniq > predicted_uniq_pos')

    os.system(f"sdiff {strain}_{region}  actual_uniq_pos > analysis_data")
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
    
    os.system(f"sdiff {strain}_{region}  predicted_uniq_pos > analysis_data")
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


    os.system(f"sdiff {dbFP} FP> analysis_data")
    os.system("awk '{if(NF==4) print $0;}' analysis_data > FP_Yes_junk")
    cmd_line='{printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"awk '{cmd_line}'  FP_Yes_junk > FP_Yes")
    os.system("rm FP_Yes_junk ")

    FP_Yes=int(os.popen("wc -l FP_Yes").readline().split()[0])

    ## confusion matrix
    TP=int(os.popen("wc -l TP").readline().split()[0])
    FN=int(os.popen("wc -l FN").readline().split()[0])
    FP1=int(os.popen("wc -l FP").readline().split()[0])
    FP=FP1-FP_Yes
    TN=int(os.popen("wc -l TN").readline().split()[0])
    print(f"TP:{TP} FN:{FN} FP:{FP} TN:{TN}")

    
    Precision=TP/(TP+FP)
    Recall=TP/(TP+FN)
    F1= 2*(Recall*Precision)/(Recall+Precision)
    print(f"Precision : {Precision:.2f}")
    print(f"Recall : {Recall:.2f}")
    print(f"F1-score : {F1:.2f}")



def coding_noncoding(GFF,reference, strain) :
    cmd_line="awk '{if($3==\"gene\" || $3==\"CDS\") print $0;}' "
    cmd_line=cmd_line+f"{GFF}  > rice_gff3_junk"
    os.system(cmd_line)

    infile=open("rice_gff3_junk","r")
    outfile=open("step1.txt","w")
    gene_dict={}
    cds_dict={}

    while True :
        row=infile.readline()
        if row==""  :
            break
        row_list=row.strip().split('\t')
        
        if row_list[2]=="gene":
            gene_name=row_list[8].strip().split(';')[0].split('=')[1].split(':')[1]

            if gene_name in gene_dict :
                if row_list[0] in ["1","2","3","4","5","6","7","8","9"] :
                    gene_dict[gene_name]=gene_dict[gene_name]+"chr0"+row_list[0]+"\t"+row_list[2]+"\t"+row_list[3]+"\t"+row_list[4]+"\t"+"CDS"
                else :
                    gene_dict[gene_name]=gene_dict[gene_name]+"chr"+row_list[0]+"\t"+row_list[2]+"\t"+row_list[3]+"\t"+row_list[4]+"\t"+"CDS"
            else :
                if row_list[0] in ["1","2","3","4","5","6","7","8","9"] :
                    gene_dict[gene_name]="chr0"+row_list[0]+"\t"+row_list[2]+"\t"+row_list[3]+"\t"+row_list[4]+"\t"+"CDS"
                else :
                    gene_dict[gene_name]="chr"+row_list[0]+"\t"+row_list[2]+"\t"+row_list[3]+"\t"+row_list[4]+"\t"+"CDS"
        elif row_list[2]=="CDS" :
            cds_name=row_list[8].split(";")[0].split("=")[1].split(":")[1]
            if cds_name in cds_dict :
                cds_dict[cds_name]=cds_dict[cds_name]+row_list[3]+"\t"+row_list[4]+"\t"
            else :
                cds_dict[cds_name]=row_list[3]+"\t"+row_list[4]+"\t"

    final_dict={}
    for key in gene_dict :
        if gene_dict[key].split('\t')[0] in ["chr01","chr02","chr03","chr04","chr05","chr06","chr07","chr08","chr09","chr10","chr11","chr12"] :
             final_dict[key]=gene_dict[key]
    for key, value in cds_dict.items() :
        key_check=key.split("-")
        key_con=key_check[0].replace("t","g")
        if key_con in final_dict :
            final_dict[key_con]=final_dict[key_con]+"\t"+key+"\t"+value

    for key,value in final_dict.items() :
        temp=key+"\t"+value+"\n"
        outfile.write(temp)

    os.system("rm -rf rice_gff3_junk")
    outfile.close()
    infile.close()

    os.system("awk '{if(NF >7) print $0;}' step1.txt  > step2.txt")


    import sys

    infile=open("step2.txt","r")
    outfile=open("step3.txt","w")

    #for _ in range(100) :
    while True :
        row=infile.readline()
        if row==""  :
            break
        n = row.count("-")
        if n<=1 :
            pr=row.strip()+"\n"
            outfile.write(pr) 
        elif n==2 :
           row_list=row.strip().split("Os")
           pr1="Os"+row_list[1]+"Os"+row_list[2]+"\n"
           pr2="Os"+row_list[1]+"Os"+row_list[3]+"\n"
           outfile.write(pr1)  
           outfile.write(pr2)  
    
        elif n==3 :
           row_list=row.strip().split("Os")
           pr1="Os"+row_list[1]+"Os"+row_list[2]+"\n"
           pr2="Os"+row_list[1]+"Os"+row_list[3]+"\n"
           pr3="Os"+row_list[1]+"Os"+row_list[4]+"\n"
           outfile.write(pr1)  
           outfile.write(pr2)  
           outfile.write(pr3)  
    

        elif n==4 :
           row_list=row.strip().split("Os")
           pr1="Os"+row_list[1]+"Os"+row_list[2]+"\n"
           pr2="Os"+row_list[1]+"Os"+row_list[3]+"\n"
           pr3="Os"+row_list[1]+"Os"+row_list[4]+"\n"
           pr4="Os"+row_list[1]+"Os"+row_list[5]+"\n"
           outfile.write(pr1)  
           outfile.write(pr2)  
           outfile.write(pr3)  
           outfile.write(pr4)  
    
    
    os.system("rm -rf step2.txt")

    infile=open("step3.txt","r")  
    outfile=open("coding_region","w")
    
    while True :
        gene=infile.readline().strip()

        if gene=="":
            break
        gene_list=gene.split('\t')
        for i in range(7, len(gene_list)-1,2) :
            start=int(gene_list[i])
            end=int(gene_list[i+1])
            for k in range(start, end+1) :
                outfile.write(f"{gene_list[1]}\t{k}\n")

    outfile.close()
    infile.close()
    os.system("rm -rf step3.txt")
    os.system(f"cat coding_region | sort  -k1,1 -k2,2n | uniq  > {strain}_coding_region")
    os.system("rm -rf coding_region")

    from Bio import SeqIO
    
    seq_infile=SeqIO.parse(reference,"fasta")  ## rice_sequence_info
    file_name=f"{strain}_sequence_info"
    outfile=open(file_name,"w")

    seq_dict={}
    for s in seq_infile :
       seq_dict[s.id]=s.seq

    for i in seq_dict :
        for k in range(1,len(seq_dict[i])+1) :
            pr=i+"\t"+str(k)+"\n"
            outfile.write(pr)
    outfile.close()

    cmd1='{if(NF==3) printf("%s\\t%s\\n",$1,$2);'
    cmd2='else if(NF==5) printf("%s\\t%s\\n",$1,$2);}'
    os.system(f"sdiff {strain}_sequence_info  {strain}_coding_region  > analysis_data")
    os.system('grep -e "|" -e "<" analysis_data > noncoding_region')
    os.system(f"awk '{cmd1} {cmd2} ' noncoding_region > {strain}_noncoding_region")
    os.system("rm noncoding_region")
    os.system("rm analysis_data")

