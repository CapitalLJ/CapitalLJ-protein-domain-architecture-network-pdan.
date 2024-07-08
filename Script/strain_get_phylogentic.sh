#!/usr/bin/bash

# 此脚本用于根据nwr对物种系统发育进行查询

input_file="strain.list"
output_file="output.tsv"

while getopts "i:o:s:" opt; do
  case $opt in
    i)
      input_file=$OPTARG  
      ;;
    o)
      output_file=$OPTARG
      ;;
    s)
      script_file=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_file>  -o <output_file> -s <script_file>"
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_file" ] || [ -z "$output_file" ]; then
  echo "Usage: $0 -i <input_file> -o <output_file>"
  exit 1
fi

# 写入TSV文件的表头
echo -e "Species_Name\tSuperkingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies" > "$output_file"

while IFS= read -r species_name; do
    tmp_file=$(mktemp)
    nwr lineage "${species_name}" > $tmp_file

    superkingdom=""
    phylum=""
    class=""
    order=""
    family=""
    genus=""
    species=""

    while IFS=$'\t' read -r rank name _; do
        case $rank in
            "superkingdom")
                superkingdom=$name
                ;;
            "phylum")
                phylum=$name
                ;;
            "class")
                class=$name
                ;;
            "order")
                order=$name
                ;;
            "family")
                family=$name
                ;;
            "genus")
                genus=$name
                ;;
            "species")
                species=$name
                ;;
        esac
    done < <(tail -n +2 $tmp_file)

    echo -e "${species_name}\t${superkingdom}\t${phylum}\t${class}\t${order}\t${family}\t${genus}\t${species}" >> "$output_file"

    rm $tmp_file
done < "$input_file"

echo "结果已写入 $output_file"