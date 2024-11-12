## Internal Error in PHYCLK Sub-system in Quartus Prime

```
Problem Details
Error:
Internal Error: Sub-system: PHYCLK, File: /quartus/periph/phyclk/phyclk_gen7.cpp, Line: 1590
iterm != nullptr
Stack Trace:
Quartus 0x20f3c: PHYCLK_GEN7::replace_connection + 0xd0 (periph_phyclk)
Quartus 0x1b6f9: PHYCLK_GEN7::connect_phyclks_in_network + 0x32d (periph_phyclk)
Quartus 0x1d067: PHYCLK_GEN7::duplicate_and_rewire_phyclks + 0x327 (periph_phyclk)
Quartus 0x20974: PHYCLK_GEN7::post_process_legal_placement + 0x140 (periph_phyclk)
Quartus 0x24610: PCC_ENV_IMPL::perform_op + 0x25c (periph_pcc)
Quartus 0x20676: PCC_ENV_IMPL::refresh_placement_until_converged + 0x146 (periph_pcc)
Quartus 0x3479f: PCC_ENV_IMPL::commit + 0x5b (periph_pcc)
Quartus 0x2818a: PCC_PERIPH_FLOW::plan + 0x212 (periph_pcc)
Quartus 0x27601: fit2_fit_plan + 0x5e1 (comp_fit2)
Quartus 0x16442: TclNRRunCallbacks + 0x62 (tcl86)
Quartus 0x17c4d: TclEvalEx + 0x9ed (tcl86)
Quartus 0xa6a8b: Tcl_FSEvalFileEx + 0x22b (tcl86)
Quartus 0xa5136: Tcl_EvalFile + 0x36 (tcl86)
Quartus 0x230ac: qexe_evaluate_tcl_script + 0x66c (comp_qexe)
Quartus 0x21be9: qexe_do_tcl + 0x8f9 (comp_qexe)
Quartus 0x2a1ad: qexe_run_tcl_option + 0x6cd (comp_qexe)
Quartus 0x3dfaf: qcu_run_tcl_option + 0x6ef (comp_qcu)
Quartus 0x29969: qexe_run + 0x629 (comp_qexe)
Quartus 0x2abd6: qexe_standard_main + 0x266 (comp_qexe)
Quartus 0xbb82: qfit2_main + 0x82 (quartus_fit)
Quartus 0x28348: msg_main_thread + 0x18 (ccl_msg)
Quartus 0x29522: msg_thread_wrapper + 0x82 (ccl_msg)
Quartus 0x2b063: mem_thread_wrapper + 0x73 (ccl_mem)
Quartus 0x2610f: msg_exe_main + 0x17f (ccl_msg)
Quartus 0xcdcb: __scrt_common_main_seh + 0x10b (quartus_fit)
Quartus 0x17613: BaseThreadInitThunk + 0x13 (KERNEL32)
Quartus 0x526a0: RtlUserThreadStart + 0x20 (ntdll)

End-trace


Executable: quartus
Comment:
None

System Information
Platform: windows64
OS name: Windows 10
OS version: 10.0.19045

Quartus Prime Information
Address bits: 64
Version: 24.1.0
Build: 115
Edition: Pro Edition
```


