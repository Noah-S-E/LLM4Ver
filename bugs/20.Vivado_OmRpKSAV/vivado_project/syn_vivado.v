// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2023 Advanced Micro Devices, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2023.2 (lin64) Build 4029153 Fri Oct 13 20:13:54 MDT 2023
// Date        : Thu May 16 16:01:22 2024
// Host        : zw-virtual-machine running 64-bit Ubuntu 22.04.2 LTS
// Command     : write_verilog -force syn_vivado.v
// Design      : top
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7k70tfbv676-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *)
module top
   (y,
    clk,
    wire3,
    wire2,
    wire1,
    wire0);
  output [9:0]y;
  input [0:0]clk;
  input [2:0]wire3;
  input [5:0]wire2;
  input [5:0]wire1;
  input [5:0]wire0;

  wire \<const0> ;
  wire GND_2;
  wire VCC_1;
  wire forvar7_i_1_n_0;
  wire [5:0]wire1;
  wire [5:0]wire1_IBUF;
  wire [9:0]y;
  wire [0:0]y_OBUF;

  GND GND
       (.G(\<const0> ));
  GND GND_1
       (.G(GND_2));
  VCC VCC
       (.P(VCC_1));
  (* XILINX_LEGACY_PRIM = "LD" *) 
  (* XILINX_TRANSFORM_PINMAP = "VCC:GE GND:CLR" *) 
  LDCE #(
    .INIT(1'b0)) 
    forvar7
       (.CLR(GND_2),
        .D(forvar7_i_1_n_0),
        .G(forvar7_i_1_n_0),
        .GE(VCC_1),
        .Q(y_OBUF));
  LUT6 #(
    .INIT(64'h9669699669969668)) 
    forvar7_i_1
       (.I0(wire1_IBUF[4]),
        .I1(wire1_IBUF[5]),
        .I2(wire1_IBUF[1]),
        .I3(wire1_IBUF[0]),
        .I4(wire1_IBUF[3]),
        .I5(wire1_IBUF[2]),
        .O(forvar7_i_1_n_0));
  IBUF \wire1_IBUF[0]_inst 
       (.I(wire1[0]),
        .O(wire1_IBUF[0]));
  IBUF \wire1_IBUF[1]_inst 
       (.I(wire1[1]),
        .O(wire1_IBUF[1]));
  IBUF \wire1_IBUF[2]_inst 
       (.I(wire1[2]),
        .O(wire1_IBUF[2]));
  IBUF \wire1_IBUF[3]_inst 
       (.I(wire1[3]),
        .O(wire1_IBUF[3]));
  IBUF \wire1_IBUF[4]_inst 
       (.I(wire1[4]),
        .O(wire1_IBUF[4]));
  IBUF \wire1_IBUF[5]_inst 
       (.I(wire1[5]),
        .O(wire1_IBUF[5]));
  OBUF \y_OBUF[0]_inst 
       (.I(y_OBUF),
        .O(y[0]));
  OBUF \y_OBUF[1]_inst 
       (.I(\<const0> ),
        .O(y[1]));
  OBUF \y_OBUF[2]_inst 
       (.I(\<const0> ),
        .O(y[2]));
  OBUF \y_OBUF[3]_inst 
       (.I(\<const0> ),
        .O(y[3]));
  OBUF \y_OBUF[4]_inst 
       (.I(\<const0> ),
        .O(y[4]));
  OBUF \y_OBUF[5]_inst 
       (.I(\<const0> ),
        .O(y[5]));
  OBUF \y_OBUF[6]_inst 
       (.I(\<const0> ),
        .O(y[6]));
  OBUF \y_OBUF[7]_inst 
       (.I(\<const0> ),
        .O(y[7]));
  OBUF \y_OBUF[8]_inst 
       (.I(\<const0> ),
        .O(y[8]));
  OBUF \y_OBUF[9]_inst 
       (.I(\<const0> ),
        .O(y[9]));
endmodule
