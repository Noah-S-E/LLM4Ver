from openai import OpenAI
from openai_client import client
import sys

def read_file_content(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


def generate_equivalence_check_code(file_path):

    syn_content = read_file_content(file_path)

    prompt = "Please write a verilog testbench code based on the above code"

    prompt = f"// File 1 Content:\n{syn_content}\n\n" + prompt


    messages = [
        {"role": "user", "content": f"{prompt}"}
    ]


    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="gpt-4o-vision-preview",
        model="gpt-4o",
        messages=messages
    )


    completion_message = completion.choices[0].message


    testbench_code_content = f"""
    {completion_message.content}
    """
    print(testbench_code_content)
    print("\n\n")
    return testbench_code_content

def extract_testbench_code(output_folder):
    file_path = f"{output_folder}/identity/rtl.v"
    testbench_code_content = generate_equivalence_check_code(file_path)

    # start_keyword = '`timescale'
    start_keyword = '```verilog'
    end_keyword = 'endmodule'
    # start_index = testbench_code_content.find(start_keyword)
    start_index = testbench_code_content.find(start_keyword) + len(start_keyword)
    end_index = testbench_code_content.find(end_keyword) + len(end_keyword)

    testbench_code = testbench_code_content[start_index:end_index]

    testbench_code = testbench_code.lstrip()

    # testbench_code = '`include "syn_{}.v"\n'.format(syn_str) + testbench_code
    print(testbench_code)

    return testbench_code

#
# file_path = "../output/fuzz1/code/top.v"


def simulation(output_folder):


    testbench_code = extract_testbench_code(output_folder)



    file_path_identity = f"{output_folder}/simulation_identity/identity_testbench.v"
    with open (file_path_identity, 'w') as f:
        f.write("`include \"syn_identity.v\"\n") 
        f.write(testbench_code)



    file_path_yosys = f"{output_folder}/simulation_yosys/yosys_testbench.v"
    with open (file_path_yosys, 'w') as f:
        f.write("`include \"syn_yosys.v\"\n")  
        f.write(testbench_code)



    file_path_vivado = f"{output_folder}/simulation_vivado/vivado_testbench.v"
    with open (file_path_vivado, 'w') as f:
        f.write("`include \"syn_vivado.v\"\n`include \"../../../../data/cells_xilinx_7.v\"\n")  
        f.write(testbench_code)





if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testbench.py output_folder")
    else:
        output_folder = sys.argv[1]
    simulation(output_folder = output_folder)
