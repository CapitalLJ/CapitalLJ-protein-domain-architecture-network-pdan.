# -*- encoding: utf-8 -*-
'''
@File    :   Domain_content_count.py
@Time    :   2024/05/16 10:12:35
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# 该脚本用于统计物种层面每种domain_content是否出现以及出现次数
# A,B 和 B,A视为一个domain_content

import argparse
import ast
import re

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,每个物种的蛋白记忆domain_content组成')
    parser.add_argument('-o', '--output', help='输出文件,物种的domain组成')
    args = parser.parse_args()
    return args

def read_input(input_file):
    protein_data = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            protein_name = data[0]
            domains = ast.literal_eval(data[1])
            # 将 domains 转换为集合，并转换为元组以便可哈希
            domain_set = tuple(sorted(set(domains)))
            protein_data[protein_name] = domain_set
    return protein_data

def domain_content_infine(input_file, protein_data, output_file):
    domain_dictionary = {}
    for protein in protein_data:
        if protein_data[protein] not in domain_dictionary:
            domain_dictionary[protein_data[protein]] = 1
        else:
            domain_dictionary[protein_data[protein]] += 1

    with open(output_file, 'w') as file:
        match = re.search(r"/([^/]+)\.tsv$", input_file)
        if match:
            strain_name = match.group(1)
        file.write("{}\t{}\n".format("domain_content", strain_name))
        for domain, count in domain_dictionary.items():
            file.write("{}\t{}\n".format(domain, count))

if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    protein_data = read_input(input_file)
    domain_content_infine(input_file, protein_data, output_file)