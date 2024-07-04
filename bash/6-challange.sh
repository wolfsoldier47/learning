#!/bin/bash
array=()
while read -r line || [ -n "$line" ]; do
    array+=("$line")
done

for ((i=0;i<${#array[@]};i++ ))
do
    echo -n "$(echo ${array[i]} | sed 's/^\s*././g'   ) "
done
