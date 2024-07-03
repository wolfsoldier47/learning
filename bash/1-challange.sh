#!/bin/bash

# printing third character from each file


if [ -z "$1" ]; then
	echo "USAGE: $0 filename"
fi

filename="$1"

if [ ! -r "$filename" ]; then
	echo "File $filename does not exist or cant be read"
	exit 1
fi

#while read -r line; do
#  echo "$line" | cut -c3
#done < "$filename"

while IFS= read -r line || [ -n "$line" ]; do
    echo "$line" | rev
done

while read -r line; do
    printf "%s" "$( echo "$line" | sed -e 's/[0-9]\{4\} [0-9]\{4\} [0-9]\{4\} \([0-9]\{4\}\)/**** **** **** \1/')"
    echo ""
done < "$filename"

#while IFS= read -r line; do
#	echo "$line" | cut -c3
#done < "$filename" 
