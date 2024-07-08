# -*- encoding: utf-8 -*-
'''
@File    :   distance_EU_boot.py
@Time    :   2024/07/01 00:22:29
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib


import argparse
import pandas as pd
import numpy as np
import os
from scipy.spatial.distance import pdist, squareform

def normol_get():
    parser = argparse.ArgumentParser(description="python distance_EU.py -i input_file -o output_folder -b num_bootstrap")
    parser.add_argument('-i', '--input', help='输入文件,每个物种的domain组成')
    parser.add_argument('-o', '--output', help='输出文件夹,用于存储所有自举样本的输出文件')
    parser.add_argument('-b', '--bootstrap', type=int, default=1, help='自举随机取样次数')
    args = parser.parse_args()
    
    return args

def distance_EU(input_file, output_folder, num_bootstrap):
    df = pd.read_csv(input_file, sep='\t', index_col=0)
    vectors = df.values
    vector_names = df.columns

    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_bootstrap):
        if num_bootstrap > 1:
            sampled_indices = np.random.choice(len(vectors), size=len(vectors), replace=True)
            sampled_vectors = vectors[sampled_indices]
        else:
            sampled_vectors = vectors
        
        distances = pdist(sampled_vectors.T, metric='euclidean')
        distance_matrix = squareform(distances)

        output_file = os.path.join(output_folder, f"bootstrap_{i+1}.csv")

        pd.DataFrame(distance_matrix, index=vector_names, columns=vector_names).to_csv(output_file, sep='\t')
        
        print(f"欧氏距离矩阵已保存到文件: {output_file}")

if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_folder = args.output
    num_bootstrap = args.bootstrap

    distance_EU(input_file, output_folder, num_bootstrap)