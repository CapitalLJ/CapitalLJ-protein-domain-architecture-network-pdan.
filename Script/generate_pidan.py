# -*- encoding: utf-8 -*-
'''
@File    :   generate_pidan.py
@Time    :   2024/06/03 10:03:13
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

import csv
import argparse

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -l dan_list -o output_file")
    parser.add_argument('-i','--input',help='输入文件,DAN聚类结果文件')
    parser.add_argument('-l','--list',help='输入文件,DAN列表文件')
    parser.add_argument('-o','--output',help='输出文件,pidan列表文件')


    args = parser.parse_args()
    
    return args


def generate_pidan_names(input_file, dan_file, output_file):
    used_dans = set()
    pidan_id = 1
    pidan_start_single = 10001
    all_dans = set()

    # 读取聚类文件并生成 pidan 编号
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            # 生成 pidan 名称
            pidan_name = f"pidan{pidan_id:05d}"
            pidan_id += 1
            
            # 将行数据转化为列表格式
            dan_list = row
            used_dans.update(dan_list)
            
            # 写入结果到输出文件
            writer.writerow([pidan_name, dan_list])

    # 读取所有 DAN 编号
    with open(dan_file, 'r') as danfile:
        reader = csv.reader(danfile, delimiter='\t')
        for row in reader:
            all_dans.add(row[0])

    # 找出未在聚类文件中出现的 DAN 编号
    unused_dans = all_dans - used_dans

    # 为每个未使用的 DAN 编号生成新的 pidan 编号
    with open(output_file, 'a', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='\t')
        for dan in unused_dans:
            pidan_name = f"pidan{pidan_start_single:05d}"
            pidan_start_single += 1
            writer.writerow([pidan_name, [dan]])

if __name__ == "__main__":
    args = normol_get()
    input_file = args.input
    output_file = args.output
    dan_file = args.list

    generate_pidan_names(input_file, dan_file, output_file)