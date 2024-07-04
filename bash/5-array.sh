#!/bin/bash

array=()
while IFS= read -r line; do
    array+=("$line")
done < "$1"

for (( i = 3; i <= 7 && i < ${#array[@]}; i++ ))
do
    echo -n "${array[i]} "
done

