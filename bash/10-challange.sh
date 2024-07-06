#!/bin/bash

var=""
while read -r line ; do
    var+="$( echo "$line" | sed 's/$/\;/g')"
   
done


printf "%s" "$( echo "$var"  | sed 's/;$/''/g' )"
