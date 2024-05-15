# -*- encoding: utf-8 -*-
'''
@File    :   scan_domainA.py
@Time    :   2024/05/09 10:01:55
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

import argparse

# 该脚本可以对hmmscan后的结果进行处理，相同区域被识别为不同domain的按照E-value进行取舍；如果两个domain有重叠，重叠部分大于百分之50%的，按照
# E-value进行取舍



def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -o output_file")
    parser.add_argument('-i','--input',help='输入文件,hmmscan后的结构')
    parser.add_argument('-o','--output',help='输出文件,包括蛋白和domain组成')
    args = parser.parse_args()
    
    return args

#判断domain结构域是否有重叠
def is_overlap(domain1, domain2):
    # start1, end1, evalue1, name = map(float, domain1)
    # start2, end2, evalue2, name = map(float, domain2)
    start1 = float(domain1[0])
    end1 = float(domain1[1])
    start2 = float(domain2[0])
    end2 = float(domain2[1])
    overlap_length = min(end1, end2) - max(start1, start2)
    if overlap_length > 0:
        if overlap_length / (end1 - start1) >= 0.5 or overlap_length / (end2 - start2) >= 0.5:
                return True
    return False

# 重叠结构域根据E-value进行取舍
def compare_evalues(domain1, domain2):
    return float(domain1[2]) - float(domain2[2])


def get_start(element):
    return element[0]

def scan_to_domainA(input_file,output_file):

    with open(input_file,'r') as file:
        lines = file.readlines()
    protein_dictionary={}
    domain_dictionary={}
    for line in lines:
        if not line.startswith('#'):
            domain_list=[]
            parts = line.strip().split()
            protein_key = parts[3]
            domain_name = parts[0]
            domain_list = [parts[17],parts[18],parts[6],parts[0]]

            if protein_key in protein_dictionary:
                protein_dictionary[protein_key].append(domain_name)
                domain_dictionary[protein_key].append(domain_list)
            else:
                protein_dictionary[protein_key] = [domain_name]
                domain_dictionary[protein_key]=[domain_list]


    # 处理每个蛋白质的 domain 列表
    protein_DA={}
    for protein in protein_dictionary:
        unique_domains = []
        DA_domain = []
        for domain1_list in domain_dictionary[protein]:
            is_unique = True
            for domain2_list in unique_domains:
                if is_overlap(domain1_list, domain2_list):
                    # 如果有重叠，则比较 E 值
                    if compare_evalues(domain1_list, domain2_list) < 0:
                        # 如果 domain1 的 E 值更小，则替换 domain2
                        unique_domains.remove(domain2_list)
                        unique_domains.append(domain1_list)
                    is_unique = False
                    break
            if is_unique:
                unique_domains.append(domain1_list)
        Domain_sort = sorted(unique_domains, key=lambda x: int(x[0]))
        for i in Domain_sort:
            DA_domain.append(i[3])
        protein_DA[protein] = DA_domain
    with open(output_file,"w") as file:
        for i in protein_DA:
            file.write("{}\t{}\n".format(i,protein_DA[i]))

    
    







if __name__ == '__main__':

    args = normol_get()
    input_file = args.input
    output_file = args.output
    result = scan_to_domainA(input_file,output_file)