


calculate_score() {
	filename=$1
	while IFS= read -r line; do
		
	    # Use awk to process each line
	    label=$(echo $line | awk '{ print $1 }')
	    result=$(echo "$line" | awk '{
		result="Pass"
		for (i = 2; i <= NF; i++) {
			if ($i < 50){
			result="Fail"
			print result
			exit 1
		}
			
		}
		print result
	    }')


	if [ "$result" ==  "Pass" ]; then
		echo "$label : Pass"
	else
		echo "$label : Fail"
	fi

done < "$filename"
}


calculate_score $1
