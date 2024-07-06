#!/bin/bash

if [ "$#" -ne 3 ]; then
	echo "Usage $0 <tar-file> <new-file> <output-tar-file>"
	exit 1
fi

DIR_WORK="/tmp/testing"

TAR_FILE=$1
NEW_FILE=$2
OUTPUT_FILE=$3

mkdir /tmp/testing
chmod 755 "$DIR_WORK"

tar -xvf "$TAR_FILE" -C "$DIR_WORK"


if [ $? -ne 0 ]; then
	echo "Error Extracting Tar"
	exit 1
fi

touch "$DIR_WORK/$NEW_FILE"


tar -cvf "$DIR_WORK/$OUTPUT_FILE"  "$DIR_WORK" 

if [ $? -ne 0 ]; then
	echo "Error Extracting TAR"
	exit 1
fi

