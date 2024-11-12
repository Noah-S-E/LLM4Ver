module top (
    output wire y,
    output wire [2:0] y2,
    output wire [2:0] y3,
    input wire clk,

    input wire wire1

);


    assign y3 = $unsigned(8'b10100000 + wire1);


    assign y2 = y3 - 1'b1;


    assign y = (8'b10011100 >> y2);

endmodule

