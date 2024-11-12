from Tool.Yosys import *
from Tool.Vivado import *
import sys


def Yosys_synthesis(output_folder):
    print("### Starting Yosys Synthesis ###\n")

    print("Running synthesis with Yosys\n")

    yosys = Yosys()
    rtl_file = f"{output_folder}/yosys/rtl.v"
    output_directory = f"{output_folder}/yosys/"
    try:
        yosys.run_synth(rtl_file, output_directory)
    except Exception as e:
        print("### Yosys Synthesis Error ###\n", str(e))
        return None  # Return None if synthesis fails
    return "success"


def Vivado_synthesis(output_folder):
    print("### Starting Vivado Synthesis ###\n")

    print("Running synthesis with Vivado\n")

    vivado = Vivado()
    output_directory_vivado = f"{output_folder}/vivado"
    try:
        vivado.run_synth("top", f"{output_directory_vivado}/rtl.v", output_directory_vivado)
    except Exception as e:
        print("### Vivado Synthesis Error ###\n", str(e))
        return None  # Return None if synthesis fails
    return "success"


if __name__ == "__main__":
    print(" ### Starting Synthesis ###\n\n")
    if len(sys.argv) != 2:
        print("Usage: python synthesis.py output_folder")
        sys.exit(1)  # Exit with error code 1
    else:
        output_folder = sys.argv[1]

        result_yosys = Yosys_synthesis(output_folder)

        if result_yosys == "success":
            result_vivado = Vivado_synthesis(output_folder)
            if result_vivado == "success":
                print("\n### Finished Synthesis###\n")
            else:
                sys.exit(1)  # Exit with error code 1
        else:
            sys.exit(1)  # Exit with error code 1
