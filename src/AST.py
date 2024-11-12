from openai import OpenAI
import re
import os
import sys
from openai_client import client


def generate_corre_AST(output_folder):
    verilog_syntax_tree = """
           verilog_syntax_tree
                   Module
                   |
                   |-- Identifier: 
                   |
                   |-- Port List
                   |   |
                   |   |-- Input: 
                   |   |-- Input: 
                   |   |-- Output:
                   |
                   |-- Always Block
                       |
                       |-- Sensitivity List
                       |   |
                       |   |-- Posedge: 
                       |   |-- Posedge: 
                       |
                       |-- If Statement
                           |
                           |-- Condition: 
                           |
                           |-- True Statement:
                           |
                           |-- False Statement:
                   ...
           end
                   """
    file_path = os.path.join(output_folder, 'identity', 'rtl.v')

    with open(file_path, 'r') as f:
        code_cotent = f.read()


    messages = [
        {"role": "user",
         "content": f"The format of the Verilog syntax tree is as follows:\n {verilog_syntax_tree} ,"
                    f"Please generate the corresponding syntax tree for this verilog code:\n {code_cotent} \n based on the format of the syntax tree.  "}
    ]


    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="gpt-4o-vision-preview",
        model="gpt-4o",
        messages=messages
    )


    completion_message = completion.choices[0].message


    syntax_tree = f"""
    {completion_message.content}
    """
    print(syntax_tree)




def tree_extract(output_folder):
    # input_text = generate_corre_AST(output_folder)
    input_text = """
           verilog_syntax_tree
                   Module
                   |
                   |-- Identifier: 
                   |
                   |-- Port List
                   |   |
                   |   |-- Input: 
                   |   |-- Input: 
                   |   |-- Output:
                   |
                   |-- Always Block
                       |
                       |-- Sensitivity List
                       |   |
                       |   |-- Posedge: 
                       |   |-- Posedge: 
                       |
                       |-- If Statement
                           |
                           |-- Condition: 
                           |
                           |-- True Statement:
                           |
                           |-- False Statement:
                   ...
           end
                   """
    syntax_tree_lines = []



    in_syntax_tree_block = False

    for line in input_text.split('\n'):


        if line.strip() == '```verilog_syntax_tree' or line.strip() == 'verilog_syntax_tree':
            in_syntax_tree_block = True
            continue
        elif line.strip() == '```':
            in_syntax_tree_block = False
            continue



        elif in_syntax_tree_block:
            syntax_tree_lines.append(line)


    return '\n'.join(syntax_tree_lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python AST.py output_folder")
    else:
        output_folder = sys.argv[1]
    tree = tree_extract(output_folder = output_folder)

    file_path_tree = os.path.join(output_folder, 'identity', 'ast.txt')
    with open(file_path_tree, 'w') as f:
        f.write('    verilog_syntax_tree:\n')  
        f.write(tree + '\n')  
        f.write('end')  





