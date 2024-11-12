import subprocess
import hashlib

class Icarus:
    def __init__(self, icarus_path="iverilog", vvp_path="vvp"):
        self.icarus_path = icarus_path
        self.vvp_path = vvp_path

    def compile(self, file):
        result = subprocess.run([self.icarus_path, "-o", "main", file], capture_output=True, text=True)
        if result.returncode != 0:
            print("Compile Error:", result.stderr)
        else:
            print("Compile Success")

    def simulate(self):
        try:
            result = subprocess.run([self.vvp_path, "main"], capture_output=True, check=True)
            output = result.stdout
            hash_value = hashlib.sha256(output).hexdigest()[:16]
            print(f"Simulation Success: Output Hash = {hash_value}")
            return hash_value
        except subprocess.CalledProcessError as e:
            print("Simulation Error:", e.stderr)
            return None

