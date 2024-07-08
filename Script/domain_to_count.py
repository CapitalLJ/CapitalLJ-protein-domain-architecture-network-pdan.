# -*- encoding: utf-8 -*-
'''
@File    :   domain_to_count.py
@Time    :   2024/06/23 16:51:25
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''




# here put the import lib
# 该脚本用于统计物种层面四个层次的domain结构信息
# 输入文件为scan的结果转化为domain的文件
# 输出文件夹，tmp文件存放中间文件


# 一、domain数量。（存在与计数）
# 二、domain_set的数量（存在与计数） 
# 三、domain_content的数量（存在与计数）



import argparse
import ast
import re
import os
import glob
import csv



def normol_get():
    parser = argparse.ArgumentParser(description="python domain_to_count.py -i input_dir  -o output_dir")
    parser.add_argument('-i','--input',help='输入文件,每个物种的蛋白记忆domain组成')
    parser.add_argument('-o','--output',help='输出文件夹，包括中间文件')
    args = parser.parse_args()
    return args

# 读取单个物种的输入文件脚本
def read_input(input_file):
    protein_data = {}
    with open(input_file, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            protein_name = data[0]
            domains = ast.literal_eval(data[1])
            protein_data[protein_name] = domains
    return protein_data

#将输入文件夹内的所有函数都读取存储到变量中，后续不再进行读取操作
def read_all_files(input_dir):
    species_data = {}
    file_paths = glob.glob(os.path.join(input_dir, '*.tsv'))
    for file_path in file_paths:
        if os.path.isfile(file_path):
            species_name = os.path.basename(file_path).replace('.tsv', '')
            protein_data = read_input(file_path)
            species_data[species_name] = protein_data
    return species_data


# ================================================================================

# domain鉴定，统计有多少个domain，结果存在output_dir/tmp/domain_list.txt中。
# 对输入文件夹里所有物种的domain进行提取，合并去重后统计，结果保存。
# 在这一步

def domain_intract(species_data, output_dir):
    domain_dir = {}
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            for domain in protein_data[protein]:
                if domain in domain_dir:
                    domain_dir[domain]+=1
                else:
                    domain_dir[domain]=1
        
    
    
    # 创建输出目录（如果不存在）
    output_path = os.path.join(output_dir, 'list')
    os.makedirs(output_path, exist_ok=True)
    
    # 写入输出文件
    with open(os.path.join(output_path, 'domain_list.txt'), 'w') as output_file:
        for domain in domain_dir:
            output_file.write(f'{domain}\t{domain_dir[domain]}\n')
    return domain_dir
    

### domain_set的鉴定，统计有多少个domain_set,结果存在output_dir/tmp/domain_set_list.txt中。
#集合只考虑组合的种类，不考虑位置和信息

def domain_set_intract(species_data, output_dir):
    domain_set_list = {}
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_dir=protein_data[protein]
            domain_set = tuple(sorted(set(domain_tmp_dir)))
            if domain_set in domain_set_list:
                domain_set_list[domain_set]+=1
            else:
                domain_set_list[domain_set]=1
    
    # 创建输出目录（如果不存在）
    output_path = os.path.join(output_dir, 'list')
    os.makedirs(output_path, exist_ok=True)
    
    # 写入输出文件
    with open(os.path.join(output_path, 'domain_set_list.txt'), 'w') as output_file:
        for domain_set in domain_set_list:
            output_file.write(f'{domain_set}\t{domain_set_list[domain_set]}\n')

    return domain_set_list


### domain_content的鉴定，统计有多少个domain_set,结果存在output_dir/tmp/domain_set_list.txt中。
#考虑组合的种类，位置和数量

def domain_count_intract(species_data, output_dir):
    domain_conunt_list = {}
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_dir=protein_data[protein]
            domain_content = tuple(domain_tmp_dir)
            if domain_content in domain_conunt_list:
                domain_conunt_list[domain_content]+=1
            else:
                domain_conunt_list[domain_content]=1


    # 创建输出目录（如果不存在）
    output_path = os.path.join(output_dir, 'list')
    os.makedirs(output_path, exist_ok=True)
    
    # 写入输出文件
    with open(os.path.join(output_path, 'domain_content_list.txt'), 'w') as output_file:
        for domain_conunt in domain_conunt_list:
            output_file.write(f'{domain_conunt}\t{domain_conunt_list[domain_conunt]}\n')

    return domain_conunt_list


def DA_list(species_data, output_dir,domain_content_list):

    output_path = os.path.join(output_dir, 'list')
    os.makedirs(output_path, exist_ok=True)

    DA__dictionary={}
    start=1000000
    with open(os.path.join(output_path, 'all_strain_DA_list.txt'), 'w') as output_file:
        for species_name, protein_data in species_data.items():
            for protein in protein_data:
                domain_tmp_dir=protein_data[protein]
                domain_content = tuple(domain_tmp_dir)
                if domain_content in DA__dictionary:
                    pass
                else:
                    DA__dictionary[domain_content]="DA"+str(start)
                    start += 1
                output_file.write(f'{protein}\t{DA__dictionary[domain_content]}\t{domain_content}\n')


    # 写入输出文件 DA列表文件
    with open(os.path.join(output_path, 'DA_list.txt'), 'w') as output_file:
        for domain_content, DA_value in DA__dictionary.items():
            output_file.write(f'{DA_value}\t{list(domain_content)}\n')
# ================================================================================


# domain 计数，根据统计到的domain的数量给每一个物种计数,只考虑0和1
def domain_infine(species_data,domain_list,output_dir):
    domain_dictionary = {species: {domain: 0 for domain in domain_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            for domain in protein_data[protein]:
                if domain in domain_list:
                    domain_dictionary[species_name][domain]=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'domain_count_01.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain'] + list(domain_dictionary.keys())
        writer.writerow(header)
        
        for domain in domain_list:
            row = [domain] + [domain_dictionary[species][domain] for species in domain_dictionary]
            writer.writerow(row)



# domain 计数，根据统计到的domain的数量给每一个物种计数,实际出现数量
def domain_count(species_data,domain_list,output_dir):
    domain_dictionary = {species: {domain: 0 for domain in domain_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            for domain in protein_data[protein]:
                if domain in domain_list:
                    domain_dictionary[species_name][domain]+=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)    
    with open(os.path.join(output_path, 'domain_count_number.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain'] + list(domain_dictionary.keys())
        writer.writerow(header)
        
        for domain in domain_list:
            row = [domain] + [domain_dictionary[species][domain] for species in domain_dictionary]
            writer.writerow(row)


#
# 统计到的domain_set的数量给每一个物种计数,只考虑0和1
def domain_set_infine(species_data,domain_set_list,output_dir):
    domain_set_dictionary = {species: {domain_set: 0 for domain_set in domain_set_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_set = tuple(sorted(set(protein_data[protein])))
            if domain_tmp_set in domain_set_list:
                    domain_set_dictionary[species_name][domain_tmp_set]=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'domain_set_count_01.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain_set'] + list(domain_set_dictionary.keys())
        writer.writerow(header)
        
        for domain_set in domain_set_list:
            row = [domain_set] + [domain_set_dictionary[species][domain_set] for species in domain_set_dictionary]
            writer.writerow(row) 


#domain_set 计数 ，根据统计到的domain_set的数量给每一个物种计数,实际出现数量
def domain_set_count(species_data,domain_set_list,output_dir):
    domain_set_dictionary = {species: {domain_set: 0 for domain_set in domain_set_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_set = tuple(sorted(set(protein_data[protein])))
            if domain_tmp_set in domain_set_list:
                    domain_set_dictionary[species_name][domain_tmp_set]+=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'domain_set_count_number.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain_set'] + list(domain_set_dictionary.keys())
        writer.writerow(header)
        
        for domain_set in domain_set_list:
            row = [domain_set] + [domain_set_dictionary[species][domain_set] for species in domain_set_dictionary]
            writer.writerow(row) 

# domain_content 计数，根据统计的domain_content的数量给每一个物种计数,只考虑0和1
def domain_content_infine(species_data,domain_content_list,output_dir):

    domain_content_dictionary = {species: {domain_content: 0 for domain_content in domain_content_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_content = tuple(sorted(set(protein_data[protein])))
            if domain_tmp_content in domain_content_list:
                    domain_content_dictionary[species_name][domain_tmp_content]=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'domain_content_count_01.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain_content'] + list(domain_content_dictionary.keys())
        writer.writerow(header)
        
        for domain_content in domain_content_list:
            row = [domain_content] + [domain_content_dictionary[species][domain_content] for species in domain_content_dictionary]
            writer.writerow(row)  


# domain_content 计数，根据统计的domain_content的数量给每一个物种计数,实际出现数量
def domain_content_count(species_data,domain_content_list,output_dir):

    domain_content_dictionary = {species: {domain_content: 0 for domain_content in domain_content_list} for species in species_data}
    
    for species_name, protein_data in species_data.items():
        for protein in protein_data:
            domain_tmp_content = tuple(sorted(set(protein_data[protein])))
            if domain_tmp_content in domain_content_list:
                    domain_content_dictionary[species_name][domain_tmp_content]+=1
    output_path = os.path.join(output_dir, 'count')
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'domain_content_count_number.txt'), 'w', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        header = ['Domain_content'] + list(domain_content_dictionary.keys())
        writer.writerow(header)
        
        for domain_content in domain_content_list:
            row = [domain_content] + [domain_content_dictionary[species][domain_content] for species in domain_content_dictionary]
            writer.writerow(row)  






# ================================================================================



if __name__ == '__main__':

    args = normol_get()
    input_dir = args.input
    output_dir = args.output
    species_data = read_all_files(input_dir)  # 读取输入文件夹内所有物种。


    domain_list=domain_intract(species_data, output_dir)  #统计并输出domain列表
    domain_set_list=domain_set_intract(species_data, output_dir) #统计并输出domain_set列表
    domain_content_list=domain_count_intract(species_data, output_dir) #统计并输出domain_count列表
    DA_list(species_data, output_dir,domain_content_list)  # 输出DA列表文件和对应的domain_count,从DA1000000开始




# 第一个层次，domain数量
    domain_infine(species_data,domain_list,output_dir)
    domain_count(species_data,domain_list,output_dir)

# 第二个层次，domain_set ,只考虑种类，不考虑数量和顺序
    domain_set_infine(species_data,domain_set_list,output_dir)
    domain_set_count(species_data,domain_set_list,output_dir)

# 第三个层次，domain_count ，考虑种类，考虑数量和顺序
    domain_content_infine(species_data,domain_content_list,output_dir)
    domain_content_count(species_data,domain_content_list,output_dir)