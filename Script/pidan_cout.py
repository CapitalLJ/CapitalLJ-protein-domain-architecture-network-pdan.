# -*- encoding: utf-8 -*-
'''
@File    :   pidan_cout.py
@Time    :   2024/06/24 21:47:30
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib


# 该脚本用于统计物种层面第四个层次的信息 pidan
# 输入文件为scan的结果转化为domain的文件；加上结构域对应的DA文件；再加上pidan列表文件夹
# 输出文件保存在count_to_distance中的pidan文件夹里
import argparse
import ast
import re
import os
import glob
import csv


def normol_get():
    parser = argparse.ArgumentParser(description="python domain_to_count.py -i input_dir -l strain_DA_list -p pidan_dir -o output_dir")
    parser.add_argument('-i','--input',help='输入文件,每个物种的蛋白记忆domain组成')
    parser.add_argument('-o','--output',help='输出文件夹，包括中间文件')
    parser.add_argument('-l','--DA_list',help='DA和结构域组成以及蛋白名称的文件')
    parser.add_argument('-p','--pidan_dir',help='pidan列表文件夹')
    args = parser.parse_args()
    return args

# =========================================================

# 读取单个物种的输入文件脚本
def read_input(input_file):
    protein_data = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            protein_name = data[0]
            domains = ast.literal_eval(data[1])
            protein_data[protein_name] = domains
    return protein_data

#将输入文件夹内的所有函数都读取存储到变量中，后续不再进行读取操作
def read_all_files(input_dir):
    species_data = {}
    file_paths = glob.glob(os.path.join(input_dir, '*.tsv'))
    for file_path in file_paths:
        if os.path.isfile(file_path):
            species_name = os.path.basename(file_path).replace('.tsv', '')
            protein_data = read_input(file_path)
            species_data[species_name] = protein_data
    return species_data


# 将蛋白名称和DA名称读取
def read_DA_list(DA_list_file):
    DA_dir = {}
    with open(DA_list_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            protein_name = data[0]
            DA_dir[protein_name] = data[1]
    
    return DA_dir


# 将pidan名称和DA列表读取
def read_pidan_list(pidan_file):
    pidan_dir={}
    with open(pidan_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            pidan_name = data[0]
            da_list = ast.literal_eval(data[1])
            pidan_dir[pidan_name] = da_list
    return pidan_dir



# ===========================================================================

def pidan_infine(species_data,DA_dir,pidan_dir,output_dir):
    file_paths = glob.glob(os.path.join(pidan_dir, '*.txt'))
    for file_path in file_paths:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path).replace('_list.txt', '')
            pidan_list =  read_pidan_list(file_path)
            pidan_dictionary ={species: {pidan: 0 for pidan in pidan_list} for species in species_data}


            for species_name, protein_data in species_data.items():
                for protein in protein_data:
                    DA_name = DA_dir[protein]
                    for pidan in pidan_list:
                        if DA_name in pidan_list[pidan]:
                            pidan_dictionary[species_name][pidan]=1

            output_path = os.path.join(output_dir, 'pidan_01')
            os.makedirs(output_path, exist_ok=True)  


            with open(os.path.join(output_path, file_name), 'w', newline='') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                header = ['pidan'] + list(pidan_dictionary.keys())
                writer.writerow(header)
                
                for pidan in pidan_list:
                    row = [pidan] + [pidan_dictionary[species][pidan] for species in pidan_dictionary]
                    writer.writerow(row)           

def pidan_count(species_data,DA_dir,pidan_dir,output_dir):
    file_paths = glob.glob(os.path.join(pidan_dir, '*.txt'))
    for file_path in file_paths:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path).replace('_list.txt', '')
            pidan_list =  read_pidan_list(file_path)
            pidan_dictionary ={species: {pidan: 0 for pidan in pidan_list} for species in species_data}


            for species_name, protein_data in species_data.items():
                for protein in protein_data:
                    DA_name = DA_dir[protein]
                    for pidan in pidan_list:
                        if DA_name in pidan_list[pidan]:
                            pidan_dictionary[species_name][pidan]+=1

            output_path = os.path.join(output_dir, 'pidan_count')
            os.makedirs(output_path, exist_ok=True)  


            with open(os.path.join(output_path, file_name), 'w', newline='') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                header = ['pidan'] + list(pidan_dictionary.keys())
                writer.writerow(header)
                
                for pidan in pidan_list:
                    row = [pidan] + [pidan_dictionary[species][pidan] for species in pidan_dictionary]
                    writer.writerow(row)      














if __name__ == '__main__':

    args = normol_get()
    input_dir = args.input
    output_dir = args.output
    DA_list_file = args.DA_list
    pidan_dir = args.pidan_dir

    species_data = read_all_files(input_dir)  # 读取输入文件夹内所有物种。
    DA_dir = read_DA_list(DA_list_file)

    # pidan_infine(species_data,DA_dir,pidan_dir,output_dir)
    pidan_count(species_data,DA_dir,pidan_dir,output_dir)