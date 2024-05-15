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
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor
from Bio.Phylo.Consensus import bootstrap_trees
from Bio.Phylo.Applications import PhymlCommandline
import numpy as np

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -o output_file")
    parser.add_argument('-i','--input',help='输入文件,循环矩阵,distance信息')
    parser.add_argument('-o','--output',help='输出文件,整合所有物种的domain组成,以供后续计算距离')
    args = parser.parse_args()
    
    return args

def distance_tree(input_file, output_file):
    # 读取距离矩阵，排除第一列
    distance_matrix = np.genfromtxt(input_file, delimiter="\t")
    processed_matrix = distance_matrix[1:, 1:]

    num_rows, num_cols = processed_matrix.shape
    triangle_matrix = []
    for i in range(num_rows):
        x=i+1
        row_data = []
        for j in range(x):
            row_data.append(processed_matrix[i, j])
        triangle_matrix.append(row_data)

    # 提取名称列表，去掉空变量
    with open(input_file) as f:
        lines = f.readlines()
        names = lines[0].strip().split("\t")[0:]
        names = [name for name in names if name]  # 去掉空变量

    print(len(triangle_matrix))

    # 创建 DistanceMatrix 对象
    dm = DistanceMatrix(names=names, matrix=triangle_matrix)

    # 使用 Neighbor Joining 方法构建树
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(dm)

    # 保存树结构到文件
    Phylo.write(tree, output_file, "newick")

    # 将距离矩阵保存到 Phylip 格式的文件中
    # with open("distance_matrix.phy", "w") as phylip_file:
    #     phylip_file.write(f"{len(names)}\n")
    #     for i in range(len(names)):
    #         phylip_file.write(f"{names[i]:<10} {' '.join(str(x) for x in distance_matrix_list[i])}\n")

    # # 使用 Phyml 运行
    # phyml_cline = PhymlCommandline(input="distance_matrix.phy")
    # phyml_cline()

if __name__ == '__main__':

    args = normol_get()
    input_file = args.input
    output_file = args.output
    num_columns = 185
    distance_tree(input_file,output_file)


