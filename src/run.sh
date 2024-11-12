#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_directory> <total_iterations>"
    exit 1
fi


output_directory=$1
total_iterations=$2


mkdir -p temp_save
touch temp_save/tem_ast.txt temp_save/temp.v


for (( i=1; i<=total_iterations; i++ ))
do

    mkdir -p "${output_directory}/${i}"


    bash run_main.sh "${output_directory}" "$i" > "${output_directory}/${i}/log.txt" 2>&1


    if (( i % 3 == 0 )); then
        echo "" > temp_save/tem_ast.txt
        echo "" > temp_save/temp.v
    fi
done

echo "All iterations completed."
