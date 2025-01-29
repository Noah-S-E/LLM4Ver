import os
import subprocess

class VivadoSynthesisError(Exception):
    """Vivado synthesis process failed"""
    pass

class Vivado:
    def __init__(self, vivado_bin=None, vivado_desc="vivado", vivado_output="syn_vivado.v"):
        self.vivado_bin = vivado_bin
        self.vivado_desc = vivado_desc
        self.vivado_output = vivado_output

    def __str__(self):
        return self.vivado_desc

    # def run_synth(self, top, v_file, output_dir): 
    #     vivado_tcl = os.path.join(output_dir, f"vivado_{top}.tcl")  
    #
    #
    #     with open(vivado_tcl, 'w') as f:
    #         f.write(self.vivado_synthesis_config(top)) 
    #
    #     subprocess.run(["sed", "s/^module/(* use_dsp48=\"no\" *) (* use_dsp=\"no\" *) module/;", "-i", v_file])
    #     vivado_bin = self.vivado_bin if self.vivado_bin else "vivado"
    #
    #     
    #     os.chdir(output_dir)
    #     vivado_tcl = f"vivado_{top}.tcl"
    #
    #
    #     result = subprocess.run([vivado_bin, "-mode", "batch", "-source", vivado_tcl], capture_output=True, text=True)
    #     if result.returncode != 0:
    #         print("Synthesis failed:", result.stderr)
    #     else:
    #         print("Synthesis succeeded")
    def run_synth(self, top, v_file, output_dir):
        try:
            if not os.path.exists(v_file):
                raise FileNotFoundError(f"Verilog file {v_file} not found")

            os.makedirs(output_dir, exist_ok=True)

            vivado_tcl = os.path.join(output_dir, f"vivado_{top}.tcl")
            with open(vivado_tcl, 'w') as f:
                f.write(self.vivado_synthesis_config(top))

            sed_cmd = ["sed", "-i", "s/^module/(* use_dsp48=\"no\" *) (* use_dsp=\"no\" *) module/;", v_file]
            subprocess.run(sed_cmd, check=True)  

            os.chdir(output_dir)

            vivado_bin = self.vivado_bin if self.vivado_bin else "vivado"
            cmd = [vivado_bin, "-mode", "batch", "-source", vivado_tcl]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True  
            )

            log_file = os.path.join(output_dir, "vivado_synth.log")
            with open(log_file, "w") as f:
                f.write(result.stdout)

            return 0

        except subprocess.CalledProcessError as e:
            error_msg = f"Vivado Error (code {e.returncode}):\n{e.stderr}"
            raise VivadoSynthesisError(error_msg) from e


    def vivado_synthesis_config(self, top):
        config_lines = [
            "# CRITICAL WARNING: [Synth 8-5821] Potential divide by zero",
            "set_msg_config -id {Synth 8-5821} -new_severity {WARNING}",
            "",
            f"read_verilog rtl.v",
            f"synth_design -part xc7k70t -top {top}",
            f"write_verilog -force syn_vivado.v"
        ]
        return "\n".join(config_lines)

