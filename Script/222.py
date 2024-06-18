# -*- encoding: utf-8 -*-
'''
@File    :   111.py
@Time    :   2024/06/16 14:33:56
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib


# 根据DA的相似性文件和列表文件

import argparse
import ast

def get_args():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -o output_file")
    parser.add_argument('-i', '--input', required=True, help='输入文件, DA的相似性')
    parser.add_argument('-l', '--list', required=True, help='输入文件, DA列表')
    parser.add_argument('-o', '--output', required=True, help='输出文件, DA列表文件')
    return parser.parse_args()

def extract_da(input_file, list_file ,output_file):
    da_list = {}
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                parts = line.strip().split('\t')
                da_list[parts[0]] = ast.literal_eval(parts[1])

    except Exception as e:
        print(f"Error reading input file: {e}")
        return
    out_da_list = {}
    try:
        with open(list_file, 'r', encoding='utf-8') as listfile:
            for line in listfile:
                parts = line.strip().split('\t')
                if parts[0] in da_list:
                    out_da_list[parts[0]] = da_list[parts[0]]
    except Exception as e:
        print(f"Error reading list file: {e}")


    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for da in out_da_list:
                outfile.write(f"{da}\t{out_da_list[da]}\n")
    except Exception as e:
        print(f"Error writing output file: {e}")    


def main():
    args = get_args()
    extract_da(args.input, args.list ,args.output)

if __name__ == "__main__":
    main()