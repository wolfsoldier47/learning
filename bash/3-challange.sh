#!/bin/bash

while IFS= read -r line || [ -n "$line" ]; do
	printf "%s" $(echo $line | grep -v -i 'a' )
done < "$1"
