# -*- encoding: utf-8 -*-
'''
@File    :   Domain_count.py
@Time    :   2024/05/11 10:22:55
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib
# 该脚本用于统计物种层面每种蛋白domain是否出现以及出现次数
import argparse
import ast
import re

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -l list.txt -o output_file")
    parser.add_argument('-i','--input',help='输入文件,每个物种的蛋白记忆domain组成')
    parser.add_argument('-l','--list',help='输入文件,domain的列表')
    parser.add_argument('-o','--output',help='输出文件,物种的domain组成')
    args = parser.parse_args()
    
    return args

def read_list(list_file):
    domain_dictionary={}
    with open(list_file,'r') as file:
        lines = file.readlines()
    for domain in lines:
        domain = domain.strip()
        domain_dictionary[domain]=0
    return domain_dictionary

def read_input(input_file):
    protein_data = {}
    with open(input_file,'r') as file:
        for line in file:
            data = line.strip().split('\t')
            protein_name = data[0]
            domains = ast.literal_eval(data[1])
            protein_data[protein_name] = domains
    return protein_data

def domainA_infine(input_file,protein_data,domain_dictionary,output_file):
    for proetin in protein_data:
        for domain in protein_data[proetin]:
            if domain in domain_dictionary:
                domain_dictionary[domain] +=1
            else:
                pass
    with open(output_file,'w') as file:
        match = re.search(r"/([^/]+)\.tsv$", input_file)
        if match:
            strain_name = match.group(1)
        file.write("{}\t{}\n".format("domain",strain_name))
        for domain in domain_dictionary:
            file.write("{}\t{}\n".format(domain,domain_dictionary[domain]))




if __name__ == '__main__':

    args = normol_get()
    input_file = args.input
    list_file = args.list
    output_file = args.output
    domain_dictionary = read_list(list_file)
    protein_data = read_input(input_file)

    domainA_infine(input_file,protein_data,domain_dictionary,output_file)

