#!/bin/bash

#本脚本嵌套了同目录下的scan_domainA.py，如有使用请注意。
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

if [ -e "$input_dir/scan.tsv" ]; then
  rm "$output_dir/scan.tsv"
fi

for i in $(ls $input_dir/tmp_scan/);do
    cat $input_dir/tmp_scan/${i} >> $output_dir/scan.tsv
done


rm $input_dir/tmp.list
rm $input_dir/split*
rm -rf $input_dir/tmp_scan
rm -rf $input_dir/tmp

python3 /scratch/wangq/llj/PIDAN_Bacteria/Script/scan_domainA.py -i $output_dir/scan.tsv -o $output_dir/domainA.tsv

protein_name=$(wc -l < $output_dir/domainA.tsv)

echo "domainA sequences: $protein_name" >> $output_dir/summary.txt