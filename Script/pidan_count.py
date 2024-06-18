# -*- encoding: utf-8 -*-
'''
@File    :   pidan_count_0_1.py
@Time    :   2024/06/03 11:17:46
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

import argparse
import ast
import re


def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -I dan_list -l pidan_list -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,物种的domain鉴定文件')
    parser.add_argument('-I', '--danlist', help='输入文件,DAN列表文件')
    parser.add_argument('-l', '--pidanlist', help='输入文件,pidan列表文件')
    parser.add_argument('-o', '--output', help='输出文件,pidan的有无鉴定')

    args = parser.parse_args()

    return args


def read_species_proteins(input_file):
    species_proteins = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            species_proteins[parts[0]] = ast.literal_eval(parts[1])
    return species_proteins


def read_da_compositions(dan_file):
    da_compositions = {}
    with open(dan_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            da_compositions[parts[0]] = ast.literal_eval(parts[1])
    return da_compositions


def read_pidan_compositions(pidan_file):
    pidan_compositions = {}
    with open(pidan_file, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            pidan_compositions[parts[0]] = ast.literal_eval(parts[1])
    return pidan_compositions


def map_species_to_da(species_proteins, da_compositions):
    species_to_da = {}
    for species, proteins in species_proteins.items():
        species_to_da[species] = []
        for da, da_proteins in da_compositions.items():
            if proteins == da_proteins:
                species_to_da[species].append(da)
    return species_to_da


def count_pidan_da_presence(species_to_da, pidan_compositions):
    results = []
    all_da = [da for das in species_to_da.values() for da in das]
    for pidan, das in pidan_compositions.items():
        count = sum(all_da.count(da) for da in das)
        results.append((pidan, count))
    return results


def write_results(input_file, file_path, results):
    match = re.search(r"/([^/]+)\.tsv$", input_file)
    if match:
        strain_name = match.group(1)
    with open(file_path, 'w') as file:
        file.write("{}\t{}\n".format("pidan_id", strain_name))
        for pidan, count in results:
            file.write(f"{pidan}\t{count}\n")


if __name__ == "__main__":
    args = normol_get()
    input_file = args.input
    output_file = args.output
    dan_file = args.danlist
    pidan_file = args.pidanlist
    species_proteins = read_species_proteins(input_file)
    da_compositions = read_da_compositions(dan_file)
    pidan_compositions = read_pidan_compositions(pidan_file)

    species_to_da = map_species_to_da(species_proteins, da_compositions)

    # 统计每一个pidan的DA出现的次数
    results = count_pidan_da_presence(species_to_da, pidan_compositions)

    # 输出结果到TSV文件
    write_results(input_file, output_file, results)