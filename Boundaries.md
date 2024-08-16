### 根据每个物种的DA特征进行细菌物种边界探究

输入文件格式：tsv文件（第一列物种基因组名称，第二列属于DA信息-33974个DA）

```txt
Es_coli_005008_GCF_013426115_1  1,5,2,7,6,6,2,1,0,12,0,4,1,57,0,1,3,0,2,0,0,2,8,2,4,0,1,24,0,1,11,2,44,3,6........

```


#### 代表性物种选择（sub57）

8092 个物种	聚类前：163583	聚类后：27779
57 个物种	聚类前：47125	聚类后：2582




聚类依据根据cos相似性进行聚类，cos相似性大于0.98聚在一起，非重复放回，牺牲精度（减少复杂度）

```python
import argparse
import numpy as np
# 该脚本属于不完全聚类，从第一个物种开始遍历列表寻找cos相似度大于0.98的物种构成一个分组，
# 再从剩下的列表重复操作（非放回，牺牲精度提高效率）

def normal_get():
    parser = argparse.ArgumentParser(description="python cluster.py -i input_file -f protein_file -o output_dir")
    parser.add_argument('-i', '--input', help='输入文件，物种的DA信息')
    parser.add_argument('-o', '--output', help='输出文件,聚类后的文件，用于下一步输入')
    parser.add_argument('-l', '--list', help='输出文件,聚类后的文件间的相似性')
    parser.add_argument('-n', '--number', type=float, help='相似性阈值')
    args = parser.parse_args()
    return args


def cosine_similarity(list1, list2):
    array1 = np.array(list1)
    array2 = np.array(list2)
    dot_product = np.dot(array1, array2)
    norm_array1 = np.linalg.norm(array1)
    norm_array2 = np.linalg.norm(array2)
    if norm_array1 == 0 or norm_array2 == 0:
        return 0  # 避免除以零
    else:
        similarity = dot_product / (norm_array1 * norm_array2)
        return similarity

# 读取文件并获取菌株的da_list
def read_info(input_file):
    strain_da = {}
    with open(input_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if line.startswith('#'):
                continue
            data = line.strip().split('\t')
            strain_name = data[0]
            da_list = [int(item) for item in data[1].split(',')]
            strain_da[strain_name] = da_list
    return strain_da

# 计算菌株对的余弦相似性并聚类
def calculate_similarities(strain_da,number):
    strain_names = list(strain_da.keys())
    rep_strain_names = {}  # 用于储存聚类信息 ，健为代表性物种，值为物种名称列表
    groups = [] # 用于储存已经聚类的数组，避免重复循环
    similarities = []

    for name1 in strain_names:
        if name1 in groups :  # 如果已经分组，则跳过循环
            continue
        else:
            rep_strain_names[name1] = []
            groups.append(name1) # name1 属于已经聚类
            for name2 in strain_names:
                if name2 not in groups:
                    similarity = cosine_similarity(strain_da[name1], strain_da[name2])
                    if similarity >= number :
                        rep_strain_names[name1].append(name2)
                        groups.append(name2)  #  name2完成聚类
                        similarities.append((name1, name2, similarity))  # 储存聚类信息
    return rep_strain_names,similarities

# 将相似性结果写入TSV文件
def write_similarities(similarities, list_file):
    with open(list_file, 'w') as file:
        # 写入标题行
        file.write("rep_name\tStrain2\tSimilarity\n")
        for strain1, strain2, similarity in similarities:
            file.write(f"{strain1}\t{strain2}\t{similarity:.4f}\n")

def write_rep_strain(rep_strain_names,strain_da,output_file):
    with open(output_file, 'w') as file:
        for strains in rep_strain_names:
            da_list = strain_da[strains]
            da_string = ','.join(map(str, da_list))
            file.write(f"{strains}\t{da_string}\n")


# 主函数
def main(input_file, output_file,list_file,number):
    # 读取数据
    strain_da = read_info(input_file)
    # 计算相似性
    rep_strain_names,similarities = calculate_similarities(strain_da,number)
    # 写入结果
    write_similarities(similarities, list_file)
    write_rep_strain(rep_strain_names,strain_da,output_file)


if __name__ == "__main__":
    args = normal_get()

    input_file = args.input
    output_file = args.output
    list_file = args.list
    number = args.number
    main(input_file, output_file,list_file,number)

```






#### 物种内部cos相似度计算

每个物种的多个基因组储存在一个tsv文件中，格式同上，计算聚类后的物种内部cos相似性

```python
import argparse
import numpy as np
# 输入文件为单个物种的DA信息文件

def normal_get():
    parser = argparse.ArgumentParser(description="python cos_blast.py -i input_file -o output_file")
    parser.add_argument('-i', '--input', help='输入文件，info.tsv')
    parser.add_argument('-o', '--output', help='输出文件,物种内相似性')
    args = parser.parse_args()
    return args

def cosine_similarity(list1, list2):  # 计算cos相似性
    array1 = np.array(list1)  
    array2 = np.array(list2)
    dot_product = np.dot(array1, array2)
    norm_array1 = np.linalg.norm(array1)
    norm_array2 = np.linalg.norm(array2)
    if norm_array1 == 0 or norm_array2 == 0:
        return 0  # 避免除以零
    else:
        similarity = dot_product / (norm_array1 * norm_array2)
        return similarity

# 读取文件并获取菌株的da_list
def read_info(input_file):
    strain_da = {}
    with open(input_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if line.startswith('#'):
                continue
            data = line.strip().split('\t')
            strain_name = data[0]
            da_list = [int(item) for item in data[1].split(',')]
            strain_da[strain_name] = da_list
    return strain_da

# 计算所有菌株对的余弦相似性
def calculate_similarities(strain_da):
    strain_names = list(strain_da.keys())
    similarities = []
    for i in range(len(strain_names)):
        for j in range(i + 1, len(strain_names)):
            strain1 = strain_names[i]
            strain2 = strain_names[j]
            similarity = cosine_similarity(strain_da[strain1], strain_da[strain2])
            similarities.append((strain1, strain2, similarity))
    return similarities

# 将相似性结果写入TSV文件
def write_similarities(similarities, output_file):
    with open(output_file, 'w') as file:
        # 写入标题行
        file.write("Strain1\tStrain2\tSimilarity\n")
        for strain1, strain2, similarity in similarities:
            file.write(f"{strain1}\t{strain2}\t{similarity:.4f}\n")

# 主函数
def main(input_file, output_file):
    # 读取数据
    strain_da = read_info(input_file)
    # 计算相似性
    similarities = calculate_similarities(strain_da)
    # 写入结果
    write_similarities(similarities, output_file)

if __name__ == "__main__":
    args = normal_get()

    input_file = args.input
    output_file = args.output
    main(input_file, output_file)
```

#### 物种间cos相似度计算
计算不同物种之间cos相似性

```python
import argparse
import numpy as np
# 输入文件为2个，query为所有物种的DA信息文件，input为单个物种的DA信息文件，A-B和B-A计算了2次

def normal_get():
    parser = argparse.ArgumentParser(description="python import DA_protein_intract.py -i input_file -f protein_file -o output_dir")
    parser.add_argument('-q', '--query', help='DA的总文件')
    parser.add_argument('-i', '--input', help='输入文件')
    parser.add_argument('-o', '--output', help='输出文件,物种内相似性')
    args = parser.parse_args()
    return args


def cosine_similarity(list1, list2):
    array1 = np.array(list1)
    array2 = np.array(list2)
    dot_product = np.dot(array1, array2)
    norm_array1 = np.linalg.norm(array1)
    norm_array2 = np.linalg.norm(array2)
    if norm_array1 == 0 or norm_array2 == 0:
        return 0  # 避免除以零
    else:
        similarity = dot_product / (norm_array1 * norm_array2)
        return similarity

# 读取文件并获取菌株的da_list
def read_info(input_file):
    strain_da = {}
    with open(input_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if line.startswith('#'):
                continue
            data = line.strip().split('\t')
            strain_name = data[0]
            da_list = [int(item) for item in data[1].split(',')]
            strain_da[strain_name] = da_list
    return strain_da

# 计算所有菌株对的余弦相似性
def calculate_similarities(strain_da,query_all_da):
    similarities = []
    for name1 in strain_da:
        for name2 in query_all_da:
            if name1 != name2:
                similarity = cosine_similarity(strain_da[name1], query_all_da[name2])
                similarities.append((name1, name2, similarity))
    return similarities

# 将相似性结果写入TSV文件
def write_similarities(similarities, output_file):
    with open(output_file, 'w') as file:
        # 写入标题行
        file.write("Strain1\tStrain2\tSimilarity\n")
        for strain1, strain2, similarity in similarities:
            file.write(f"{strain1}\t{strain2}\t{similarity:.4f}\n")

# 主函数
def main(input_file, output_file,query_file):
    # 读取数据
    strain_da = read_info(input_file)
    query_all_da = read_info(query_file)
    # 计算相似性
    similarities = calculate_similarities(strain_da,query_all_da)
    # 写入结果
    write_similarities(similarities, output_file)





if __name__ == "__main__":
    args = normal_get()
    query_file = args.query
    input_file = args.input
    output_file = args.output
    main(input_file, output_file,query_file)

```

给计算后的cos相似性文件加上物种信息等

```txt
strains1    strains2    cos_similar species(strains1)   same_species
Acin_baum_04117201_GCF_028751705_1  Acin_baum_13A297n_GCF_030413705_1   0.9780  Acinetobacter_baumannii Y
Acin_baum_04117201_GCF_028751705_1  Acin_pittii_2018EL_00063_GCF_022213985_1    0.9699  Acinetobacter_baumannii N  
```

```python

import argparse
import os 
import re

def normal_get():
    parser = argparse.ArgumentParser(description="python info_add.py -i input_file -l list_dist -o output_file")
    parser.add_argument('-l', '--list', help='列表文件输入文件夹')
    parser.add_argument('-i', '--input', help='输入文件')
    parser.add_argument('-o', '--output', help='输出文件,物种内相似性')
    args = parser.parse_args()
    return args


def read_list(list_dir):
   name_dir={}
   for filename in os.listdir(list_dir):
        if filename.endswith('.list'):
            with open(os.path.join(list_dir, filename), 'r') as file:
                species = re.sub(r'\.list$', '', filename)
                for line in file:
                    strains=line.strip()
                    name_dir[strains] = species
    return name_dir



def info_add(name_dir,input_file,output_file):
    with open(input_file, 'r') as file,open(output_file, 'w') as outfile:
        for line in file:
            data = line.strip().split('\t')
            strains1 = data[0]
            strains2 = data[1]
            if name_dir[strains1] = name_dir[strains2]:
                same_species = 'Y'
            else：
                same_species = 'N'
            outfile.write(f"{strains1}\t{strains2}\t{data[2]}\t{name_dir[strains1]}\t{same_species}\n")


if __name__ == "__main__":
    args = normal_get()
    list_dir = args.list
    input_file = args.input
    output_file = args.output

    name_dir = read_list(list_dir)
    info_add(name_dir,input_file,output_file)

```