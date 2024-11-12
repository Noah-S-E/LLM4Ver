import toml
from openai_client import client


def read_config(file_path):
    try:
        with open(file_path, "r") as file:
            config = toml.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: Config file '{file_path}' not found.")
        return None


def config_preinput(file_path):
    config = read_config(file_path)

    if config is not None:

        config_str = toml.dumps(config)


        pre_prompt = f"The following is <Config files> which is the construction prompt prefix for the Verilog code, please remember\n{config_str}"

        messages = [
            {"role": "system",
             "content": "You are a Verilog programmer, adept at writing Verilog code and explaining complex programming concepts in innovative ways."},
            {"role": "user", "content": f"{pre_prompt}"}
        ]


        completion = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            # model="gpt-4o-vision-preview",
            model="gpt-4o",
            messages=messages,
            stream = True 
        )


