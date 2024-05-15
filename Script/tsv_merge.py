# -*- encoding: utf-8 -*-
'''
@File    :   tsv_merge.py
@Time    :   2024/05/11 13:56:45
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

# 该脚本用于整合所有物种的domain信息,文件夹内文件后缀为.tsv
import os
import pandas as pd
import argparse

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_dir -l list.txt -o output_file")
    parser.add_argument('-i','--input',help='输入文件夹,每个物种的domain组成')
    parser.add_argument('-o','--output',help='输出文件,整合所有物种的domain组成,以供后续计算距离')
    args = parser.parse_args()
    
    return args


def merge(input_dir,output_file):
    merged_data = pd.DataFrame()

    # 读取第一个文件的第一列数据
    first_column = pd.read_csv(os.path.join(input_dir, os.listdir(input_dir)[0]), sep='\t', usecols=[0], header=None)

    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".tsv"):
            file_path = os.path.join(input_dir, filename)
            # 读取文件并合并数据到 DataFrame
            df = pd.read_csv(file_path, sep='\t', header=None)
            merged_data = pd.concat([merged_data, df.iloc[:, 1]], axis=1)

    # 插入第一列数据到 DataFrame 中
    merged_data = pd.concat([first_column, merged_data], axis=1)

    # 写入合并后的数据到新的 tsv 文件
    merged_data.to_csv(output_file, sep='\t', index=False, header=False)



if __name__ == '__main__':

    args = normol_get()
    input_dir = args.input
    output_file = args.output

    merge(input_dir,output_file)
