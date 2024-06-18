#!/usr/bin bash

db="/scratch/wangq/llj/phylogentic/pfam/Pfam-A.hmm" # (默认数据库，可更改)

while getopts "i:o:l:d:" opt; do
  case $opt in
    i)
      input_dir=$OPTARG
      ;;
    o)
      output_dir=$OPTARG
      ;;
    d)
      db=$OPTARG
      ;;
    l)
      list=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_dir> -l list_file -o <output_dir>"
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_dir" ] || [ -z "$output_dir" ] || [ -z "$list" ]; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi



cat $list | 
parallel --no-run-if-empty --linebuffer -k -j 6 "
hmmscan -E 1e-5 --domE 1e-5 --cpu 4 --domtblout $output_dir/{}.tsv /scratch/wangq/llj/phylogentic/pfam/Pfam-A.hmm $input_dir/tmp/{} > /dev/null
"
