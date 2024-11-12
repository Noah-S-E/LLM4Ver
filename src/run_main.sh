#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <output_directory> <fuzz_number>"
    exit 1
fi


output_directory=$1
fuzz_number=$2


mkdir -p "${output_directory}"


mkdir -p "${output_directory}/${fuzz_number}/identity" "${output_directory}/${fuzz_number}/vivado" "${output_directory}/${fuzz_number}/yosys" "${output_directory}/${fuzz_number}/simulation_identity" "${output_directory}/${fuzz_number}/simulation_vivado" "${output_directory}/${fuzz_number}/simulation_yosys" "${output_directory}/${fuzz_number}/equiv_identity_vivado" "${output_directory}/${fuzz_number}/equiv_identity_yosys"


python generate.py "${output_directory}/${fuzz_number}"

count_yosys=0

while [[ $count_yosys -lt 3 && $exit_code_yosys -ne 0 ]]; do
    cd "${output_directory}/${fuzz_number}/identity" || break
    yosys -p "read_verilog rtl.v;" > yosys_output.log 2> yosys_errors_${count_yosys}.log
    exit_code_yosys=$?
    if [ $exit_code_yosys -ne 0 ]; then
        echo "Yosys Check Error."
        cp rtl.v rtl_yosys_${count_yosys}.v 
        cd ../../../

        python error_feedback.py "${output_directory}/${fuzz_number}" "yosys" ${count_yosys}
    else
        echo "Yosys Check Success."
        cd ../../../
    fi
    ((count_yosys++))
done


if [[ $count_yosys -eq 3 && $exit_code_yosys -ne 0 ]]; then
    echo "Yosys错误反馈3次，仍然有错误"
fi

cd "${output_directory}/${fuzz_number}/identity/"
echo -e "read_verilog rtl.v\ncheck_syntax" > vivado_check.tcl
cd ../../../


count_vivado=0
exit_code_vivado=1

while [[ $count_vivado -lt 3 && exit_code_vivado -ne 0 ]]; do
    cd "${output_directory}/${fuzz_number}/identity" || break
    vivado -mode batch -source vivado_check.tcl > vivado_output.log 2> vivado_errors_${count_vivado}.log
    exit_code_vivado=$?
    if [ $exit_code_vivado -ne 0 ]; then
        echo "Vivado Check Error."
        cp rtl.v rtl_vivado_${count_vivado}.v  
        cd ../../../

        python error_feedback.py "${output_directory}/${fuzz_number}" "vivado" ${count_vivado}
    else
        echo "Vivado Check Success."
        cd ../../../
    fi
    ((count_vivado++))
done


if [[ $count_vivado -eq 3 && $exit_code_vivado -ne 0 ]]; then
    echo "Vivado error feedback 3 times, there are still errors"
fi

echo -e "### Verilog Code Check Finished ###.\n"


folders=('vivado' 'yosys' 'simulation_identity' 'simulation_vivado' 'simulation_yosys' 'equiv_identity_vivado' 'equiv_identity_yosys')

for folder in "${folders[@]}"; do
    target_folder="${output_directory}/${fuzz_number}/${folder}"
    if [ ! -d "${target_folder}" ]; then
        mkdir -p "${target_folder}"
    fi
    cp "${output_directory}/${fuzz_number}/identity/rtl.v" "${target_folder}/rtl.v"
done

cp "${output_directory}/${fuzz_number}/identity/rtl.v" "${output_directory}/${fuzz_number}/identity/syn_identity.v"


python synthesis.py "${output_directory}/${fuzz_number}"
if [ $? -ne 0 ]; then
    echo "Synthesis failed. Exiting."
fi

echo -e "### Starting Simulation ###\n"

cp "${output_directory}/${fuzz_number}/identity/syn_identity.v" "${output_directory}/${fuzz_number}/simulation_identity/syn_identity.v"
cp "${output_directory}/${fuzz_number}/yosys/syn_yosys.v" "${output_directory}/${fuzz_number}/simulation_yosys/syn_yosys.v"
cp "${output_directory}/${fuzz_number}/vivado/syn_vivado.v" "${output_directory}/${fuzz_number}/simulation_vivado/syn_vivado.v"

python testbench.py "${output_directory}/${fuzz_number}"

echo -e "\n\nRunning simulation for identity\n"

cd "${output_directory}/${fuzz_number}/simulation_identity/"
iverilog -o identity_main identity_testbench.v > icarus_stderr.log 2>&1
if [ $? -eq 0 ]; then
    echo "identity simulation iverilog Compilation Success"
    timeout 1m vvp -n identity_main > vvp.log
    if [ $? -eq 0 ]; then
        hash_value_identity=$(sha256sum vvp.log | cut -c1-16)
        echo "identity Simulation Success: Output Hash = $hash_value_identity"
    else
        echo "identity Simulation Timeout or Failed"
    fi
else
    echo "identity simulation iverilog Compilation Failed"
fi

cd ..

cd simulation_yosys/
echo -e "\nRunning simulation for yosys\n"
iverilog -o yosys_main yosys_testbench.v > icarus_stderr.log 2>&1
if [ $? -eq 0 ]; then
    echo "Yosys simulation iverilog Compilation Success"
    timeout 1m vvp -n yosys_main > vvp.log
    if [ $? -eq 0 ]; then
        hash_value_yosys=$(sha256sum vvp.log | cut -c1-16)
        echo "yosys Simulation Success: Output Hash = $hash_value_yosys"
    else
        echo "yosys Simulation Timeout or Failed"
    fi
else
    echo "Yosys simulation iverilog Compilation Failed"
fi

cd ..

cd simulation_vivado/
echo -e "\nRunning simulation for vivado\n"
iverilog -o vivado_main vivado_testbench.v > icarus_stderr.log 2>&1
if [ $? -eq 0 ]; then
    echo "Vivado simulation iverilog Compilation Success"
    timeout 1m vvp -n vivado_main > vvp.log
    if [ $? -eq 0 ]; then
        hash_value_vivado=$(sha256sum vvp.log | cut -c1-16)
        echo "Vivado Simulation Success: Output Hash = $hash_value_vivado"
    else
        echo "Vivado Simulation Timeout or Failed"
    fi
else
    echo "Vivado simulation iverilog Compilation Failed"
fi

echo "identity: $hash_value_identity    yosys: $hash_value_yosys    vivado: $hash_value_vivado"

cd ../../../
python AST.py "${output_directory}/${fuzz_number}"

cp "${output_directory}/${fuzz_number}/identity/ast.txt" "temp_save/tem_ast.txt"
cp "${output_directory}/${fuzz_number}/identity/rtl.v" "temp_save/temp.v"
