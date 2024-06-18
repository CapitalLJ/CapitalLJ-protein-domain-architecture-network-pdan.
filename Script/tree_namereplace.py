# -*- encoding: utf-8 -*-
'''
@File    :   tree_namereplace.py
@Time    :   2024/06/13 13:45:22
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib


import argparse
import csv

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file  -l list.tsv -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,')
    parser.add_argument('-l', '--list', help='替换列表文件,')
    parser.add_argument('-o', '--output', help='输出文件,')
    args = parser.parse_args()
    return args
def load_mapping(tsv_file):
    mapping = {}
    with open(tsv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if len(row) == 2:
                name, id = row
                mapping[id] = name
    return mapping

def replace_ids_in_text(text_file, mapping, output_file):
    with open(text_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
    for id, name in mapping.items():
        content = content.replace(id, name)
        
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    tsv_file = args.list
    mapping = load_mapping(tsv_file)
    replace_ids_in_text(input_file, mapping, output_file)