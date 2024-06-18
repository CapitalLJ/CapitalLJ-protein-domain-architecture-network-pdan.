# -*- encoding: utf-8 -*-
'''
@File    :   tsvTophylip.py
@Time    :   2024/06/11 10:47:28
@Author  :   Leilingjie 
@Version :   1.0
@Contact :   2438296284@qq.com
'''

# 该脚本用于对tsv文件格式的tsv距离矩阵文件转化为以空格为间隔的txt文件进行phylip系统发育树构建，因为
# phylip对于物种名称有字符限制，最多10个字符，因此使用S00000001进行物种名称替换，物种列表文件方便后续替换回来。
# here put the import lib
import argparse



def normol_get():
    parser = argparse.ArgumentParser(description="python tsvTophylip.py -i input_file  -l strain_list -o output_file")
    parser.add_argument('-i', '--input', help='输入文件,距离矩阵')
    parser.add_argument('-l', '--strain_list', help='输出文件,物种列表文件')
    parser.add_argument('-o', '--output', help='输出文件,pidan的有无鉴定')

    args = parser.parse_args()
    return args

def process_distance_matrix(input_file, matrix_output_file, mapping_output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 读取物种名称
    original_species = lines[0].strip().split()[0:]
    species_count = len(original_species)

    # 创建新的简短名称
    new_species = [f"S{str(i+1).zfill(8)}" for i in range(species_count)]
    
    # 创建物种名称映射
    species_mapping = dict(zip(original_species, new_species))

    # 创建输出内容
    matrix_output_lines = []
    matrix_output_lines.append(f" {species_count} \n")

    # 处理矩阵数据
    for i in range(1, len(lines)):
        line_data = lines[i].strip().split()
        original_name = line_data[0]
        new_name = species_mapping[original_name]
        distances = ' '.join(line_data[1:])
        matrix_output_lines.append(f"{new_name} {distances} \n")  # 末尾添加一个空格

    # 将矩阵输出内容写入文件
    with open(matrix_output_file, 'w') as f:
        f.writelines(matrix_output_lines)
    
    # 生成并写入物种名称映射文件
    with open(mapping_output_file, 'w') as f:
        for original_name, new_name in species_mapping.items():
            f.write(f"{original_name}\t{new_name}\n")
    
    print(f"Matrix output written to {matrix_output_file} with species count {species_count}.")
    print(f"Species mapping output written to {mapping_output_file}.")


def main():
    args = normol_get()

    input_file = args.input
    matrix_output_file = args.output
    mapping_output_file = args.strain_list
    process_distance_matrix(input_file, matrix_output_file, mapping_output_file)


if __name__ == "__main__":
    main()