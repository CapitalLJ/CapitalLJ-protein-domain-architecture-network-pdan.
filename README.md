# CapitalLJ-protein-domain-architecture-network-pdan.

## bac120系统发育树构建

[参考博客](https://blog.csdn.net/woodcorpse/article/details/108924563)

bac120文献 [A standardized bacterial taxonomy based on genome phylogeny substantially revises the tree of life](https://www.nature.com/articles/nbt.4229)

GTDB-Tk是一个软件工具包，用于根据基因组数据库分类法GTDB为细菌和古细菌基因组分配客观的分类法。它旨在与最近的进展一起使用，从而可以直接对环境样本中获得数百或数千个由基因组组装的基因组（MAG）进行物种分类注释。它也可以用于分离和单细胞的基因组物种注释。本次使用的是gtdbtk-2.1.1，下面演示在超算上的简要使用教程。

```shell
export GTDBTK_DATA_PATH="/share/home/wangq/miniconda3/envs/gtdbtk-2.1.1/share/gtdbtk-2.1.1/db"
# gtdbtk 依赖的数据库  

export LD_LIBRARY_PATH="/share/home/wangq/miniconda3/envs/gtdbtk-2.1.1/lib:$LD_LIBRARY_PATH"
# gtdbtk 相关依赖

export LD_LIBRARY_PATH="/share/home/wangq/miniconda3/envs/gtdbtk-2.1.1/lib:$LD_LIBRARY_PATH"
# gtdbtk 加入环境变量

gtdbtk -h 
```


如果想在其他工作站使用，可直接下载压缩包解压缩。[gtdbtk-2.1.1.tar.gz](http://114.212.160.236:5000/)

```shell
tar -xzf  gtdbtk-2.1.1.tar.gz
cd gtdbtk-2.1.1/bin
pwd
# 目前的绝对路径
# 修改gtdbtk第一行的绝对路径


export GTDBTK_DATA_PATH="<your_path>/gtdbtk-2.1.1/share/gtdbtk-2.1.1/db"
export LD_LIBRARY_PATH="<your_path>/gtdbtk-2.1.1/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="<your_path>/gtdbtk-2.1.1/lib:$LD_LIBRARY_PATH"

# 将上面三行加入~/.bashrc

gtdbtk -h 

```
















### pidan分类依据

#### 蛋白序列比对

##### 每一个DA构建一个数据库，每一个DA比对得到一个相似度。

```shell
# all_strain_DA_list.txt  蛋白名称和DA信息    
# BAD46750.1      DA1000000       ('SpoU_methylase',)
# BAD46753.1      DA1000001       ('Glycos_transf_2',)
# BAD46761.1      DA1000002       ('Peptidase_C39', 'ABC_membrane', 'ABC_tran')
# BAD46762.1      DA1000003       ('DUF4294',)

##  蛋白序列建库


for i in $(ls data/DA/);do
makeblastdb -in data/DA/${i}/${i}.faa -dbtype prot -out data/DA/${i}/db
done


for i in $(ls split/);do

cat split/${i} | parallel -j 23 'makeblastdb -in data/DA/{1}/{1}.faa -dbtype prot -out data/DA/{1}/db'

done

#DA_pro_number.tsv
# DA1000000       604
# DA1000001       839
# DA1000002       64

## 建库后比对，DA中的蛋白序列大于2条的进行比对

for i in $(awk '$2 > 2 {print $1}' DA_pro_number.tsv);do
    blastp -query data/DA/${i}/${i}.faa -db data/DA/${i}/db -out data/DA/${i}/output.tsv -outfmt 6 -max_target_seqs 1000000 -num_threads 10 
done


##### pidan 蛋白序列提取

for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    python pidan_pro_intrc.py -i pidan/pidan_${i}_list.txt -l all_strain_DA_list.txt -f all_protein.faa -o data/pidan_${i}
done


echo "0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95" | parallel -j 10
'for i in $(ls data/pidan_{1}/);do ;makeblastdb -in data/pidan_{1}/${i}/${i}.faa -dbtype prot -out data/pidan_{1}/${i}/db ; done
'

#!/usr/bin bash
for i in $(cat 0.05.txt);do
blastp -query data/pidan_0.05/${i}/${i}.faa -db data/pidan_0.05/${i}/db -out data/pidan_0.05/${i}/output.tsv -outfmt 6 -num_threads 22
done


```
 


这个脚本用于提取每个DA下的蛋白序列，后续对每一个DA的蛋白序列文件建库和比对。
```python
# <!-- import DA_protein_intract.py -->
import argparse
import os
from Bio import SeqIO  # 使用Biopython库中的SeqIO来处理序列文件

def normal_get():
    parser = argparse.ArgumentParser(description="python import DA_protein_intract.py -i input_file -f protein_file -o output_dir")
    parser.add_argument('-i', '--input', help='输入文件，蛋白-DA列表')
    parser.add_argument('-f', '--faa', help='蛋白序列文件')
    parser.add_argument('-o', '--output', help='输出文件夹，DA对应的蛋白序列')
    args = parser.parse_args()
    return args

def read_input(input_file):
    DA_protein = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            DA_name = data[1]
            protein_name = data[0]
            if DA_name in DA_protein:
                DA_protein[DA_name].append(protein_name)
            else:
                DA_protein[DA_name] = [protein_name]
    return DA_protein

def read_faa(protein_file):
    protein_seq = {}
    for record in SeqIO.parse(protein_file, 'fasta'):
        protein_seq[record.id] = str(record.seq)
    return protein_seq

def DA_pro_intract(DA_protein, protein_seq, output_dir):
    # 创建输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 提取DA中的所有蛋白序列，并储存到相应的文件夹中
    for DA, proteins in DA_protein.items():
        DA_folder = os.path.join(output_dir, DA)
        if not os.path.exists(DA_folder):
            os.makedirs(DA_folder)
        
        output_file = os.path.join(DA_folder, f"{DA}.faa")  # 文件名为DA名称
        
        with open(output_file, 'w') as f:
            for protein_name in proteins:
                if protein_name in protein_seq:
                    protein_sequence = protein_seq[protein_name]
                    f.write(f">{protein_name}\n{protein_sequence}\n")
                else:
                    print(f"Warning: Protein {protein_name} not found in the sequence file.")

if __name__ == '__main__':
    args = normal_get()
    input_file = args.input
    output_dir = args.output
    protein_file = args.faa

    DA_protein = read_input(input_file)
    protein_seq = read_faa(protein_file)
    DA_pro_intract(DA_protein, protein_seq, output_dir)
```

这个脚本用于从比对结果提取比对分数平均值（一个库有100条序列，归一化就要除以9900[99x100]）


```python

import argparse
import os

def normal_get():
    parser = argparse.ArgumentParser(description="python3 blast_score.py -i input_dir -o output.tsv")
    parser.add_argument('-i', '--input', help='输入文件夹，包含多个子文件夹，每个子文件夹里有一个BLAST输出文件')
    parser.add_argument('-o', '--output', help='输出文件，保存计算结果的tsv文件')
    args = parser.parse_args()
    return args

def parse_blast_output(input_file):
    """解析BLAST输出结果并统计每对序列的最高分数"""
    scores = {}
    unique_queries = set()
    
    with open(input_file) as f:
        for line in f:
            fields = line.strip().split("\t")
            query_id = fields[0]
            subject_id = fields[1]
            score = float(fields[2])  # 比对分数位于第3列

            # 使用 (query_id, subject_id) 作为键
            key = (query_id, subject_id)
            
            # 更新分数，如果当前分数比之前存储的高
            if key not in scores or score > scores[key]:
                scores[key] = score

            # 记录唯一的query_id
            unique_queries.add(query_id)

    # 计算总分数
    total_score = sum(scores.values())
    num = len(unique_queries)
    
    if num > 1:
        adjusted_score = (total_score - 100 * num) / (num * (num - 1))
    else:
        # 当 num <= 1 时，公式的分母会为零，此时调整分数为零或其他适当值
        adjusted_score = 0

    return adjusted_score

def blast_tsv(input_dir, output_file):
    with open(output_file, 'w') as out_f:
        out_f.write("subfolder\ttotal_score\n")
        
        for subdir, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".tsv"):
                    subfolder_name = os.path.basename(subdir)
                    tmp_file = os.path.join(subdir, file)
                    score = parse_blast_output(tmp_file)
                    out_f.write(f"{subfolder_name}\t{score}\n")

if __name__ == '__main__':
    args = normal_get()
    input_dir = args.input
    output_file = args.output
    blast_tsv(input_dir, output_file)

```

这个脚本用于将pidan所包含的DA提取出来

```python

import argparse
import os
import ast

def normal_get():
    parser = argparse.ArgumentParser(description="python import DA_protein_intract.py -i input_file -l list  -o output_file")
    parser.add_argument('-i', '--input', help='输入文件，pidan-DA列表')
    parser.add_argument('-l', '--list', help='输入文件，DA-score')
    parser.add_argument('-o', '--output', help='输出文件,部分DA分数')
    args = parser.parse_args()
    return args

def read_input(input_file):
    pidan_DA = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            DA_list = ast.literal_eval(data[1])
            pidan_name = data[0]
            if len(DA_list) > 1:
                pidan_DA[pidan_name] = DA_list
    return pidan_DA

def read_list(list_file):
    DA_score = {}
    with open(list_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            DA_name = data[0]
            score = data[1]
            DA_score[DA_name] = score
    return DA_score

def wirte_out(pidan_DA,DA_score,output_file):
    piadn_DA_score = {}
    for pidan in pidan_DA:
        for DA in pidan_DA[pidan]:
            if DA in DA_score:
                piadn_DA_score[DA] = DA_score[DA]
    
    with open(output_file, 'w') as f:
        for DA in piadn_DA_score:
            f.write(f"{DA}\t{piadn_DA_score[DA]}\n")



if __name__ == '__main__':
    args = normal_get()
    input_file = args.input
    output_file = args.output
    list_file = args.list

    pidan_DA = read_input(input_file)
    DA_score = read_list(list_file)
    wirte_out(pidan_DA,DA_score,output_file)






```



### POY构建系统发育树
##### 形态学特征与特征向量

使用protein-domain的有无与数量多少进行系统发育树的构建，我们可以在一定程度上与基于形态学的静态同源特征
进行类比。POY中的形态学的编码方案分为两种： non-additive and additive 。这正好与我们的domain鉴定的有无
与数量相匹配。有无对应non-additive，数量对应additive；有关信息可以查看[POY version 4: phylogenetic analysis using dynamic homologies](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1096-0031.2009.00282.x)

##### Hennig86 文件格式

使用POY根据特征向量构树时需要我们将文件转化为特定格式进行输入，这里我们使用的是Hennig86的文件格式，关于Hennig86的信息这里不做展开。感兴趣可以阅读[Hennig86](https://paperzz.com/doc/8636474/hennig86---the-george-washington-university)

将特征向量统计文件转化为Hennig86格式的ss文件
```shell
python3 count_to_ss.py -i 

```
```python
# 脚本名称 count_to_ss.py
# 输入文件夹count_to_distance

import argparse
import pandas as pd
import os

def normol_get():
    parser = argparse.ArgumentParser(description="python count_to_ss.py -i input_file  -o output_file -l strain_number.tsv")
    parser.add_argument('-i','--input',help='输入文件,domain鉴定的文件')
    parser.add_argument('-o','--output',help='输出文件，用于POY构建系统发育的ss文件')
    parser.add_argument('-l','--list',help='输出文件，物种编号文件')
    args = parser.parse_args()
    return args


def read_file(input_file):
    df = pd.read_csv(input_file, sep='\t')
    strain_number={}
    result_dict={}

    for i, column in enumerate(df.columns[1:], start=1):
        new_column_name = f'S{i:08d}'
        strain_number[column] = new_column_name
    
    for i, column in enumerate(df.columns[0:], start=0):
        if i > 0:
            column_values = '\t'.join(df[column].astype(str))
            result_dict[strain_number[column]] = column_values
        else:
            # 对于第一列，保留原始列名（假设第一列是特殊的，比如索引或名称列）
            column_values = '\t'.join(df[column].astype(str))
            result_dict[column] = column_values

    return strain_number,result_dict

def write_strain_number(strain_number, temp_output_list):
    with open(temp_output_list, 'w') as f:
        for original_name, new_name in strain_number.items():
            f.write(f"{original_name}\t{new_name}\n")


def write_output_file(result_dict,output_file):
    keys = list(result_dict.keys())
    # num_keys = len(keys)
    # value_length = len(next(iter(result_dict.values())))
    with open(output_file, 'w') as f:
        # # 写入 xread
        # f.write("xread\n")
        
        # # 写入两个数字
        # f.write(f"{num_keys} {value_length}\n")
        
        # 写入每个键和值
        for key in keys:
            f.write(f"{key}\t{result_dict[key]}\n")
        
        # # 写入结尾的分号
        # f.write(";\n")


        

def compare_and_replace(temp_file, final_file):
    if os.path.exists(final_file):
        with open(temp_file, 'r') as temp, open(final_file, 'r') as final:
            if temp.read() == final.read():
                os.remove(temp_file)
            else:
                print("Error: Temporary file and final file do not match.")
                os.remove(temp_file)
                raise ValueError("Files do not match.")
    else:
        os.replace(temp_file, final_file)

if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    output_list = args.list

    strain_number, result_dict = read_file(input_file)
    
    temp_output_list = output_list + '_temp'
    write_strain_number(strain_number, temp_output_list)
    compare_and_replace(temp_output_list, output_list)
    write_output_file(result_dict, output_file)


```


```python

# 脚本名称 count_to_nex.py
# 输入文件夹count_to_distance

import argparse
import pandas as pd
import os

def normol_get():
    parser = argparse.ArgumentParser(description="python count_to_ss.py -i input_file  -o output_file -l strain_number.tsv -t datatype")
    parser.add_argument('-i','--input',help='输入文件,domain鉴定的文件')
    parser.add_argument('-o','--output',help='输出文件，用于POY构建系统发育的nexus文件')
    parser.add_argument('-l','--list',help='输出文件，物种编号文件')
    parser.add_argument('-t','--type',help='输出文件类型，分为standard和continuous;-t S // -t C')
    args = parser.parse_args()
    return args

def read_file(input_file):
    df = pd.read_csv(input_file, sep='\t')
    strain_number={}
    result_dict={}

    for i, column in enumerate(df.columns[1:], start=1):
        new_column_name = f'S{i:08d}'
        strain_number[column] = new_column_name
        column_values = df[column].to_numpy()
        result_dict[strain_number[column]] = column_values

    return strain_number,result_dict

def write_strain_number(strain_number, temp_output_list):
    with open(temp_output_list, 'w') as f:
        for original_name, new_name in strain_number.items():
            f.write(f"{original_name}\t{new_name}\n")

def compare_and_replace(temp_file, final_file):
    if os.path.exists(final_file):
        with open(temp_file, 'r') as temp, open(final_file, 'r') as final:
            if temp.read() == final.read():
                os.remove(temp_file)
            else:
                print("Error: Temporary file and final file do not match.")
                os.remove(temp_file)
                raise ValueError("Files do not match.")
    else:
        os.replace(temp_file, final_file)

def write_output_file(result_dict,output_file,output_type):
    keys = list(result_dict.keys())
    num_keys = len(keys)
    value_length = len(result_dict[keys[0]])
    with open(output_file, 'w') as f:
        f.write("#NEXUS\n")
        f.write("Begin data;\n")
        f.write("\tDimensions ntax={} nchar={};\n".format(num_keys, value_length))
        if output_type == "S":
            f.write("\tFormat datatype=standard;\n")
            f.write("\tMatrix\n")
            for key in keys:
                values = "".join(map(str, result_dict[key]))
                f.write(f"\t{key}\t{values}\n")
        elif output_type == "C":
            f.write("\tFormat datatype=continuous;\n")
            f.write("\tMatrix\n")
            for key in keys:
                values = "\t".join(map(str, result_dict[key]))   
                f.write(f"\t{key}\t{values}\n")        

        f.write(";\nEND;\n")


if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    output_list = args.list
    output_type = args.type

    strain_number, result_dict = read_file(input_file)
    
    temp_output_list = output_list + '_temp'
    write_strain_number(strain_number, temp_output_list)
    compare_and_replace(temp_output_list, output_list)
    write_output_file(result_dict, output_file,output_type)
















```


```python
# 脚本名称 count_to_phy.py
# 输入文件夹count_to_distance

import argparse
import pandas as pd
import os

def normol_get():
    parser = argparse.ArgumentParser(description="python count_to_ss.py -i input_file  -o output_file -l strain_number.tsv -t datatype")
    parser.add_argument('-i','--input',help='输入文件,domain鉴定的文件')
    parser.add_argument('-o','--output',help='输出文件，用于POY构建系统发育的phylip文件')
    parser.add_argument('-l','--list',help='输出文件，物种编号文件')
    parser.add_argument('-t','--type',help='输出文件类型，分为standard和continuous;-t S // -t C')
    args = parser.parse_args()
    return args
def read_file(input_file, output_type):
    df = pd.read_csv(input_file, sep='\t')
    strain_number = {}
    result_dict = {}

    for i, column in enumerate(df.columns[1:], start=1):
        new_column_name = f'S{i:08d}'
        strain_number[column] = new_column_name
        column_values = df[column].to_numpy()
        
        if output_type == 'C':
            def transform_value(value):
                if value == 0:
                    return 0
                elif 1 <= value <= 10:
                    return 1
                elif 11 <= value <= 20:
                    return 2
                elif 21 <= value <= 30:
                    return 3
                elif 31 <= value <= 40:
                    return 4
                elif 41 <= value <= 50:
                    return 5
                elif 51 <= value <= 60:
                    return 6
                elif 61 <= value <= 70:
                    return 7
                elif 71 <= value <= 80:
                    return 8
                elif 81 <= value <= 90:
                    return 9
                else:
                    return 9

            # 使用 vectorize 函数将 transform_value 应用于 column_values
            transform_func = np.vectorize(transform_value)
            column_values = transform_func(column_values)
        
        result_dict[strain_number[column]] = column_values

    return strain_number, result_dict

def write_strain_number(strain_number, temp_output_list):
    with open(temp_output_list, 'w') as f:
        for original_name, new_name in strain_number.items():
            f.write(f"{original_name}\t{new_name}\n")

def compare_and_replace(temp_file, final_file):
    if os.path.exists(final_file):
        with open(temp_file, 'r') as temp, open(final_file, 'r') as final:
            if temp.read() == final.read():
                os.remove(temp_file)
            else:
                print("Error: Temporary file and final file do not match.")
                os.remove(temp_file)
                raise ValueError("Files do not match.")
    else:
        os.replace(temp_file, final_file)

def write_output_file(result_dict,output_file):
    keys = list(result_dict.keys())
    num_keys = len(keys)
    value_length = len(result_dict[keys[0]])
    with open(output_file, 'w') as f:
        f.write("{} {};\n".format(num_keys, value_length))
        for key in keys:
            values = "".join(map(str, result_dict[key]))
            f.write(f"\t{key}\t{values}\n")



if __name__ == '__main__':
    args = normol_get()
    input_file = args.input
    output_file = args.output
    output_list = args.list
    output_type = args.type

    strain_number, result_dict = read_file(input_file,output_type)
    
    temp_output_list = output_list + '_temp'
    write_strain_number(strain_number, temp_output_list)
    compare_and_replace(temp_output_list, output_list)
    write_output_file(result_dict, output_file)



```



POY的使用(windows版，linux安装暂时遇到困难，先不去管)




```shell


for i in $(find ../ss/ -type f -name "*.phy");do

bsub -q mpi -n 24 /scratch/wangq/llj/app/iqtree-2.3.5-Linux-intel/bin/iqtree2 -s ${i} -st MORPH -B 1000 -T 22


done




```


### PIDAN_Bacteria

#### 物种信息还原与数据库构建

```shell
# info.tsv
#name   id      rep     strain  size    annotation
# Desulfocu_africanus_DSM_2603_GCF_000422545_1_WP_005982748       WP_005982748.1  WP_005982748.1 Desulfocu_africanus_DSM_2603_GCF_000422545_1    97      DUF883 family protein
# Desulfocu_africanus_DSM_2603_GCF_000422545_1_WP_005982794       WP_005982794.1  WP_005982794.1  Desulfocu_africanus_DSM_2603_GCF_000422545_1    84      hypothetical protein


for i in $(cat info.tsv);do
    python3 specis_strains.py -i strain_domain/${i}.tsv -l ~/data/Bacteria/Protein/${i}/info.tsv -o strain_domain/${i}
done

```

```python
import argparse
import os

def normal_get():
    parser = argparse.ArgumentParser(description="python3 specis_starins.py -i input -l info.tsv -o output_dir")
    parser.add_argument('-i', '--input', help='输入文件，物种总的pro-domain文件')
    parser.add_argument('-l', '--list', help='物种文件')
    parser.add_argument('-o', '--output', help='输出文件夹')
    args = parser.parse_args()
    return args

def read_input(input_file):
    Protein_Da = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            Da = tuple(data[1:])
            protein_name = data[0]
            Protein_Da[protein_name] = Da
    return Protein_Da

def read_info(info_file, Protein_Da):
    strain_pro = {}
    with open(info_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            data = line.strip().split('\t')
            strain_name = data[3]
            pro_name = data[1]
            rep_name = data[2]
            if rep_name in Protein_Da:
                if strain_name in strain_pro:
                    strain_pro[strain_name][pro_name] = Protein_Da[rep_name]
                else:
                    strain_pro[strain_name] = {}
                    strain_pro[strain_name][pro_name] = Protein_Da[rep_name]
    return strain_pro

def write_out(strain_pro, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for species, proteins in strain_pro.items():
        output_file = os.path.join(output_dir, f"{species}.tsv")
        with open(output_file, 'w') as file:
            for pro_name, domains in proteins.items():
                file.write(f"{pro_name}\t{domains}\n")

if __name__ == '__main__':
    args = normal_get()
    input_file = args.input
    output_dir = args.output
    info_file = args.list

    Protein_Da = read_input(input_file)
    strain_pro = read_info(info_file, Protein_Da)
    write_out(strain_pro, output_dir)




```










