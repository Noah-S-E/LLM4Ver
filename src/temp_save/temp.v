module top (
    input wire clk,
    input wire rst,
    input wire [3:0] d,       // Extend the input to 4 bits
    output reg [3:0] q        // Extend the output to 4 bits
);
    // Parameter declaration
    parameter SHIFT_VALUE = 1;
    parameter WIDTH = 4;
    
    // Internal signal
    reg [WIDTH-1:0] temp;

    // Generate block for initialization
    genvar i;
    generate
        for (i = 0; i < WIDTH; i = i + 1) begin : gen_block
            always @(posedge clk or posedge rst) begin
                if (rst) begin
                    temp[i] <= 1'b0;  // Initialize to zero on reset
                end else begin
                    temp[i] <= d[i];
                end
            end
        end
    endgenerate

    // Additional behavioral logic
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            q <= 4'b0000;  // Reset the output
        end else begin
            // Conditional statement
            if (temp[0]) begin
                q <= temp << SHIFT_VALUE;  // Left shift temp if LSB is 1
            end else begin
                q <= temp + 4'b0001;      // Increment temp if LSB is 0
            end
        end
    end
endmodule