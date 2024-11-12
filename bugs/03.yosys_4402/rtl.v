module top  (y, clk, wire0);
  output wire y;
  input wire clk;

  input wire signed [5:0] wire0;

  reg reg16 = (1'h0);

  reg signed [2:0]forvar14 = (1'h0);

  reg [2:0] forvar10 = (1'h0);
  reg [2:0] forvar9 = (1'h0);

  assign y = reg16;
  always
    @(posedge clk) begin
       for (forvar14 = (1'h0); (forvar14 < (1'h1)); forvar14 = (forvar14 + (1'h1)))
        begin
       reg16 = ($signed((wire0 <= forvar14)) ? $unsigned((-forvar9)) : (^~$signed(forvar10)));
       end
    end
endmodule
