#!/bin/bash
read -r num_integers

# Read the integers into an array
read -r -a integers

# Declare an associative array to store counts of each integer
declare -A count

# Count occurrences of each integer
for num in "${integers[@]}"; do
    (( count[$num]++ ))
    echo "${count[$num]}"
done

# Print out the non-occurring values
echo "Non-occurring values:"
for num in "${!count[@]}"; do
    if (( count[$num] == 1 )); then
        echo "$num"
    fi
done




#echo "$(</dev/stdin) | tr '' '\n' | sort | uniq -u
