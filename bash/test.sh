#!/bin/bash
read n
read -r input
echo "$(echo "$input" | tr ' ' '\n' | sort | uniq -u)"
