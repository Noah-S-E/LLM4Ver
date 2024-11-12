## 	Port Declaration Syntax Error with Yosys

### Version
Yosys 0.39+165

### On which OS did this happen?
Linux

### Reproduction Steps

In Yosys, the read_verilog and synth commands can be used to read and synthesize Verilog code. However, they may not always detect certain syntax errors in the port declaration list. For example, consider the following code:

```
module top (
  output wire y,
  input wire clk,
);

  wire [2:0] wire1 = 3'b000;
  assign y = wire1; 
endmodule
```


![images](./Inconsistent.png)

According to the Verilog language specification, the commaafter input wire clk, should not be there. Normally, this should be a syntax error. However, when I use Yosys to parse and synthesize this code, it does not detect this error and synthesizes successfully.