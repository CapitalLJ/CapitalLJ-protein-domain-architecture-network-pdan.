#!/usr/bin bash

#物种数量太多，帮助进行任务上传,在/scratch/wangq/llj/PIDAN_Bacteria这一个目录下进行,实际是对
# 第2步的脚本进行上传

# tmp_2.sh和tmp_3.sh可以随意交替使用，但是注意不能有进行中的任务

ls split/ | head -n 2 > split-tmp.list

for i in $(cat split-tmp.list);do
    for y in $(cat split/${i});do
        bash Script/2_protein_scan.sh -i protein/${y} -o protein/${y}
    done
done

for i in $(cat split-tmp.list);do
    rm split/${i}
done
    