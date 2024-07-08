# -*- encoding: utf-8 -*-
'''
@File    :   shared_bipartitions.py
@Time    :   2024/07/08 09:55:02
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# here put the import lib

import argparse
import os
from io import StringIO
from Bio import Phylo


def parse_arguments():
    """
    解析命令行参数。
    
    返回:
        args: 解析后的参数。
    """
    parser = argparse.ArgumentParser(description="计算两个树文件共享的二分节点")
    parser.add_argument('-q', '--query', required=True, help='模板树文件')
    parser.add_argument('-i', '--input', required=True, help='比对的树文件夹')
    parser.add_argument('-o', '--output', required=True, help='保存相似度矩阵的输出文件')
    args = parser.parse_args()
    return args

def read_trees(tree_file):
    with open(tree_file, 'r') as f:
        tree_str = f.read()
    trees = [tree for tree in re.split(r';\s*\n', tree_str) if tree]
    return [Phylo.read(StringIO(tree + ';'), 'newick') for tree in trees]


def get_clade_terminals(clade):
    return set(term.name for term in clade.get_terminals())

def calculate_topological_similarity(tree1, tree2):
    # 提取树的所有分支
    def get_all_bipartitions(tree):
        bipartitions = set()
        for clade in tree.find_clades():
            if not clade.is_terminal():
                bipartitions.add(frozenset(get_clade_terminals(clade)))
        return bipartitions

    bipartitions1 = get_all_bipartitions(tree1)
    bipartitions2 = get_all_bipartitions(tree2)

    # 计算Jaccard相似度指数
    # print(bipartitions1)
    print(len(bipartitions1))
    print(len(bipartitions2))
    intersection = len(bipartitions1.intersection(bipartitions2))
    # union = len(bipartitions1.union(bipartitions2))
    jaccard_index = intersection / len(bipartitions1) if len(bipartitions1) != 0 else 0

    return jaccard_index

def main():
    args = parse_arguments()

    # 读取模板树并输出其分类单元命名空间
    query_tree = Phylo.read(args.query, 'newick')

    # 打开输出文件
    with open(args.output, 'w') as output_file:
        output_file.write("Tree_Name\tShared_Bipartitions_Percentage\tMax_RF_Distance\n")
        
        # 遍历输入文件夹中的所有树文件
        for tree_filename in os.listdir(args.input):
            tree_path = os.path.join(args.input, tree_filename)
            if os.path.isfile(tree_path):
                target_tree = Phylo.read(tree_path, 'newick')

                similarity_percentage= calculate_topological_similarity(query_tree, target_tree)
                output_file.write(f"{tree_filename}\t{similarity_percentage:.2f}\n")

if __name__ == "__main__":
    main()




