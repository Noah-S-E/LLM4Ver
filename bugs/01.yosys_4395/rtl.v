module top (y, clk);
  output wire [4:0] y;
  input wire clk; 

  wire [4:0] wire1; 

  assign wire1 = $signed((~""));
  assign y = wire1;
endmodule

