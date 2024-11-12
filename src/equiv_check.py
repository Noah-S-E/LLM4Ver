from equivcheck_code import *
import sys
import subprocess

def equivcheck(output_folder):

    print("\n### Starting Equivalence Check ###\n")


    print("Running equivalence check for identity and yosys")
    yosys_equiv(output_dir= output_folder)


    bash_script = "./run_symbiyosys.sh"


    arguments_yosys = [f"{output_folder}/equiv_identity_yosys/", "syn_identity.v", "syn_yosys.v", "equiv.v"]


    arguments_str = ' '.join(arguments_yosys)


    subprocess.run(f"{bash_script} {arguments_str}", shell=True)

    print("Finished equivalence check for identity and yosys\n")



    print("Running equivalence check for identity and vivado")

    vivado_equiv(output_dir= output_folder)

 
    bash_script = "./run_symbiyosys.sh"


    arguments_yosys = [f"{output_folder}/equiv_identity_vivado/", "syn_identity.v", "syn_vivado.v", "equiv.v"]


    arguments_str = ' '.join(arguments_yosys)


    subprocess.run(f"{bash_script} {arguments_str}", shell=True)

    print("Finished equivalence check for identity and vivado\n\n")
    print("### Finished Equivalence Check###\n")





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python equiv_check.py output_folder")
    else:
        output_folder = sys.argv[1]
    equivcheck(output_folder = output_folder)


