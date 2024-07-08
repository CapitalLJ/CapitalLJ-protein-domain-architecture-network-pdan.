#!/usr/bin bash

# 输入文件夹是distance文件,包括随机生成的自举文件
# 输出文件的子文件夹里分别为原始矩阵和随机自举矩阵两个文件
# 脚本文件为tsv文件转化为phylip文件，同时输出了物种名称替换文件。


input_dir=""
output_dir=""
Script="/scratch/wangq/llj/phylogentic/Script/tsvTophylip.py"


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
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
  echo "Usage: $0 -i <input_file> -o <output_dir>"
  exit 1
fi




# 去除 input_dir 末尾的斜杠（如果有）
if [ "${input_dir: -1}" == "/" ]; then
  input_dir="${input_dir%/}"
fi



# 去除 output_dir 末尾的斜杠（如果有）
if [ "${output_dir: -1}" == "/" ]; then
  output_dir="${output_dir%/}"
fi



# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
#     mkdir -p $output_dir/${i}
#     mkdir -p $output_dir/${i}_tmp
# done

# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
#     python3 $Script -i $input_dir/distance_${i}.txt -l $input_dir/phylip_strain_list -o $output_dir/${i}/${i}.phylip
# done

# for i in domain_count_01 domain_count_number domain_set_count_01 domain_set_count_number domain_content_count_01 domain_content_count_number;do
#     for y in $(ls $input_dir/${i});do
#         python3 $Script -i $input_dir/${i}/${y} -l  $input_dir/phylip_strain_list -o  $output_dir/${i}_tmp/${y}.phylip
#     done

#     for z in $(ls $output_dir/${i}_tmp);do
#         cat $output_dir/${i}_tmp/${z}>> $output_dir/${i}/boot_${i}.phylip
#     done

#     rm -rf $output_dir/${i}_tmp
# done



# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
#     mkdir -p $output_dir/pidan_01/pidan_${i}
#     mkdir -p $output_dir/pidan_01/pidan_${i}_tmp
# done

# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
#     python3 $Script -i $input_dir/pidan_01/distance_pidan_${i}.txt -l $input_dir/phylip_strain_list -o $output_dir/pidan_01/pidan_${i}/pidan_${i}.phylip
# done


# for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
#     for y in $(ls $input_dir/pidan_01/pidan_${i});do
#         python3 $Script -i $input_dir/pidan_01/pidan_${i}/${y} -l $input_dir/phylip_strain_list -o $output_dir/pidan_01/pidan_${i}_tmp/${y}.phylip
#     done

#     for z in $(ls $output_dir/pidan_01/pidan_${i}_tmp);do
#         cat $output_dir/pidan_01/pidan_${i}_tmp/${z} >> $output_dir/pidan_01/pidan_${i}/boot_${i}.phylip
#     done

#     rm -rf $output_dir/pidan_01/pidan_${i}_tmp
# done


for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    mkdir -p $output_dir/pidan_count/pidan_${i}
    mkdir -p $output_dir/pidan_count/pidan_${i}_tmp
done

for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    python3 $Script -i $input_dir/pidan_count/distance_pidan_${i}.txt -l $input_dir/phylip_strain_list -o $output_dir/pidan_count/pidan_${i}/pidan_${i}.phylip
done


for i in 0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95;do
    for y in $(ls $input_dir/pidan_count/pidan_${i});do
        python3 $Script -i $input_dir/pidan_count/pidan_${i}/${y} -l $input_dir/phylip_strain_list -o $output_dir/pidan_count/pidan_${i}_tmp/${y}.phylip
    done

    for z in $(ls $output_dir/pidan_count/pidan_${i}_tmp);do
        cat $output_dir/pidan_count/pidan_${i}_tmp/${z} >> $output_dir/pidan_count/pidan_${i}/boot_${i}.phylip
    done

    rm -rf $output_dir/pidan_count/pidan_${i}_tmp
done






