#!/bin/bash

number=1
while [ $number -le 10 ]
do
    echo "$number"
    number=$(( number+1 ))

done


number=1
until [ $number -gt 10 ]
do
    echo "$number"
    number=$(( number + 1 ))
done



echo 'for loops'

for i in {1..20}
do
    echo $i
done


for (( i=0; i<5; i++))
do
  if [ $i -gt 5 ]
  then
    break
  fi
  echo $i
done