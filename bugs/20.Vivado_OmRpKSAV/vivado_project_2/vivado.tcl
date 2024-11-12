# 读取 Verilog 文件

read_verilog rtl.v

# 进行设计综合，不带任何额外参数

synth_design -top top

# 写入综合后的 Verilog 文件

write_verilog -force syn_vivado.v

# 创建仿真项目

create_project -force sim ./vivado_sim_test

# 添加综合后的 Verilog 文件到项目中

add_files -norecurse syn_vivado.v

# 设置 syn_vivado.v 为全局文件
set_property file_type {Verilog} [get_files syn_vivado.v]
set_property is_global_include 1 [get_files syn_vivado.v]

# 添加测试平台文件到仿真文件集

add_files -fileset sim_1 -norecurse vivado_testbench.v

# 导入文件到项目中

import_files -force -norecurse

# 设置仿真顶层模块

set_property top testbench [get_fileset sim_1]

# 添加 data 目录下的所有 .v 文件到项目并设置为全局文件
set data_files [glob -nocomplain ./data/*.v]
foreach file $data_files {
    add_files -norecurse $file
    set_property file_type {Verilog} [get_files $file]
    set_property is_global_include 1 [get_files $file]
}

# 启动仿真

launch_simulation


