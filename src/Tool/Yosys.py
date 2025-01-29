import subprocess
import os

class SynthesisError(Exception):
    """Yosys synthesis process failed"""
    pass

class Yosys:
    def __init__(self, yosys_bin=None, yosys_desc="yosys", yosys_output="syn_yosys.v"):
        self.yosys_bin = yosys_bin if yosys_bin else "yosys"
        self.yosys_desc = yosys_desc
        self.yosys_output = yosys_output

    # def run_synth(self, src_file, output_dir, log_file="yosys.log"):
    #     # Check if src_file exists
    #     if not os.path.exists(src_file):
    #         print(f"Error: File {src_file} not found.")
    #         return
    #
    #     # Create output directory if it doesn't exist
    #     os.makedirs(output_dir, exist_ok=True)
    #
    #     # Construct output file path
    #     output_file = os.path.join(output_dir, self.yosys_output)
    #     log_file = os.path.join(output_dir, log_file)  # Modify log file path
    #
    #     # Construct command
    #     cmd = [self.yosys_bin, "-p", f"read_verilog {src_file}; synth; write_verilog -noattr {output_file}"]
    #
    #     # Run synthesis
    #     result = subprocess.run(cmd, capture_output=True, text=True)
    #
    #     # Write synthesis log to file
    #     with open(log_file, "w") as f:
    #         f.write(result.stdout)
    #         if result.returncode != 0:
    #             f.write("Synthesis Error:" + result.stderr)
    #         else:
    #             f.write("Synthesis Success")
    #
    #     # Print synthesis result
    #     if result.returncode != 0:
    #         print("### Yosys Synthesis Error ###\n\n", result.stderr)
    #     else:
    #         print("### Yosys Synthesis Success ###\n\n")
    #         print("### Finished synthesis with yosys ###\n")
    #         # print("### Yosys Synthesis Success. Verilog saved to", output_file)
    #         # print("Synthesis Log saved to", log_file)  # Print log file path
    def run_synth(self, src_file, output_dir, log_file="yosys.log"):
        try:
            # Check if src_file exists
            if not os.path.exists(src_file):
                raise FileNotFoundError(f"Source RTL file {src_file} not found")

            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Construct output file path
            output_file = os.path.join(output_dir, self.yosys_output)
            log_file = os.path.join(output_dir, log_file)  # Modify log file path

            # Construct command
            cmd = [self.yosys_bin, "-p", f"read_verilog {src_file}; synth; write_verilog -noattr {output_file}"]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True  
            )

            try:
                with open(log_file, "w") as f:
                    f.write(result.stdout)
                    f.write("\nSynthesis Success")
            except IOError as e:
                raise IOError(f"Failed to write log file: {str(e)}") from e
            return 0

        except subprocess.CalledProcessError as e:

            raise SynthesisError(f"Yosys Error:\n{e.stderr}") from e