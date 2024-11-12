#!/bin/bash

# 创建文件夹
mkdir -p identity
mkdir -p yosys
mkdir -p vivado

# 复制文件并插入代码
function prepare_folder() {
    local testbench=$1
    local syn_file=$2
    local folder=$3
    local wave_file="wave_${folder}"

    # 复制文件
    cp ${testbench}.v ${folder}/${testbench}.v
    cp rtl.v ${folder}/rtl.v
    cp ${syn_file}.v ${folder}/${syn_file}.v

    # 在endmodule前插入代码
    awk -v wave_file="${wave_file}" '
        /endmodule/ {
            print "  initial"
            print "    begin"
            print "      $dumpfile(\"" wave_file ".vcd\");"
            print "      $dumpvars(0, testbench);"
            print "    end"
        }
        { print }
    ' ${folder}/${testbench}.v > ${folder}/${testbench}_temp.v

    # 替换原始文件
    mv ${folder}/${testbench}_temp.v ${folder}/${testbench}.v
}

# 处理各个文件夹
prepare_folder "identity_testbench" "rtl" "identity"
prepare_folder "yosys_testbench" "syn_yosys" "yosys"
prepare_folder "vivado_testbench" "syn_vivado" "vivado"

# 进入各个文件夹并执行命令
cd identity
iverilog -o identity_main identity_testbench.v > icarus_stderr.log 2>&1
vvp -n identity_main -lxt2 > vvp_identity.log
cd ..

cd yosys
iverilog -o yosys_main yosys_testbench.v > icarus_stderr.log 2>&1
vvp -n yosys_main -lxt2 > vvp_yosys.log
cd ..

cd vivado
iverilog -o vivado_main vivado_testbench.v > icarus_stderr.log 2>&1
vvp -n vivado_main -lxt2 > vvp_vivado.log
cd ..

