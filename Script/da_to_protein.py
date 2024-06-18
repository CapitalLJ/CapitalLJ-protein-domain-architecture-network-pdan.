# -*- encoding: utf-8 -*-
'''
@File    :   pidan_count_0_1.py
@Time    :   2024/06/03 11:17:46
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

import argparse
import ast

# 该脚本将蛋白的结构域信息储存为DA信息

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -I dan_list -l pidan_list -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,物种的domain鉴定文件')
    parser.add_argument('-I', '--danlist', help='输入文件,DAN列表文件')
    args = parser.parse_args()
    
    return args

def read_species_proteins(input_file):
    species_proteins = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            species_proteins[parts[0]] = ast.literal_eval(parts[1])
    return species_proteins

def read_compositions(file):
    compositions = {}
    with open(file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            compositions[parts[0]] = ast.literal_eval(parts[1])
    return compositions

def map_species_to_da(species_proteins, da_compositions):
    species_to_da = {}
    print("start")
    for species, proteins in species_proteins.items():
        species_to_da[species] = []
        for da, da_proteins in da_compositions.items():
            if proteins == da_proteins:
                species_to_da[species].append(da)
    print("end")
    with open("all_protein_da.tsv",'w') as file:
        for i in  species_to_da:
            file.write(f"{i}\t{species_to_da[i]}\n")
    return species_to_da

def replace_pidan_compositions(pidan_compositions, species_to_da):
    replaced_pidan = {}
    for pidan, da_list in pidan_compositions.items():
        print(pidan)
        replaced_list = []
        for da in da_list:
            for protein,protein_da in species_to_da:
                if da == protein_da:
                    replaced_list.append(protein)
        replaced_pidan[pidan] = replaced_list
    
    return replaced_pidan

def write_output(output_file, replaced_pidan):
    with open(output_file, 'w') as file:
        for pidan, replaced_list in replaced_pidan.items():
            file.write(f"{pidan}\t{replaced_list}\n")

def main():
    args = normol_get()

    species_proteins = read_species_proteins(args.input)
    da_compositions = read_compositions(args.danlist)
    species_to_da = map_species_to_da(species_proteins, da_compositions)


if __name__ == "__main__":
    main()