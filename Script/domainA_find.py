# -*- encoding: utf-8 -*-
'''
@File    :   domainA_infine.py
@Time    :   2024/05/09 16:13:02
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

# 该脚本用于对多物种的蛋白质(domain_Architectures)进行去重,并给domain_Architectures进行编号.输入文件是scan_domainA脚本的输出文件
import argparse


def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -o output_file")
    parser.add_argument('-i','--input',help='输入文件,hmmscan后的结构')
    parser.add_argument('-o','--output',help='输出文件,包括蛋白和domain组成')
    args = parser.parse_args()
    
    return args


def domainA_infine(input_file,output_file):
    with open(input_file,'r') as file:
        lines = file.readlines()

    with open(output_file,"w") as outfile:    
        DoA__dictionary={}
        start=1000000
        for line in lines:
            parts = line.strip().split("\t")
            protein_name = parts[0]
            domainA = parts[1]
            if domainA in DoA__dictionary:
                pass
            else:
                DoA__dictionary[domainA]="DA"+str(start)
                start+=1
            outfile.write("{}\t{}\t{}\n".format(protein_name,DoA__dictionary[domainA],domainA))








if __name__ == '__main__':

    args = normol_get()
    input_file = args.input
    output_file = args.output
    domainA_infine(input_file,output_file)