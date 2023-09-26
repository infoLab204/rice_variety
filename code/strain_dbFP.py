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
# end of confusion_matrix()


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


    sdiff_exe="sdiff "+dbtype+"_uniq_pos  "+"/erate/"+sample+"_error_analysis_uniq_pos "+ "> /erate/"+sample+"_"+dbtype+"_analysis"
    os.system(sdiff_exe)

    #rm_cmd=f"rm -rf {dbtype}_uniq_pos"
    #os.system(rm_cmd)
    rm_cmd=f"rm -rf erate/{sample}_error_analysis_uniq_pos"
    os.system(rm_cmd)

    sdiff_extract="awk '{if(NF==4) print $0;}' "+"erate/"+sample+"_"+dbtype+"_analysis"+" > "+"erate/"+sample+"_"+dbtype+"_common"
    os.system(sdiff_extract)

    rm_cmd=f"rm -rf erate/{sample}_{dbtype}_analysis"  
    print(rm_cmd)
    #os.system(rm_cmd)

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
    print(eff_num, mismatch_num, (mismatch_num-eff_num)/mismatch_num)
    error_rate.write(f"{sample}\t{(mismatch_num-eff_num)/mismatch_num}")


    rm_cmd=f"rm -rf {sample_name}"
    os.system(rm_cmd)
    rm_cmd="erate/"+sample+"_"+dbtype+"_variant_pos"
    os.system(rm_cmd)

    sample_infile.close()
    eff_infile.close()
    error_rate.close()

# end of error_rate()


