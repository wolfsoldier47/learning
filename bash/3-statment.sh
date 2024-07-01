#!/bin/bash

count=10

if [ $count -eq 10 ]
then
    echo "the condition has met"
else
    echo "not 10"
fi


if (( $count > 9 ))
then
  echo "true"
else
  echo "false"

fi



if (( $count > 9 ))
then 
  echo "this is true"
elif (( $count <= 9 ))
then
    echo "this is false"
else
    echo "false boy"
fi

age=40

if [ $age -gt 18 ] && [ $age -lt 40 ]
then
    echo "Age is correct"
else
    echo "Age is not correct"
fi



if [ $age -gt 18 ] || [ $age -lt 40 ]
then
    echo "Age is correct"
else
    echo "Age is not correct"
fi

if [ $age -gt 18 -o $age -lt 40 ]
then
    echo "Age is correct"
else
    echo "Age is not correct"
fi

if [[ $age -gt 18 || $age -lt 40 ]]
then
    echo "Age is correct double"
else
    echo "Age is not correct"
fi