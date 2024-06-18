#!/bin/bash

#本脚本嵌套了同目录下的scan.sh，如有使用请注意。
# 初始化变量
input_dir=""
output_dir=""

# 解析命令行选项
# -i 输入文件夹，分解的蛋白文件。（一般在tmp文件里）
# -j 线程数
# -o 输出文件夹
# -d pafm比对数据库（需要提前构建索引），默认值可以自己更改。


while getopts "i:o:" opt; do
  case $opt in
    i)
      input_dir=$OPTARG
      ;;
    o)
      output_dir=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_dir>  -o <output_dir> "
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi


# 创建临时输出目录,用于存放分解的子文件的hmmscan，后续合并。
tmp_dir="$output_dir/tmp_scan"
mkdir -p "$tmp_dir"


ls "$input_dir/tmp" > "$input_dir/tmp.list"
split -l 12 -d "$input_dir/tmp.list" "$input_dir/split"

for i in $(ls $input_dir/split*);do
bsub -q mpi -n 24 bash /scratch/wangq/llj/PIDAN_Bacteria/Script/scan.sh -i $input_dir -l ${i} -o $output_dir/tmp_scan 
done

# rm $input_dir/../tmp.list
# rm $input_dir/../split*

