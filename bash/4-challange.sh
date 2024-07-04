#!/bin/bash
array=()
while read -r line || [ -n "$line" ]; do
    array+=("$line")
done
new_array=()
for ((i=0;i<3;i++))
do
    new_array+=("${array[@]}")
done

echo "${new_array[@]}"
