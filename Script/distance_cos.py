# -*- encoding: utf-8 -*-
'''
@File    :   distance_cos.py
@Time    :   2024/07/01 16:02:40
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib


import argparse
import pandas as pd
from scipy.spatial.distance import pdist, squareform

def parse_arguments():
    """
    解析命令行参数。
    
    返回:
        args: 解析后的参数。
    """
    parser = argparse.ArgumentParser(description="计算输入文件的余弦相似度矩阵")
    parser.add_argument('-i', '--input', required=True, help='包含每个物种domain组成的输入文件')
    parser.add_argument('-o', '--output', required=True, help='保存相似度矩阵的输出文件')
    args = parser.parse_args()
    return args

def calculate_cosine_similarity(input_file, output_file):
    """
    从输入文件计算余弦相似度矩阵，并保存到输出文件。
    
    参数:
        input_file (str): 输入文件的路径。
        output_file (str): 输出文件的路径。
    """
    try:
        # 读取输入文件
        df = pd.read_csv(input_file, sep='\t', index_col=0)
        
        # 提取用于计算相似度的向量
        vectors = df.values
        
        # 计算余弦距离
        distances = pdist(vectors.T, metric='cosine')
        
        # # 将余弦距离转换为余弦相似度
        # similarities = 1 - distances
        
        # 获取向量名称
        vector_names = df.columns
        
        # 构建相似度矩阵
        similarity_matrix = squareform(distances)
        
        # 将相似度矩阵保存到文件
        pd.DataFrame(similarity_matrix, index=vector_names, columns=vector_names).to_csv(output_file, sep='\t')
        
        print(f"余弦相似度矩阵已保存到文件: {output_file}")
    
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    args = parse_arguments()
    calculate_cosine_similarity(args.input, args.output)