from openai import OpenAI
import re
from openai_client import client

def generate_verilog_syntax_tree( verilog_syntax_tree=None):
    if verilog_syntax_tree is None:

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


    messages = [
        {"role": "user",
         "content": f"Please write a Verilog code and name the top-level module as 'top',"
                    f"The Verilog code should meet that A signal (such as a network or register) can only be driven by one source.  "
                    f"then generate the corresponding syntax tree. The format of the syntax tree should follow:\n{verilog_syntax_tree}."}
    ]

    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="gpt-4o-vision-preview",
        model="gpt-4o",
        messages=messages
    )


    completion_message = completion.choices[0].message


    code_syntax_tree = f"""
    {completion_message.content}
    """
    print(code_syntax_tree)
    print("==============")
    return code_syntax_tree


def extract_verilog_base_code_and_syntax_tree(input_text):
    code_lines = []
    syntax_tree_lines = []


    in_code_block = False
    in_syntax_tree_block = False

    for line in input_text.split('\n'):

        if line.strip() == '```verilog':
            in_code_block = True
            continue
        elif line.strip() == '```':
            in_code_block = False
            continue


        if line.strip() == '```verilog_syntax_tree' or line.strip() == 'verilog_syntax_tree':
            in_syntax_tree_block = True
            continue
        elif line.strip() == '```':
            in_syntax_tree_block = False
            continue


        if in_code_block:
            code_lines.append(line)
        elif in_syntax_tree_block:
            syntax_tree_lines.append(line)


    return '\n'.join(code_lines), '\n'.join(syntax_tree_lines)


def generate_supplemental_code(prompt):


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


    supplemental_code = f"""
    {completion_message.content}
    """
    # print(code_syntax_tree)
    return supplemental_code


def extract_supplemental_code(prompt):
    supplemental_code_content = generate_supplemental_code(prompt)

    start_keyword = '```verilog'
    end_keyword = 'endmodule'
    start_index = supplemental_code_content.find(start_keyword) + len(start_keyword)
    end_index = supplemental_code_content.rfind(end_keyword) + len(end_keyword)

    supplemental_code = supplemental_code_content[start_index:end_index]

    supplemental_code = supplemental_code.lstrip()

    # print(supplemental_code)
    return supplemental_code
