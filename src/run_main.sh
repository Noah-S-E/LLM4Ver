#!/bin/bash

# ===================== Style Definitions =====================
BORDER="╔══════════════════════════════════════════════════╗
║                VERILOG FUZZING RUN               ║
╚══════════════════════════════════════════════════╝"
SECTION_HEADER="▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄"
SECTION_FOOTER="▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"

# ===================== Global Variables =====================
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# ===================== Helper Functions =====================
print_header() {
    echo "$BORDER"
    echo "[📁] Output Directory: $(realpath "$1")"
    echo "[🔢] Fuzz Number: $2"
    echo "[🕒] Start Time: $(date '+%Y-%m-%d %H:%M:%S')"
    echo
}

print_section() {
    echo "$SECTION_HEADER"
    printf "█ %-48s █\n" "$1"
    echo "$SECTION_FOOTER"
}

print_check() {
    case $1 in
        0) echo "✔️ Success (${2:-1} attempt$([[ $2 -gt 1 ]] && echo s))";;
        *) echo "❌ Failed (${2:-1} attempt$([[ $2 -gt 1 ]] && echo s))";;
    esac
}

safe_cd() {
    # Safely change directory with error checking
    cd "$1" || {
        echo "❌ Failed to enter directory: $1"
        exit 1
    }
}

# ===================== Main Function =====================
main() {
    # Record start time for duration calculation
    local start_time=$(date +%s)
    
    # Validate input parameters
    if [ "$#" -ne 2 ]; then
        echo "Usage: $0 <output_directory> <fuzz_number>"
        exit 1
    fi

    # Initialize paths
    local output_directory=$(realpath "$1")
    local fuzz_number=$2
    local work_dir="${output_directory}/${fuzz_number}"

    # Setup logging
    mkdir -p "$work_dir"
    exec > >(tee "${work_dir}/log.txt") 2>&1
    print_header "$output_directory" "$fuzz_number"

    # ===================== Directory Initialization =====================
    print_section "INITIALIZATION"
    local subdirs=(identity vivado yosys 
                  simulation_identity simulation_vivado simulation_yosys
                  equiv_identity_vivado equiv_identity_yosys)
    
    for dir in "${subdirs[@]}"; do
        mkdir -p "${work_dir}/${dir}" || {
            echo "❌ Failed to create directory: ${work_dir}/${dir}"
            exit 1
        }
    done
    echo "✅ Directory structure created successfully"

    # ===================== Verilog Generation =====================
    print_section "GENERATION"
    local gen_start=$(date +%s)
    if ! python "${SCRIPT_DIR}/generate.py" "$work_dir"; then
        echo "❌ Verilog generation failed"
        exit 1
    fi
    echo "✅ Verilog generation completed ($(($(date +%s) - gen_start))s)"

    # ===================== Syntax Checks =====================
    print_section "SYNTAX CHECKS"
    echo "[🔍] Running syntax checks:"
    local check_start=$(date +%s)
    # echo $work_dir
    # echo "${work_dir}/../.."
    # Yosys syntax check with retry logic
    
    local yosys_check=1
    local yosys_attempts=0
    local yosys_exit_code=1
    while (( yosys_attempts < 3 )); do
        safe_cd "${work_dir}/identity" || exit 1

        local yosys_err_log="./yosys_errors_${yosys_attempts}.log"
        yosys -p "read_verilog rtl.v" > ./yosys_output.log 2> "${yosys_err_log}"
        yosys_exit_code=$?
        
        if [[ $yosys_exit_code -eq 0 ]]; then
            rm -f "${yosys_err_log}"
            echo "  ├─ Yosys:   $(print_check 0 $((yosys_attempts+1)))"
            break
        else
            cp rtl.v "./rtl_yosys_${yosys_attempts}.v"
            python "${SCRIPT_DIR}/error_feedback.py" "$work_dir" "yosys" ${yosys_attempts}
            echo "  ├─ Yosys Attempt $((yosys_attempts+1)) failed. Retrying..."
        fi

        ((yosys_attempts++))
        
    done
    
    if (( yosys_attempts >= 3 && yosys_exit_code != 0 )); then
    echo "  ├─ Yosys:   $(print_check 1 3)"
    yosys_check = 0
    # exit 1  # Maybe Vivado check success
    fi

    # Vivado syntax check with retry logic
    local vivado_attempts=0
    local vivado_exit_code=1
    local vivado_check=1
    while (( vivado_attempts < 3 )); do
        safe_cd "${work_dir}/identity"

        local vivado_err_log="./vivado_errors_${vivado_attempts}.log"
        echo "check_syntax" > vivado_check.tcl
        vivado -mode batch -source vivado_check.tcl > ./vivado_output.log 2> "${vivado_err_log}"
        vivado_exit_code=$?

        if [[ $ivado_exit_code -eq 0 ]]; then
            rm -f "${vivado_err_log}"
            echo "  └─ Vivado:  $(print_check 0 $((vivado_attempts+1)))"
            break
        else
            cp rtl.v "./rtl_vivado_${vivado_attempts}.v"
            python "${SCRIPT_DIR}/error_feedback.py" "$work_dir" "vivado" ${vivado_attempts}
            echo "  ├─ Vivado Attempt $((vivado_attempts+1)) failed. Retrying..."
        fi

        ((vivado_attempts++))
    done

    if (( vivado_attempts >= 3 && vivado_exit_code != 0 )); then
        vivado_check=0
        echo "  ├─ Vivado:   $(print_check 1 3)"
        # exit 1  # Maybe Yosys check success
    fi

    #Yosys or Vivado check time
    if ((yosys_check ==1 && vivado_check == 1)); then
        echo "✅ Syntax check completed ($(($(date +%s) - check_start))s)"
    else
        echo "❌ Syntax check completed ($(($(date +%s) - check_start))s)"
    fi

    # ===================== Synthesis =====================
    folders=('vivado' 'yosys' 'simulation_identity' 'simulation_vivado' 
         'simulation_yosys' 'equiv_identity_vivado' 'equiv_identity_yosys')
    source_rtl="${work_dir}/identity/rtl.v"
    for folder in "${folders[@]}"; do
        target_dir="${work_dir}/${folder}"
        cp -v "$source_rtl" "$target_dir/" > /dev/null 2>&1;
    done
    cp "${work_dir}/identity/rtl.v" "${work_dir}/identity/syn_identity.v" > /dev/null 2>&1


    print_section "SYNTHESIS"
    local syn_start=$(date +%s)
    if ! python "${SCRIPT_DIR}/synthesis.py" "$work_dir"; then
        echo "❌ Synthesis failed"
        echo "❌ Synthesis completed ($(($(date +%s) - syn_start))s)"
        exit 1
    else
        echo "✅ Synthesis completed ($(($(date +%s) - syn_start))s)"
    fi
    

    # ===================== Simulation =====================
    print_section "SIMULATION"
    cp "${work_dir}/identity/syn_identity.v" "${work_dir}/simulation_identity/syn_identity.v" > /dev/null 2>&1
    cp "${work_dir}/yosys/syn_yosys.v" "${work_dir}/simulation_yosys/syn_yosys.v" > /dev/null 2>&1
    cp "${work_dir}/vivado/syn_vivado.v" "${work_dir}/simulation_vivado/syn_vivado.v" > /dev/null 2>&1
    local sim_start=$(date +%s)
    python "${SCRIPT_DIR}/testbench.py" "$work_dir" 

    run_simulation() {
        local target=$1
        safe_cd "${work_dir}/simulation_${target}"
        
        # Compile with Icarus Verilog
        if ! iverilog -o "${target}_main" "${target}_testbench.v" > "compile.log" 2>&1; then
            echo "❌ ${target} compilation failed"
            return 1
        fi
        
        # Run simulation with timeout
        timeout 1m vvp -n "${target}_main" > "vvp.log" 2>&1
        local vvp_exit=$?
        
        if [ $vvp_exit -eq 0 ]; then
            sed -i '/_testbench\.v/d' "vvp.log"
            sha256sum "vvp.log" | cut -c1-16
        elif [ $vvp_exit -eq 124 ]; then
            echo "❌ ${target} simulation timed out"
            return 1
        else
            echo "❌ ${target} simulation failed with exit code $vvp_exit"
            return 1
        fi
    }
    
        
    echo "✅ Simulation completed ($(($(date +%s) - sim_start))s)"
    echo "[📊] Simulation results:"
    local orig_hash=$(run_simulation identity)
    local yosys_hash=$(run_simulation yosys)
    local vivado_hash=$(run_simulation vivado)

    # Display comparison results
    echo "  ├─ Original:   $orig_hash $([[ "$orig_hash" == "$yosys_hash" ]] && echo "✔️" || echo "❌")"
    echo "  ├─ Yosys:      $yosys_hash $([[ "$yosys_hash" == "$orig_hash" ]] && echo "✔️" || echo "❌")"
    echo "  └─ Vivado:     $vivado_hash $([[ "$vivado_hash" == "$orig_hash" ]] && echo "✔️" || echo "❌")"

    # ===================== Finalization =====================
    print_section "SUMMARY"
    echo "✅ All checks completed successfully"
    echo "⏱️  Total execution time: $(($(date +%s) - start_time))s"

    python "${SCRIPT_DIR}/AST.py" "${work_dir}"

    cp "${work_dir}/identity/ast.txt" "${work_dir}/../../temp_save/tem_ast.txt"
    cp "${work_dir}/identity/rtl.v" "${work_dir}/../../temp_save/temp.v"
}

# Execute main function with arguments
main "$@"