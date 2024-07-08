#!/usr/bin/bash

# 上一步是DA_blast.sh，将算好距离的DA进行mcl聚类，建议在domainA_score文件夹里直接操作

input_file=""
output_dir="" 
Script="/scratch/wangq/llj/phylogentic/Script"  # 默认初始值
list="/scratch/wangq/llj/phylogentic/result/count_to_distance/list/DA_list.txt"

while getopts "i:o:s:l:" opt; do
  case $opt in
    i)
      input_file=$OPTARG
      ;;
    o)
      output_dir=$OPTARG
      ;;
    s)
      Script=$OPTARG
      ;;
    l)
      list=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_file>  -o <output_dir> [-s Script_dir] -l DA_list"
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_file" ] || [ -z "$output_dir" ]; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi

# 去除 output_dir 末尾的斜杠（如果有）
if [ "${output_dir: -1}" == "/" ]; then
  output_dir="${output_dir%/}"
fi

# 创建临时目录用于存储分解后的输入文件
tmp_dir="$output_dir/tmp"
mkdir -p "$tmp_dir"

mkdir -p "$output_dir/mcl"

# awk '$3 > 0' "$input_file" > "$tmp_dir/DA_0.tsv"

# 人为剔除低质量的点
# for i in 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95; do
#     awk -v threshold="$i" '$3 > threshold' "$input_file" > "$tmp_dir/DA_${i}.tsv"
# done



#mcl聚类
# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95; do
#     mcl $tmp_dir/DA_${i}.tsv --abc -I 2 -o $output_dir/mcl/mcl_${i}.tsv
# done

for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95; do
    python3 $Script/generate_pidan.py -i $output_dir/mcl/mcl_${i}.tsv -l $list -o $output_dir/mcl/pidan_${i}_list.txt
done
