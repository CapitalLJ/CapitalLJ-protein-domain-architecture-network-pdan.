#!/usr/bin bash

# 运行目录：/scratch/wangq/llj/phylogentic
# 对下载的185种细菌进行bac120串联树的构建


strain_list="/scratch/wangq/llj/phylogentic/result/strain.list"  # 物种列表文件

while getopts "i:o:l:" opt; do
  case $opt in
    i)
      input_dir=$OPTARG   # data文件夹
      ;;
    o)
      output_dir=$OPTARG
      ;;
    l)
      strain_list=$OPTARG
      ;;
    *)
      echo "Usage: $0 -i <input_dir>  -o <output_dir> -l <strain_list>"
      exit 1
      ;;
  esac
done

# 检查是否提供了必须的参数
if [ -z "$input_dir" ] || [ -z "$output_dir" ] ; then
  echo "Usage: $0 -i <input_dir> -o <output_dir>"
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

E_VALUE=1e-20

# for marker in $(cat HMM/marker.lst); do
#     echo >&2 "==> marker [${marker}]"
#     mkdir -p $output_dir/Domain/${marker}

#     cat $strain_list | parallel  -j 8 "
#         gzip -dcf $input_dir/{}/*_protein.faa.gz | 
#             hmmsearch -E ${E_VALUE} --domE ${E_VALUE} --noali --notextw HMM/hmm/${marker}.HMM - |
#             grep '>>' |
#             perl -nl -e ' m(>>\s+(\S+)) and printf qq(%s\t%s\n), \$1, \"{}\"; '
#         " > $output_dir/Domain/${marker}/replace.tsv
#     echo >&2
# done


# for i in $(cat $strain_list);do
#     cat $input_dir/${i}/*_protein.faa.gz
# done > $output_dir/Domain/all.uniq.fa.gz


# cat HMM/marker.lst |
#     parallel --no-run-if-empty --linebuffer -k -j 4 '
#         cat bac120/Domain/{}/replace.tsv |
#             wc -l
#     ' |
#     tsv-summarize --quantile 1:0.25,0.5,0.75

# 184     186     266


# cat HMM/marker.lst |
#     parallel --no-run-if-empty --linebuffer -k -j 4 "
#         echo {}
#         cat $output_dir/Domain/{}/replace.tsv |
#             wc -l
#     " |
#     paste - - |
#     tsv-filter --invert --ge 2:170 --le 2:200 |
#     cut -f 1 \
#     > $output_dir/Domain/marker.omit.lst


# cat HMM/marker.lst |
#     grep -v -Fx -f $output_dir/Domain/marker.omit.lst |
#     parallel --no-run-if-empty --linebuffer -k -j 4 "

#         cat $output_dir/Domain/{}/replace.tsv \
#             > $output_dir/Domain/{}/{}.replace.tsv

#         faops some $output_dir/Domain/all.uniq.fa.gz <(
#             cat $output_dir/Domain/{}/{}.replace.tsv |
#                 cut -f 1 |
#                 tsv-uniq
#             ) stdout \
#             > $output_dir/Domain/{}/{}.pro.fa
#     "
    

# cat HMM/marker.lst |
#     parallel --no-run-if-empty --linebuffer -k -j 8 "
#         echo >&2 "==> marker [{}]"
#         if [ ! -s $output_dir/Domain/{}/{}.pro.fa ]; then
#             exit
#         fi
#         if [ -s $output_dir/Domain/{}/{}.aln.fa ]; then
#             exit
#         fi

#         mafft --auto $output_dir/Domain/{}/{}.pro.fa > $output_dir/Domain/{}/{}.aln.fa
#     "



# for marker in $(cat HMM/marker.lst); do
#     echo >&2 "==> marker [${marker}]"
#     if [ ! -s $output_dir/Domain/${marker}/${marker}.pro.fa ]; then
#         continue
#     fi

#     # sometimes `muscle` can not produce alignments
#     if [ ! -s $output_dir/Domain/${marker}/${marker}.aln.fa ]; then
#         continue
#     fi

#     # 1 name to many names
#     cat $output_dir/Domain/${marker}/${marker}.replace.tsv |
#         tsv-select -f 1-2 |
#         parallel --no-run-if-empty --linebuffer -k -j 4 "
#             faops replace -s $output_dir/Domain/${marker}/${marker}.aln.fa <(echo {}) stdout
#         " \
#         > $output_dir/Domain/${marker}/${marker}.replace.fa
# done



# for marker in $(cat HMM/marker.lst); do
#     if [ ! -s $output_dir/Domain/${marker}/${marker}.pro.fa ]; then
#         continue
#     fi
#     if [ ! -s $output_dir/Domain/${marker}/${marker}.aln.fa ]; then
#         continue
#     fi

#     # sequences in one line
#     faops filter -l 0 $output_dir/Domain/${marker}/${marker}.replace.fa stdout

#     # empty line for .fas
#     echo
# done \
#     > $output_dir/Domain/bac120.aln.fas

# cat $strain_list | fasops concat $output_dir/Domain/bac120.aln.fas stdin -o $output_dir/Domain/bac120.aln.fa

# trimal -in  $output_dir/Domain/bac120.aln.fa -out  $output_dir/Domain/bac120.trim.fa -automated1


# FastTree -fastest -noml $output_dir/Domain/bac120.trim.fa > $output_dir/Domain/bac120.trim.newick



