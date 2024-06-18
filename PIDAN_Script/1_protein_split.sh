#!/bin/bash

# 初始化变量
input_file=""
output_file=""
threads=120  #默认初始值是120 (24*5)

# 解析命令行选项
# -i 输入文件，压缩的物种蛋白文件.gz
# -j 线程数
# -o 输出文件夹

while getopts "i:j:o:" opt; do
  case $opt in
    i)
      input_file=$OPTARG
      ;;
    j)
      threads=$OPTARG
      ;;
    o)
      output_dir=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_file> -j threasd(24n) -o <output_dir>"
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_file" ] || [ -z "$output_dir" ]; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi


file_nums=$(($threads/2))  # 分解的文件数


# 创建输出目录和 tmp 子目录
tmp_dir="$output_dir/tmp"
mkdir -p "$tmp_dir"

# 计算总的序列数
total_sequences=$(zcat "$input_file" | grep -c '^>')

# 计算每个文件应包含的序列数
sequences_per_file=$(( (total_sequences + file_nums - 1) / file_nums ))

# 输出传入的参数
# echo "Input file: $input_file"
# echo "Number of threads: $threads"
# echo "Output directory: $output_dir"
echo "Total sequences: $total_sequences" >> $output_dir/summary.txt
# echo "Sequences per file: $sequences_per_file"



# 输入文件是物种内的所有蛋白（降维过后），首先将其分解为指定数量的文件
# 使用 awk 进行拆分
zcat "$input_file" | awk -v tmp_dir="$tmp_dir" -v prefix="$(basename "${input_file%.*}")" -v sequences_per_file="$sequences_per_file" '
BEGIN {
  part = 0;
  seq_count = 0;
  filename = tmp_dir "/" prefix "_part" part ".fa.gz";
}
{
  if (/^>/) {
    seq_count++;
    if (seq_count > sequences_per_file) {
      part++;
      seq_count = 1;
      filename = tmp_dir "/" prefix "_part" part ".fa.gz";
    }
  }
  print $0 | "gzip >> " filename;
}
'

echo "拆分完成。所有部分已保存到目录: $tmp_dir"


