# -*- encoding: utf-8 -*-
'''
@File    :   disatnce_EU.py
@Time    :   2024/05/11 15:28:21
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

import argparse
import pandas as pd
from scipy.spatial.distance import pdist, squareform

def normol_get():
    parser = argparse.ArgumentParser(description="python scan_domainA.py -i input_file -l list.txt -o output_file")
    parser.add_argument('-i','--input',help='输入文件,每个物种的domain组成')
    parser.add_argument('-o','--output',help='输出文件,整合所有物种的domain组成,以供后续计算距离')
    args = parser.parse_args()
    
    return args

def distance_EU(input_file,output_file):

    df = pd.read_csv(input_file, sep='\t', index_col=0)

# 提取要计算距离的向量数据
    vectors = df.values

# 计算欧氏距离
    distances = pdist(vectors.T, metric='euclidean')

# 获取要计算的向量名称
    vector_names = df.columns

# 构建距离矩阵
    distance_matrix = squareform(distances)

# 将距离矩阵保存到文件
    pd.DataFrame(distance_matrix, index=vector_names, columns=vector_names).to_csv(output_file, sep='\t')

    print("欧氏距离矩阵已保存到文件:", output_file)

if __name__ == '__main__':

    args = normol_get()
    input_file = args.input
    output_file = args.output

    distance_EU(input_file,output_file)
