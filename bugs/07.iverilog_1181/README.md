**Bidirectional Port Drive Assertion Error**

The following design triggers an error when implementing a bidirectional bus:

```
ivl: logic_lpm.c:2284: emit_signal_net_const_as_ca: Assertion `0' failed
```

The command executed is:

```sh
iverilog -tvlog95 rtl.v
```

```verilog
module top_module();
  wire data_bus; // Bidirectional data bus

  module_a u_module_a (
    .data(data_bus)
  );

  module_b u_module_b (
    .data(data_bus)
  );
endmodule

module module_a (
  inout wire data
);
  // Drive the data bus with 1 when module_a is active
  assign data = 1'b1;
endmodule

module module_b (
  inout wire data
);
  // Read data from the bus
  wire data_in = data;

  // Set data to high impedance to allow other modules to drive the bus
  assign data = 1'bz;
endmodule
```
