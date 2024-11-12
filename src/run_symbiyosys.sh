#!/bin/bash


if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <work_dir> <file1.v> <file2.v> <file3.v>"
    exit 1
fi


cd $1


cat << EOF > proof.sby
[options]
multiclock on
mode prove

[engines]
abc pdr

[script]
read -formal $2
read -formal $3
read -formal $4
read -formal cells_xilinx_7.v
prep -top equiv

[files]
$2
$3
$4
../../../data/cells_xilinx_7.v
EOF


sby -f proof.sby > sby.log 2>&1

if [ $? -eq 0 ]; then
    echo "Equiv Success"
else
    echo "Equiv Failed"
fi
