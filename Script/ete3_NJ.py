# -*- encoding: utf-8 -*-
'''
@File    :   phylip_tree.py
@Time    :   2024/05/11 16:59:30
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib
# 该脚本用于将循环distance矩阵转化为tree结构

import argparse
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import average
from ete3 import Tree

def normol_get():
    parser = argparse.ArgumentParser(description="python phylip_tree.py -i input_file -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,循环矩阵,distance信息')
    parser.add_argument('-o', '--output', help='输出文件,整合所有物种的domain组成,以供后续计算距离')
    args = parser.parse_args()
    return args

def distance_tree(input_file, output_file):
    # 读取距离矩阵，排除第一列
    distance_matrix = np.genfromtxt(input_file, delimiter="\t")
    processed_matrix = distance_matrix[1:, 1:]

    # 提取名称列表
    with open(input_file) as f:
        lines = f.readlines()
        names = lines[0].strip().split("\t")[1:]  # 从第一个列开始
        names = [name for name in names if name]  # 去掉空变量

    # 创建邻接矩阵
    dist_array = squareform(processed_matrix)
    linkage_matrix = average(dist_array)

    # 使用 ete3 创建 NJ 树
    tree = Tree.from_linkage_matrix(linkage_matrix, names)

    # 保存树结构到文件
    tree.write(outfile=output_file, format=1)



if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    distance_tree(input_file, output_file)