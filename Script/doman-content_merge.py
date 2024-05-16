# -*- encoding: utf-8 -*-
'''
@File    :   doman-content_merge.py
@Time    :   2024/05/16 14:17:58
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib
import argparse
import os

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_dir -l list_file -o output_file")
    parser.add_argument('-i','--input', help='输入文件夹,每个物种的domain组成')
    parser.add_argument('-l','--list', type=str, help='输入文件,domain_content的列表')
    parser.add_argument('-o','--output', help='输出文件,整合所有物种的domain组成,以供后续计算距离')
    args = parser.parse_args()
    
    return args

def read_list2(list_file):
    domain_dictionary = {}
    with open(list_file, 'r') as file:
        lines = file.readlines()
    for line in lines:
        domain = line.strip()
        domains = eval(domain)
        domain_dictionary[domains] = []
    return domain_dictionary

def read_input(input_file):
    protein_data = {}
    with open(input_file, 'r') as file:
        file.readline()
        for line in file:
            data = line.strip().split('\t')
            sorted_domains = data[0]
            domain_c = eval(sorted_domains)
            count = data[1]
            protein_data[domain_c] = count
    return protein_data

def merge(input_dir, output_file, domain_dictionary):
    name_dir={}
    name_dir["domain_content"]=[]
    for filename in os.listdir(input_dir):
        if filename.endswith(".tsv"):
            file_path = os.path.join(input_dir, filename)
            file_domain = read_input(file_path)
            name_dir["domain_content"].append(filename)
            for domain in domain_dictionary:
                if domain in file_domain:
                    domain_dictionary[domain].append(file_domain[domain])
                else:
                    domain_dictionary[domain].append(0)
    
    with open(output_file, 'w') as file:
        names = '\t'.join(map(str, name_dir["domain_content"])) 
        file.write("{}\t{}\n".format("domain_content", names))
        for domain, counts in domain_dictionary.items():
            counts_str = '\t'.join(map(str, counts)) 
            file.write("{}\t{}\n".format(domain, counts_str))


if __name__ == '__main__':
    args = normol_get()
    input_dir = args.input
    output_file = args.output
    list_file = args.list
    domain_dictionary = read_list2(list_file)
    print(111)
    merge(input_dir, output_file, domain_dictionary)