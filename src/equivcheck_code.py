from openai import OpenAI
import os
from openai_client import client

def read_file_content(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


def generate_equivalence_check_code(file1_path, file2_path):

    syn_identity_content = read_file_content(file1_path)
    syn_yosys_content = read_file_content(file2_path)

    prompt = "Please write a Verilog code for equivalence checking based on the two codes above. " \
             "The module name should be ‘equiv’. " \
             "All variables except rst clk should be assigned initial values such as reg, wire, etc. e.g.(wire output = 1'b0) assigned for initialization." \
             "It should meet the standards of formal verification engines such as ABC with Property Directed Reachability (PDR) when performing equivalence checks with tools like SymbiYosys (SBY). " \
             "It should meet that A signal (such as a network or register) can only be driven by one source " \
             "Do not contain the $error statement or else $display statement and should be formatted similarly to the following:" \
             """
                module equiv(
                    input wire clk,
                    input wire a,
                    input wire b
                );
                
                wire out1 = 1'b0, out2 = 1'b0; ////ATTENTION
                
                // Instantiate the two modules to be checked for equivalence
                top_1 t1(.a(a), .b(b), .c(out1));
                top_2 t2(.a(a), .b(b), .c(out2));
                
                // Always block for formal verification with clk as the triggering signal
                always @(posedge clk) begin
                    // Assertion for formal equivalence checks
                    assert(out1 == out2);
                end
                
                endmodule
            """

    prompt = f"// File 1 Content:\n{syn_identity_content}\n\n// File 2 Content:\n{syn_yosys_content}\n\n" + prompt


    messages = [
        {"role": "system",
         "content": "You are a Verilog programmer, adept at writing Verilog code and explaining complex programming concepts in innovative ways."},
        {"role": "user", "content": f"{prompt}"}
    ]


    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="gpt-4o-vision-preview",
        model="gpt-4o",
        messages=messages
    )


    completion_message = completion.choices[0].message


    equivalence_check_code_content = f"""
    {completion_message.content}
    """
    # print (equivalence_check_code_content)
    return equivalence_check_code_content


#
# prompt = "Please write a Verilog code for equivalence checking based on the two codes above. " \
#          "The module name should be ‘equiv’. " \
#          "It should meet the Verilog-2005 standard and use assertion-style equivalence checking code. " \
#          "It should not contain the $error statement and should be formatted similarly to the following:" \
#          """
#          module equiv(
#             input clk,
#             input [6:0] w0,
#             input [10:0] w1,
#             input signed [10:0] w2,
#             input [11:0] w3
#         );
#
#         wire [49:0] y1, y2;
#         top t1(y1, clk, w0, w1, w2, w3);
#         top_synth_netlist t2(y2, clk, w0, w1, w2, w3);
#
#         always @(posedge clk)
#             assert(y1 == y2);
#
#         endmodule
#         """

# file1_path = "../output/fuzz1/code/rtl.v"
# file2_path = "../output/fuzz1/code/syn_yosys.v"
#
# # prompt = f"// File 1 Content:\n{file1_content}\n\n// File 2 Content:\n{file2_content}\n\n" + prompt
# # print(prompt)


def extract_equivcheck_code(file1_path, file2_path):
    equivchech_code_content = generate_equivalence_check_code(file1_path, file2_path)

    start_keyword = '```verilog'
    end_keyword = 'endmodule'
    start_index = equivchech_code_content.find(start_keyword) + len(start_keyword)
    end_index = equivchech_code_content.find(end_keyword) + len(end_keyword)
 
    equivchech_code = equivchech_code_content[start_index:end_index]

    equivchech_code = equivchech_code.lstrip()

    # print(equivchech_code)
    return equivchech_code


#
# file1_path = "../output/fuzz1/code/rtl.v"
# file2_path = "../output/fuzz1/code/syn_yosys.v"


def yosys_equiv( output_dir):
    equivalence_check_yosys_code = extract_equivcheck_code(f"{output_dir}/equiv_identity_yosys/syn_identity.v",
                                                           f"{output_dir}/equiv_identity_yosys/syn_yosys.v")


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    with open(os.path.join(f"{output_dir}/equiv_identity_yosys", "equiv.v"), "w") as equiv_file:
        equiv_file.write(equivalence_check_yosys_code)




def vivado_equiv(output_dir):
    equivalence_check_vivado_code = extract_equivcheck_code(
                                                            f"{output_dir}/equiv_identity_vivado/syn_identity.v",
                                                            f"{output_dir}/equiv_identity_vivado/syn_vivado.v")


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    with open(os.path.join(f"{output_dir}/equiv_identity_vivado", "equiv.v"), "w") as equiv_file:
        equiv_file.write(equivalence_check_vivado_code)
