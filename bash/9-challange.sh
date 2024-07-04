#!/bin/bash
awk '{printf "%s", $0; if (NR % 3 == 0) print ""; else printf "\t"}' 
