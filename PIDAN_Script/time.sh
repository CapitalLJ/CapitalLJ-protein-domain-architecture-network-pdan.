#!/usr/bin/bash

count=0
for i in {1..1000}; do
    output=$(bjobs | wc -l)
    if [ "$output" -eq 0 ]; then
        let "count+=1"
        bash Script/tmp_2.sh
        echo "运行次数： $count"
    else
        sleep 1m
    fi
done