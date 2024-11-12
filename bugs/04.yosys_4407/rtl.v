module top  (y, clk, wire3, wire2, wire1, wire0);
  output wire [(1'h0):(1'h0)] y;
  input wire [(1'h0):(1'h0)] clk;
  input wire [(1'h1):(1'h0)] wire3;
  input wire [(2'h2):(1'h0)] wire2;
  input wire [(2'h2):(1'h0)] wire1;
  input wire [(2'h2):(1'h0)] wire0;


  reg [(1'h0):(1'h0)] reg264 = (1'h0);
  reg [(2'h2):(1'h0)] reg274 = (1'h0);
  wire [(2'h2):(1'h0)] wire7;
  wire [(2'h2):(1'h0)] wire6;
  wire [(2'h2):(1'h0)] wire5;
  wire [(1'h0):(1'h0)] wire4;
  reg [(1'h0):(1'h0)] reg278 = (1'h0);
  assign y = reg278;
  assign wire4 = wire0[0:0];

  assign wire6 = (((8'ha7) ? {wire4} : ((8'ha6) ? wire1 : (8'h9e))) - (8'ha3));

  always
    @(posedge clk) begin

              reg274 <= wire3[(1'h1):(1'h1)];
              if ({$unsigned((wire0 >> wire6))})
                begin

                end
              else
                begin
                  reg278 = $unsigned(({reg274} > $unsigned(reg264)));
                end

    end
  
      
endmodule
