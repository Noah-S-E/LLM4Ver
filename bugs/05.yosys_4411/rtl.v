module top (
  output wire y,
  input wire clk,
);

  wire [2:0] wire1 = 3'b000;
  assign y = wire1; 
endmodule