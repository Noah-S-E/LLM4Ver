from code_generate import *
from code_inspect import *
from dotenv import load_dotenv
from config_extract import read_config
from prompt_generate import *
from openai_client import client
from config_extract import *
import sys

def generate(file_path1, file_path2, output_folder):
    print("### Verilog Generate ###\n\n")


    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
        content1 = file1.read()
        content2 = file2.read()

    if not content1.strip() or not content2.strip():
        config_file_path = "../config/config.toml"
        config_preinput(config_file_path)

        code_syntax_tree = generate_verilog_syntax_tree()
        # print(code_syntax_tree)
        verilog_code, syntax_tree = extract_verilog_base_code_and_syntax_tree(code_syntax_tree)
        # print(verilog_code)
        print("\n")
        # print(syntax_tree)
        print("\n")


        # with open(file_path1, 'w') as f:
        #     f.write(verilog_code)
        # with open(file_path2, 'w') as f:
        #     f.write(syntax_tree)

        # file_path_base = os.path.join(output_folder, 'identity', 'original.txt')
        # with open(file_path_base, 'w') as f:
        #     f.write(code_syntax_tree)

        file_path = os.path.join(output_folder, 'identity', 'rtl.v')
        with open(file_path, 'w') as f:
            f.write(verilog_code)

        # folders = ['identity', 'vivado', 'yosys', 'simulation_identity', 'simulation_vivado', 'simulation_yosys',
        #            'equiv_identity_vivado', 'equiv_identity_yosys']
        #
        # for folder in folders:
        #     file_path = os.path.join(output_folder, folder, 'rtl.v')
        #     with open(file_path, 'w') as f:
        #         f.write(verilog_code)
        #
        #     if folder == 'identity':
        #         syn_identity_path = os.path.join(output_folder, folder, 'syn_identity.v')
        #         with open(syn_identity_path, 'w') as syn_f:
        #             syn_f.write(verilog_code)
    else:
        verilog_base_code = content1
        syntax_base_tree = content2

        probabilities = {"module_declaration": 0.3, "enrich_module_behavior": 0.7}
        selected_operation = select_operation(probabilities)
        extend_code_description = extend_code_rule(selected_operation)


        parttern = generate_supplementary_code_prompt()

        # prompt_final = f"<Verilog Basic Code> :\n{verilog_base_code}\n\n" \
        #                f"<expanded code description> :\n{extend_code_description}\n\n" \
        #                f"<Verilog Basic Syntax Tree> :\n{syntax_base_tree}\n\n" \
        #                f"<Config files> :\n{config}\n\n" \
        #                f"Pattern : {parttern}\n" \
        #                f"Try to exclude areas where code has not been executed as much as possible\n\n" \
        #                f"Notice: A always block is only sensitive to the rising or falling edge of one signal!(do not exit \"always @ (posedge a or posedge b))\" " \
        #                f"Notice:!! Variables and signal clk rst etc must be declared." \
        #                f"Do not have an int type." \
        #                f"If you want to declare an output port that is of type Reg, you should directly use \"output reg Y\" in the port declaration. " \
        #                f"Instead of declaring Y as output on the port of the module, and then declaring Y as a reg type again inside the module.\n\n"
        # print(prompt_final)

        prompt_final = f"<Verilog Basic Code> :\n{verilog_base_code}\n\n" \
                       f"<expanded code description> :\n{extend_code_description}\n\n" \
                       f"<Verilog Basic Syntax Tree> :\n{syntax_base_tree}\n\n" \
                       f"Pattern : {parttern}\n\n" \
                       f"Meets Verilog 2005 syntax" \
                       f"ATTention: Please use Markdown format and ensure that the generated Verilog code is placed within the ```verilog  ```, and the generated syntax tree within the ```verilog_syntax_tree  ```."

        supplemental_code = extract_supplemental_code(prompt_final)
        print(supplemental_code)

        file_path = os.path.join(output_folder, 'identity', 'rtl.v')
        with open(file_path, 'w') as f:
            f.write(supplemental_code)

        # folders = ['identity', 'vivado', 'yosys', 'simulation_identity', 'simulation_vivado', 'simulation_yosys',
        #            'equiv_identity_vivado', 'equiv_identity_yosys']
        # for folder in folders:
        #     file_path = os.path.join(output_folder, folder, 'rtl.v')
        #     with open(file_path, 'w') as f:
        #         f.write(supplemental_code)
        #
        #     if folder == 'identity':
        #         syn_identity_path = os.path.join(output_folder, folder, 'syn_identity.v')
        #         with open(syn_identity_path, 'w') as syn_f:
        #             syn_f.write(supplemental_code)

    print("### Verilog Generate Success ###\n\n")




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate.py output_folder")
    else:
        file_path1 = "./temp_save/temp.v"
        file_path2 = "./temp_save/tem_ast.txt"
        output_folder = sys.argv[1]
        generate(file_path1, file_path2, output_folder)
