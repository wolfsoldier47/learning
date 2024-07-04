#!/bin/bash

# Loop through each SCSI host and trigger a rescan
for host in /sys/class/scsi_host/host*; do
    echo "---" "$host/scan" 
done


for files in $(ls); do
	if [ "$files" == "scan.sh" ]; then
	echo "$files got it"
	fi
done
