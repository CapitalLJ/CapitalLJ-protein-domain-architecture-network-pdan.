#!/usr/bin/bash

# 准备文件夹 domainA_score ，里面包含一个 domain_score.tsv 是所有结构域的打分文件
# 这是将进行了DA鉴定后的结果进行blast算出不同DA间距离的脚本
# 上一步是进行domain_to_count.py，将这个脚本生成的DA_list作为输入


input_file=""
output_dir=""
threads=20  # 默认初始值是 20，分解的文件数量
script_file="/scratch/wangq/llj/phylogentic/Script/blast.py"

while getopts "i:o:s:" opt; do
  case $opt in
    i)
      input_file=$OPTARG  
      ;;
    o)
      output_dir=$OPTARG
      ;;
    s)
      script_file=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_dir>  -o <output_dir> -s <script_file>"
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

total_lines=$(wc -l < $input_file)

lines_per_file=$(( (total_lines + 19) / 20 ))

split -l $lines_per_file -d $input_file $tmp_dir/split

parallel_script="$output_dir/run_parallel.sh"

echo "parallel -j 23 \"  python3 $script_file -i  $tmp_dir/{1} -I $input_file -s $output_dir/domain_score.tsv -o $output_dir/{1}.tsv\" ::: \$(ls $tmp_dir/)" > "$parallel_script"
# 给并行脚本添加执行权限
chmod +x $parallel_script

bsub -q mpi -n 24 bash $parallel_script 