#!/bin/bash

echo -n "Name of the file to write to: "
read filename

if [ -f $filename ]; then
    echo "WARNING: File exists"
fi

echo -n "Value of i: "
read max_i
echo -n "Value of j: "
read max_j

for (( i = 1; i <= $max_i; i++ ))
do
  for (( j = 1; j <= $max_j; j++ ))
  do
    echo "Will write ($i, $j). Press Enter when ready."
    read -n1 -s
    sudo python3 training_file_creator.py $filename $i $j 
  done
done
