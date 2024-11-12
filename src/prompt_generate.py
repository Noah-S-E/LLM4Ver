import random
from openai_client import client

def select_operation(probabilities):
    """
    probabilities: A dictionary containing the probabilities for each operation.
                   Example: {"module_declaration": 0.7, "enrich_module_behavior": 0.3}
    """

    operations = list(probabilities.keys())
    probs = list(probabilities.values())


    selected_operation = random.choices(operations, weights=probs, k=1)[0]

    return selected_operation

# probabilities = {"module_declaration": 0.7, "enrich_module_behavior": 0.3}
# selected_op = select_operation(probabilities)
# print(selected_op)





def generate_rule():
    rule_map = {
      "rule_1": {"description": "Add declarations for wires and registers.", "probability": 0.1},
      "rule_2": {"description": "Add arithmetic and other operations.", "probability": 0.2},
      "rule_3": {"description": "Add bitwise operations.", "probability": 0.15},
      "rule_4": {"description": "Add shift operations.", "probability": 0.1},
      "rule_5": {"description": "Add arrays.", "probability": 0.05},
      "rule_6": {"description": "Add conditional statements (if-else).", "probability": 0.1},
      "rule_7": {"description": "Add loop statements.", "probability": 0.1},
      "rule_8": {"description": "Add case statements.", "probability": 0},
      "rule_9": {"description": "Add begin-end blocks.", "probability": 0.05},
      "rule_10": {"description": "Add parameter declarations.", "probability": 0.05},
      "rule_11": {"description": "Add generate blocks.", "probability": 0.05}
    }

    total_probability = sum(data["probability"] for data in rule_map.values())


    for data in rule_map.values():
        data["probability"] /= total_probability


    selected_rules = []
    num_rules = random.randint(1, len(rule_map)) 
    while len(selected_rules) < num_rules:
        random_value = random.random()
        cumulative_probability = 0
        for op, data in rule_map.items():
            cumulative_probability += data["probability"]
            if random_value <= cumulative_probability:
                selected_rules.append(data["description"])
                break

    return selected_rules



def extend_code_rule(operation):
    if operation == "module_declaration":

        prompt_operation = "Generate submodule for the module and instantiate it"

    elif operation == "enrich_module_behavior":

        prompt_operation = "Add additional behavior to the current module"

    else:
        raise ValueError("Invalid operation")
    rule_description = generate_rule()
    rule_description = "  ".join(rule_description)
    # print(f"Generate Rule: {rule_description}")
    return prompt_operation + "  Reference practices:    " + rule_description






# probabilities = {"module_declaration": 0.7, "enrich_module_behavior": 0.3}
# selected_operation = select_operation(probabilities)
# print(selected_operation)
# # generated_rule = generate_rule()
# extend_code_description=extend_code_rule(selected_operation)
# print("Selected Operation:", selected_operation)
# print("extend_code_description:", extend_code_description)

def generate_supplementary_code_prompt():

    prompt = "Please generate a supplementary code of the input <Verilog Basic Code> by <expanded code rule> and utilizing the <Verilog Basic Syntax Tree>, " \
             "under the probability constraints in <Config files>." \
             "Additionally, ensure that the top-level module is named \"top\"and that the Verilog code generated complies with the Verilog-2005 version."

    return prompt


# prompt = generate_supplementary_code_prompt()
# print(prompt)



def bug_prompt_preinput():

    bug_prompt_preinput = ""

    messages = [
        {"role": "user", "content": f"The following are common verilog error messages, please remember not to make them again: \n {bug_prompt_preinput}"}
    ]


    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="gpt-4o-vision-preview",
        model="gpt-4o",
        messages=messages
    )


    # completion_message = completion.choices[0].message


    # return_content = f"""
    #     {completion_message.content}
