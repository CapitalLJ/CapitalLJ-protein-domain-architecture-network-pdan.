# -*- encoding: utf-8 -*-
'''
@File    :   protein_get.py
@Time    :   2024/06/05 14:17:32
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib
# 该脚本用于将每个pidan中对应的蛋白输出到一个文件里面，组成一个蛋白库，后续用于比对
import argparse
import ast
from Bio import SeqIO
import os

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -l pidan_list -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,所有物种的蛋白文件')
    parser.add_argument('-l', '--pidanlist', help='输入文件,pidan列表文件')
    parser.add_argument('-o', '--output', help='输出文件夹,每一个pidan一个文件')

    args = parser.parse_args()
    return args

def read_fasta(file_path):
    sequences_dict = {}

    with open(file_path, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            sequences_dict[record.id] = {
                "sequence": str(record.seq),
                "description": record.description
            }

    return sequences_dict


def read_pidan_list(file_path):
    pidan_dict = {}

    with open(file_path, 'r') as f:
        for line in f:
            pidan, da_list = line.strip().split('\t')
            da_numbers = ast.literal_eval(da_list)
            pidan_dict[pidan] = da_numbers

    return pidan_dict


def protein_get(sequences_dict,pidan_dict,output):
    if not os.path.exists(output):
        os.makedirs(output)

    # 遍历每个pidan，找到对应的蛋白，并输出到文件
    for pidan, da_numbers in pidan_dict.items():
        if len(da_numbers) == 1:
            continue
        output_file_path = os.path.join(output, f"{pidan}.fasta")
        with open(output_file_path, 'w') as output_file:
            for da in da_numbers:
                if da in sequences_dict:
                    seq_info = sequences_dict[da]
                    output_file.write(f">{da} {seq_info['description']}\n")
                    output_file.write(f"{seq_info['sequence']}\n")
                else:
                    print(f"警告: {da} 在蛋白文件中未找到，跳过。")


def main():
    args = normol_get()

    sequences_dict = read_fasta(args.input)
    pidan_dict = read_pidan_list(args.pidanlist)
    protein_get(sequences_dict,pidan_dict,args.output)


if __name__ == "__main__":
    main()
