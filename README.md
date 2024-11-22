# LLM4Ver
## [Generating Syntax Valid Verilog Designs with LLMs to Detect Compiler Defects in FPGA Logic Synthesis Tools](https://github.com/Noah-S-E/LLM4Ver)

***
**Env dependencies:**
1. **python 3.8**
2. **openai 1.17.1**
3. **pyverilog 1.3.0**
4. **Provide an API for large language models in src/openai_client.py**

***
**Fuzz Testing Targets:(logic synthesis tools and simulated tools)**
1. **Vivado 2023.2**
2. **Yosys 0.39+165**
3. **Icarus Verilog V12_0**
4. **Quartus Prime 23.1**
***

## Our Work

In modern electronic system design, the **logic synthesis** and **functional simulation** steps of **Field-Programmable Gate Arrays (FPGAs)** play a crucial role. These steps are performed by **Electronic Design Automation (EDA) tools**, which:

- **Convert Hardware Description Language (HDL) code into logic gates and circuit layouts**, and
- **Simulate their behavior** to ensure the correctness and stability of the design.

However, **logic synthesis tools and simulation tools may contain defects** that can cause the design to exhibit unexpected behavior when implemented in hardware, leading to serious consequences.

### Our Solution: **VerFuzzer**

We propose a novel fuzzing method named **VerFuzzer**, the **first fuzz testing tool** that leverages **prompting large language models** for generating valid **Verilog programs** to test logic synthesis tools.


***
## directory structure
```
VerFuzzer-main/
├── README.md
├── check.py
├── config/
│   └── config.toml
├── src/
│   ├── AST.py
│   ├── code_generate.py
│   ├── code_inspect.py
│   ├── config_extract.py
│   ├── equiv_check.py
│   ├── equivcheck_code.py
│   ├── error_feedback.py
│   ├── generate.py
│   ├── openai_client.py
│   ├── prompt_generate.py
│   ├── run.sh
│   ├── run_main.sh
│   ├── run_symbiyosys.sh
│   ├── synthesis.py
│   ├── testbench.py
│   └── Tool/
│       ├── Icarus.py
│       ├── Vivado.py
│       └── Yosys.py
│   └── temp_save/
│       ├── tem_ast.txt
│       └── temp.v
```

The directory structure of the document is as follows. After adding the API, you can run the command below to execute:
```bash run.sh <outputdir> <number>```
***
## These are the bugs we have discovered (./bugs)
| ID    | Summary                                                                     | Software |
|-------|-----------------------------------------------------------------------------|----------|
| bug1  | Bit Operations Mishandles Empty String                                      | Yosys    |
| bug2  | Netlist Discrepancies with Design                                           | Yosys    |
| bug3  | Signed Keyword Handling Defect                                              | Yosys    |
| bug4  | Abnormal Output                                                             | Yosys    |
| bug5  | Port Declaration Syntax Error                                               | Yosys    |
| bug6  | Incorrect Right Shift Operation                                             | Yosys    |
| bug7  | Bidirectional Port Drive Assertion Error                                    | Iverilog |
| bug8  | Assertion Error on Task Array Set                                           | Iverilog |
| bug9  | Crash for PHYCLK GEN7                                                       | Quartus  |
| bug10 | Crash for VRFX DDM                                                          | Quartus  |
| bug11 | Segmentation Fault                                                          | Vivado   |
| bug12 | Crash for Tcl PanicVA and TclEvalObjEx                                      | Vivado   |
| bug13 | Crash for NPinC, ConstProp                                                  | Vivado   |
| bug14 | Crash for HARTNlUtil, HARTLutMap                                            | Vivado   |
| bug15 | Crash for DFNode::calcConstantBinaryInt                                     | Vivado   |
| bug16 | Crash for HARTOptMux::groupMFFC                                             | Vivado   |
| bug17 | Crash for HARTOptMux::createPartition                                       | Vivado   |
| bug18 | Crash for HOptGenControl::areadInSource                                     | Vivado   |
| bug19 | Crash for DFLink::findIndexForPortName                                      | Vivado   |
| bug20 | Bt-Width Definition Inconsistencies                                         | Vivado   |

We are grateful to the staff of these tools for their assistance in discovering and confirming vulnerabilities.
