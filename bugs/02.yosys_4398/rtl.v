module top  (y, clk, wire1);
  output wire [1:0] y;
  input wire clk;
 input wire signed [5:0] wire1;  

  reg signed [1:0] forvar7 = 2'b00;  
  reg signed [6:0] forvar5 = 7'b0000000;  

  
  assign y = {forvar7};
  
  always
    @(posedge clk) 
    begin
      for (forvar5 = (7'b0000000); (forvar5 < (7'b0000001)); forvar5 = (forvar5 + (7'b0000001)))
        begin
          if ( (^(forvar5 + wire1) ? forvar5 : wire1) )
            begin
		          forvar7 = (2'b01);
            end
        end
    end
endmodule
