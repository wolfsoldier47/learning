filename="$1"

while IFS= read -r line || [ -n "$line" ]; do
    # Extract the label (first field)
    label=$(echo "$line" | awk '{print $1}')
    
    # Count the number of fields in the line (excluding the first field which is the label)
    num_values=$(echo "$line" | awk '{print NF-1}')
    
    # Check if there are only two numbers
    if [ "$num_values" -le 2 ]; then
        echo "Not all scores are available for $label"
    fi
done < "$filename"


