import os
import sys
from openai_client import client


def feedback(output_folder, str, number):

    if str == 'yosys':
        file_path = os.path.join(output_folder, 'identity', f'yosys_errors_{number}.log')
    elif str == 'vivado':
        file_path = os.path.join(output_folder, 'identity', f'vivado_errors{number}.log')


    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在.")
        return


    with open(file_path, 'r') as file:
        error_content = file.read()

    # print(error_content)
    # print(" ")

    file_verilog = os.path.join(output_folder, 'identity', 'rtl.v')
    with open(file_verilog, 'r') as file:
        verilog_code = file.read()

    error_feedback_prompt = "The above is the Verilog code and its error report. " \
             "Please modify the code according to the error report."

    prompt = f"{verilog_code}\n\n" + f"{error_content}\n\n" +  error_feedback_prompt


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


    modified_code_content = f"""
    {completion_message.content}
    """
    # print(testbench_code_content)
    return modified_code_content


def extract_modified_code(file_path, syn_str, num):
    modified_code_content = feedback(file_path, syn_str, num)

    start_keyword = '```verilog'
    end_keyword = 'endmodule'
    start_index = modified_code_content.find(start_keyword) + len(start_keyword)
    end_index = modified_code_content.find(end_keyword) + len(end_keyword)

    modified_code = modified_code_content[start_index:end_index]

    modified_code = modified_code.lstrip()


    return modified_code

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python error_feednack.py output_folder syn_str num")
    else:
        output_folder = sys.argv[1]
        syn_str = sys.argv[2]
        num = sys.argv[3]
        modified_code = extract_modified_code(f"{output_folder}", f"{syn_str}", num)
        print("modified_code: \n\n")
        print(modified_code)
        print(" ")

        file_path = os.path.join(output_folder, 'identity', 'rtl.v')
        with open(file_path, 'w') as f:
            f.write(modified_code)

