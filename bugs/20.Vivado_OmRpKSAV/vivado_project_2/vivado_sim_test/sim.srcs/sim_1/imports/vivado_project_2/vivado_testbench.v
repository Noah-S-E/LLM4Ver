`include "../data/cells_cmos.v"
`include "../data/cells_cyclone_v.v"
`include "../data/cells_verific.v"
`include "../data/cells_xilinx_7.v"
`include "../data/cells_yosys.v"
`include "syn_vivado.v"

module testbench  ;
  wire [(32'h9):(32'h0)] y;
  reg [(1'h0):(1'h0)] clk;
  reg [(2'h2):(1'h0)] wire3;
  reg [(3'h5):(1'h0)] wire2;
  reg signed [(3'h5):(1'h0)] wire1;
  reg [(3'h5):(1'h0)] wire0;
  top #() top1 (.y(y), .clk(clk), .wire3(wire3), .wire2(wire2), .wire1(wire1), .wire0(wire0));
  initial
    begin
      clk = (1'h0);
      {wire3, wire2, wire1, wire0} = (1'h0);
      #10 {wire3, wire2, wire1, wire0} = (254'h27facae24b87efc91cb6a84e6c8e39876d91718c0ab33e483411627f804de100);
      #10 {wire3, wire2, wire1, wire0} = (253'h18e1f7d46f511cebaefe5152105620ceb0f8b394976347ac08205d9dc4595de5);
      #10 {wire3, wire2, wire1, wire0} = (255'h4ae4d4d2caa2efc45cd8b675e5c53f5a1b0f4011a942b03cce1c11ac9d318485);
      #10 {wire3, wire2, wire1, wire0} = (255'h6a085cbfa1e96a6b5241f49a7f151b68978bd8ccc3be3f86f3037339c8c9608f);
      #10 {wire3, wire2, wire1, wire0} = (255'h4e0aaf2427d1958c0b075d749e4e95814cfee14ea6a62ad70f7266e091577f9b);
      #10 {wire3, wire2, wire1, wire0} = (256'hdbdb1d86026b4a780e10e454b84f82958ffbf5e3c5ed37d17e3785519be7f3fa);
      #10 {wire3, wire2, wire1, wire0} = (256'hfdbf672be0c0ec9f1e91fa1634a81201211ee2b0d31b26f5f4f6273740e5ac89);
      #10 {wire3, wire2, wire1, wire0} = (255'h6dcce6ec3918c771fc0712a736c408b550e3f7c4fad8f8f541dab5cfdfdca958);
      #10 {wire3, wire2, wire1, wire0} = (256'hdc0676530dc00484ab379d2ade3cf39465d8a07b25c0c75e4fcbc283034cc5d4);
      #10 {wire3, wire2, wire1, wire0} = (256'h9f6c295158fb2dea1a2cb50d137bdd799ce39ba16a19b7e04e5f928ec0dd91fc);
      #10 {wire3, wire2, wire1, wire0} = (254'h31efb20784a6bb13892439c9a9f384c86acb641e7cd517f8f7eb9f20f4644bd2);
      #10 {wire3, wire2, wire1, wire0} = (256'hfaf89a519021f65a03b331ce3c1bd98c5ba4d5eec23be11328de6b21ab123515);
      #10 {wire3, wire2, wire1, wire0} = (255'h426184f46e4af6096eaa7b1e8ecdad553f4044db9b24eac871c3eece6bf49ac7);
      #10 {wire3, wire2, wire1, wire0} = (256'h988b40ff8546177e0338baa805dca6fcdc3156e09f172883e2eb8da43a8a4a63);
      #10 {wire3, wire2, wire1, wire0} = (256'h8e266cdcd8e96909352d4004b4d10363e8d244649ddb5e7a996421ea7f9fee47);
      #10 {wire3, wire2, wire1, wire0} = (249'h14f99d98dd557a017fece6e0f58ed14ac092dff28459f8b5bcdf45ed8fd4035);
      #10 {wire3, wire2, wire1, wire0} = (256'hbdc12cdec7e957bfd88b8c1d08722dadd17b34e3dcfec1b86ad475845784bbfd);
      #10 {wire3, wire2, wire1, wire0} = (255'h6ba8b5184a1c66a7111a41cbdfeac417000485bb528c78f64ba388a250902ff7);
      #10 {wire3, wire2, wire1, wire0} = (255'h6dab4eac9c63af6c45653bb331eed233b929fa5aa608c9ed38298f664438c2e5);
      #10 {wire3, wire2, wire1, wire0} = (256'hd95d0b6d23a5630773030aaf75bc84fbd7bd11d18971bc905b0854ac8ce03d17);
      #10 $finish;
    end
  always
    #5 clk = (~clk);
  always
    @(posedge clk) $strobe ("%b", y);
endmodule
