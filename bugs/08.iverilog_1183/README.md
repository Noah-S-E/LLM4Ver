Assertion lwid == ivl_signal_width(lsig)' failed

I have minimized the design and encountered an assertion error when using a task to assign values to array elements.

The error is as follows (I have upgraded to the latest version of Icarus Verilog `Icarus Verilog version 13.0 (devel) (s20221226-565-g6c8ed62a5)`):

```
iverilog -g2005-sv t.v
ivl: stmt_assign.c:480: store_vec4_to_lval: Assertion `lwid == ivl_signal_width(lsig)' failed.
```

<br/>

```verilog
module array();
  logic clk;
  logic [1:0] a[2];  

  task task1(output logic [1:0] a);
    begin
      a[0] = 00;  
      a[1] = 01;
    end
  endtask
  
  always @(posedge clk) begin
    task1(a);  
    $display("buff = %h", a); 
  end

endmodule
```
