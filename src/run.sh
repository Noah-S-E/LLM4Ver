# #!/bin/bash


# if [ "$#" -ne 2 ]; then
#     echo "Usage: $0 <output_directory> <total_iterations>"
#     exit 1
# fi


# output_directory=$1
# total_iterations=$2


# mkdir -p temp_save
# touch temp_save/tem_ast.txt temp_save/temp.v


# for (( i=1; i<=total_iterations; i++ ))
# do

#     mkdir -p "${output_directory}/${i}"


#     bash run_main.sh "${output_directory}" "$i" > "${output_directory}/${i}/log.txt" 2>&1


#     if (( i % 3 == 0 )); then
#         echo "" > temp_save/tem_ast.txt
#         echo "" > temp_save/temp.v
#     fi
# done

# echo "All iterations completed."
#!/bin/bash
#!/bin/bash
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

# Generate HTML report
html_file="${output_directory}/report.html"
echo "<html><head><title>Synthesis Report</title>" > $html_file
echo "<style>
    body { font-family: 'Times New Roman', serif; }
    table { width: 100%; border-collapse: collapse; font-size: 1.2em; }
    th, td { padding: 10px; text-align: center; border: 1px solid #ddd; }
    th { background-color: #f2f2f2; }
    .success { background-color: #d4edda; }
    .error { background-color: #f8d7da; }
    .simulation { white-space: pre; font-family: monospace; font-weight: bold; text-align: center; }
</style>" >> $html_file
echo "</head><body>" >> $html_file
echo "<h1 style='text-align: center;'>Synthesis Report</h1>" >> $html_file
echo "<table>" >> $html_file
echo "<tr><th>Directory</th><th>Yosys Synthesis</th><th>Vivado Synthesis</th><th>Simulation</th><th>Consistency</th></tr>" >> $html_file

for dir in "${output_directory}"/*/; do
    log_file="${dir}log.txt"
    if [ -f "$log_file" ]; then
        # Check Yosys Synthesis status
        if grep -Fq  "✅ YOSYS SYNTHESIS COMPLETE [SUCCESS]" "$log_file"; then
            yosys_status="S"
            yosys_class="success"
        else
            yosys_status="E"
            yosys_class="error"
        fi

        # Check Vivado Synthesis status
        if grep -Fq  "✅ VIVADO SYNTHESIS COMPLETE [SUCCESS]" "$log_file"; then
            vivado_status="S"
            vivado_class="success"
        else
            vivado_status="E"
            vivado_class="error"
        fi

        # Enhanced hash extraction method: Find the first match from the end of file
        extract_last_hash() {
            local pattern="$1"
            # Reverse file content using tac, then find first matching line with awk
            local hash=$(tac "$log_file" | awk -v pat="$pattern" '
                $0 ~ pat {  # Pattern matching condition
                    print $3;  # Extract 3rd field (hash value)
                    exit       # Exit immediately after first match
                }'
            )
            
            # Error handling for empty hash
            if [ -z "$hash" ]; then
                echo "❌ Hash extraction failed for pattern: $pattern" >&2  # Error to stderr
                return 1  # Return non-zero status
            fi
            echo "$hash"  # Output successful result
        }

        # Extract hash values for each implementation
        identity=$(extract_last_hash "├─ Original:")    # Original implementation hash
        yosys_hash=$(extract_last_hash "├─ Yosys:")     # Yosys synthesis hash
        vivado_hash=$(extract_last_hash "└─ Vivado:")   # Vivado synthesis hash

        # Validate extraction results
        # echo "Original: $identity"     # Display original hash
        # echo "Yosys:    $yosys_hash"   # Display Yosys hash
        # echo "Vivado:   $vivado_hash"  # Display Vivado hash

        # Handle empty values
        if [ -z "$yosys_hash" ]; then
            yosys_hash=""
        fi
        if [ -z "$vivado_hash" ]; then
            vivado_hash=""
        fi

        # Format simulation column with aligned hash values
        simulation_content="identity: <b>$identity</b>
yosys:    <b>$yosys_hash</b>
vivado:   <b>$vivado_hash</b>"

        # Check consistency
        if [ "$identity" == "$yosys_hash" ] && [ "$identity" == "$vivado_hash" ]; then
            consistency="C"
            consistency_class="success"
        else
            consistency="I"
            consistency_class="error"
        fi

        # Add row to HTML table
        echo "<tr>" >> $html_file
        echo "<td>${dir}</td>" >> $html_file
        echo "<td class='$yosys_class'>$yosys_status</td>" >> $html_file
        echo "<td class='$vivado_class'>$vivado_status</td>" >> $html_file
        echo "<td class='simulation'>$simulation_content</td>" >> $html_file
        echo "<td class='$consistency_class'>$consistency</td>" >> $html_file
        echo "</tr>" >> $html_file
    fi
done

echo "</table></body></html>" >> $html_file

echo "HTML report generated at ${html_file}"