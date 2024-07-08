#!/usr/bin bash

# 该文件夹用于phylip的脚本化

# 输入文件为Domain_tree文件夹，子文件为原始phylip文件和随机boot文件
# 输出文件有三个，原始树，boot树集合以及带有自举的树.部分脚本和变量为默认初始值，后续可更改

input_dir=""
Script="/scratch/wangq/llj/phylogentic/Script/boottree.py"
replace_script="/scratch/wangq/llj/phylogentic/Script/tree_namereplace.py"
list_file="/scratch/wangq/llj/phylogentic/result/cos_distance/phylip_strain_list"

while getopts "i:o:s:" opt; do
  case $opt in
    i)
      input_dir=$OPTARG  
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
if [ -z "$input_dir" ] ; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi

# 去除 input_dir 末尾的斜杠（如果有）
if [ "${input_dir: -1}" == "/" ]; then
  input_dir="${input_dir%/}"
fi


CURRENT_DIR=$(pwd)

# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
# OUTPUT_FILE=$input_dir/${i}/nj.par

# cat <<EOL > "$OUTPUT_FILE"
# ${i}.phylip
# Y #确认以上设定的参数
# EOL

# OUTPUT_FILE2=$input_dir/${i}/boot_nj.par

# cat <<EOL > "$OUTPUT_FILE2"
# boot_${i}.phylip
# M #选择
# 100
# 9 #随机数
# Y #确认以上设定的参数
# EOL

# done



# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
#     cd $input_dir/${i}
#     ~/llj/phylip-3.697/exe/neighbor < nj.par
#     rm outfile
#     mv outtree query.newick
#     ~/llj/phylip-3.697/exe/neighbor < boot_nj.par
#     rm outfile
#     mv outtree boot.newick

#     python3 $Script -q query.newick -i boot.newick -o ${i}.newick.tmp

#     cd $CURRENT_DIR
# done

# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
#     python3 $replace_script -i $input_dir/${i}/${i}.newick.tmp -l $list_file -o   $input_dir/${i}/${i}.newick
# done


# ==========================================================

# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
# OUTPUT_FILE3=$input_dir/pidan_01/pidan_${i}/nj.par
# cat <<EOL > "$OUTPUT_FILE3"
# pidan_${i}.phylip
# Y #确认以上设定的参数
# EOL

# OUTPUT_FILE4=$input_dir/pidan_01/pidan_${i}/boot_nj.par

# cat <<EOL > "$OUTPUT_FILE4"
# boot_${i}.phylip
# M #选择
# 100
# 9 #随机数
# Y #确认以上设定的参数
# EOL


# done




# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
#     cd $input_dir/pidan_01/pidan_${i}
#     ~/llj/phylip-3.697/exe/neighbor < nj.par
#     rm outfile
#     mv outtree query.newick
#     ~/llj/phylip-3.697/exe/neighbor < boot_nj.par
#     rm outfile
#     mv outtree boot.newick

#     python3 $Script -q query.newick -i boot.newick -o pidan_${i}.newick.tmp

#     cd $CURRENT_DIR

# done

# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
#     python3 $replace_script -i $input_dir/pidan_01/pidan_${i}/pidan_${i}.newick.tmp -l $list_file -o   $input_dir/pidan_01/pidan${i}.newick
# done




# ==============================================







for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
OUTPUT_FILE3=$input_dir/pidan_count/pidan_${i}/nj.par
cat <<EOL > "$OUTPUT_FILE3"
pidan_${i}.phylip
Y #确认以上设定的参数
EOL

OUTPUT_FILE4=$input_dir/pidan_count/pidan_${i}/boot_nj.par

cat <<EOL > "$OUTPUT_FILE4"
boot_${i}.phylip
M #选择
100
9 #随机数
Y #确认以上设定的参数
EOL


done




for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    cd $input_dir/pidan_count/pidan_${i}
    ~/llj/phylip-3.697/exe/neighbor < nj.par
    rm outfile
    mv outtree query.newick
    ~/llj/phylip-3.697/exe/neighbor < boot_nj.par
    rm outfile
    mv outtree boot.newick

    python3 $Script -q query.newick -i boot.newick -o pidan_${i}.newick.tmp

    cd $CURRENT_DIR

done

for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    python3 $replace_script -i $input_dir/pidan_count/pidan_${i}/pidan_${i}.newick.tmp -l $list_file -o   $input_dir/pidan_count/pidan${i}.newick
done