import os
import glob
import re
import argparse
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# Function to remove comments from Verilog code
def remove_comments(verilog_code):
    # Remove block comments (/* ... */)
    verilog_code = re.sub(r'/\*.*?\*/', '', verilog_code, flags=re.DOTALL)
    # Remove single-line comments (// ...)
    verilog_code = re.sub(r'//.*', '', verilog_code)
    # Replace keywords and identifiers with placeholders
    verilog_code = re.sub(r'\b(module|input|output|reg|wire|always|begin|end)\b', 'KEYWORD', verilog_code)
    verilog_code = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'IDENTIFIER', verilog_code)  # Replace identifiers
    # Replace numbers with 'NUMBER'
    verilog_code = re.sub(r'\b\d+(\.\d+)?\b', 'NUMBER', verilog_code)
    # Remove excessive whitespace
    verilog_code = re.sub(r'\s+', ' ', verilog_code)
    # Convert to lowercase
    verilog_code = verilog_code.lower()
    return verilog_code.strip()



# Define a function to read all rtl.v files from subdirectories
def read_verilog_files(directory):
    # Use glob to find all rtl.v files in subdirectories
    file_paths = glob.glob(os.path.join(directory, '**', 'identity', 'rtl.v'), recursive=True)
    verilog_codes = []

    # Iterate through all file paths and read each file's content
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            cleaned_content = remove_comments(content)  # Remove comments from the code
            if cleaned_content.strip():  # Ensure the file is not empty after removing comments
                verilog_codes.append(cleaned_content)
    
    return verilog_codes

# Prepare the Verilog code for Doc2Vec model
def prepare_documents(verilog_codes):
    # Tagging each document for training Doc2Vec model
    tagged_data = [TaggedDocument(words=code.split(), tags=[str(i)]) for i, code in enumerate(verilog_codes)]
    return tagged_data

# Train the Doc2Vec model
def train_doc2vec_model(tagged_data):
    model = Doc2Vec(vector_size=100, window=2, min_count=1, workers=4, epochs=1000)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    return model

# Set up command-line argument parser
def parse_args():
    parser = argparse.ArgumentParser(description="Calculate Doc2Vec similarity of Verilog code")
    parser.add_argument('directory', type=str, help="Root directory containing subdirectories with identity/rtl.v files")
    return parser.parse_args()

# Main program
def main():
    # Parse command-line arguments
    args = parse_args()

    # Read all rtl.v files from the specified directory and its subdirectories
    verilog_codes = read_verilog_files(args.directory)

    if not verilog_codes:
        print("No valid rtl.v files found.")
        return

    # Prepare the Verilog code documents for Doc2Vec model
    tagged_data = prepare_documents(verilog_codes)

    # Train Doc2Vec model
    model = train_doc2vec_model(tagged_data)

    # Calculate similarity between documents using Doc2Vec's similarity function
    similarities = []
    for i in range(len(verilog_codes)):
        for j in range(i + 1, len(verilog_codes)):
            # Calculate similarity directly using Doc2Vec's `similarity` method
            sim = model.dv.similarity(i, j)  # Get the similarity between documents i and j
            similarities.append(sim)

    # Calculate the average similarity
    average_similarity = sum(similarities) / len(similarities)
    print(f"Doc2Vec average similarity: {average_similarity}")

# Run the main program
if __name__ == "__main__":
    main()

