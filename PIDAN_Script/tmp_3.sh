#!/usr/bin bash

diff -qr split 2_split/ | grep -E 'Only in|differ' | awk '{print $NF}' > split-3-tmp.list

for i in $(cat split-3-tmp.list);do
    for y in $(cat 2_split/${i});do
        bash Script/3_scan_to_domain.sh -i protein/${y} -o protein/${y}
    done
done

for i in $(cat split-3-tmp.list);do
    rm 2_split/${i}
done

mv output* log/

