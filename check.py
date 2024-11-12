import os


def count_logs(directory):
    yosys_check_error_count = 0
    yosys_synthesis_success_count = 0
    vivado_synthesis_success_count = 0
    yosys_simulation_success_count = 0
    vivado_simulation_success_count = 0
    total_files = 0

    for subdir, _, files in os.walk(directory):
        for file in files:
            if file == 'log.txt':
                total_files += 1
                with open(os.path.join(subdir, file), 'r') as f:
                    log_content = f.readlines()
                    first_yosys_check = None

                    for line in log_content:
                        if 'Yosys Check' in line:
                            first_yosys_check = line
                            break

                    if first_yosys_check and 'Error' in first_yosys_check:
                        yosys_check_error_count += 1

                    if any('### Yosys Synthesis Success ###' in line for line in log_content):
                        yosys_synthesis_success_count += 1
                    if any('### Vivado Synthesis Success ###' in line for line in log_content):
                        vivado_synthesis_success_count += 1
                    if any('Yosys simulation iverilog Compilation Success' in line for line in log_content):
                        yosys_simulation_success_count += 1
                    if any('Vivado simulation iverilog Compilation Success' in line for line in log_content):
                        vivado_simulation_success_count += 1

    def calculate_percentage(part, whole):
        return 100 * float(part) / float(whole) if whole != 0 else 0

    print(f"Total log files: {total_files}")
    print(
        f"Yosys Check Error logs: {yosys_check_error_count} ({calculate_percentage(yosys_check_error_count, total_files):.2f}%)")
    print(
        f"Yosys Synthesis Success logs: {yosys_synthesis_success_count} ({calculate_percentage(yosys_synthesis_success_count, total_files):.2f}%)")
    print(
        f"Vivado Synthesis Success logs: {vivado_synthesis_success_count} ({calculate_percentage(vivado_synthesis_success_count, total_files):.2f}%)")
    print(
        f"Yosys simulation iverilog Compilation Success logs: {yosys_simulation_success_count} ({calculate_percentage(yosys_simulation_success_count, total_files):.2f}%)")
    print(
        f"Vivado simulation iverilog Compilation Success logs: {vivado_simulation_success_count} ({calculate_percentage(vivado_simulation_success_count, total_files):.2f}%)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
    else:
        directory = sys.argv[1]
        count_logs(directory)
