#!/bin/bash
paste -d';' - - - | awk '{print $0}'
#var=""
#sum=1
#while read -r line || [ -n "$line" ]; do
#    if (( $sum % 3 == 0 ));then
#        var+="$( echo "$line" )"
#        var+="$(echo "\n")"
#    else
#    var+="$( echo "$line" | sed 's/$/\;/g')"
#    fi
#    sum+=1
   
#done


#printf "%s" "$( echo -e "$var"  | sed 's/;$/''/g'  )"

