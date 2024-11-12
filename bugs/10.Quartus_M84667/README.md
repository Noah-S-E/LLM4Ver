

## Internal Error in VRFX2 Sub-system in Quartus Prime
```
Problem Details
Error:
Internal Error: Sub-system: VRFX2, File: /quartus/synth/vrfx2/vrfx2_ddm.cpp, Line: 6168
uinst
Stack Trace:
  Quartus         0x7d2d9e: VRFX_DDM::create_ddm_connections() + 0xa40 (synth_vrfx2)
  Quartus         0x7d41b0: VRFX_DDM::convert_netlist(VRFX2_TOPDOWN_MGR::ELAB_INST_ENTRY*) + 0x626 (synth_vrfx2)
  Quartus         0x7d5205: vrfx2_ddm_convert_all_netlists(BASEX_ELABORATE_INFO*, Netlist*) + 0xa52 (synth_vrfx2)
  Quartus         0x820225: new_verific::VRFX2_EXTRACTOR::extract_hierarchy(char const*, std::vector<BASEX_ENTITY*, std::allocator<BASEX_ENTITY*> > const&, BASEX_ELABORATE_INFO*, bool, bool, bool, bool, bool) + 0x1787 (synth_vrfx2)
  Quartus         0x10da19: QIS_RTL_STAGE::IMPL::elaborate_verific(QHD_PARTITION*, BASEX_ENTITY*, BASEX_ELAB_INFO_CORE&, std::vector<BASEX_ENTITY*, std::allocator<BASEX_ENTITY*> > const&, bool) + 0x305 (synth_qis)
  Quartus         0x14ee1d: QIS_RTL_STAGE::IMPL::elaborate_ddm_module(DDM_MODULE*, BASEX_ENTITY*, std::vector<BASEX_ENTITY*, std::allocator<BASEX_ENTITY*> > const&, std::vector<DDM_MODULE*, std::allocator<DDM_MODULE*> >&) + 0x10d (synth_qis)
  Quartus         0x14f77a: QIS_RTL_STAGE::IMPL::elaborate_ddm(DDM_MODULE*) + 0x11a (synth_qis)
  Quartus         0x152249: QIS_RTL_STAGE::IMPL::elaborate_ddm() + 0xd75 (synth_qis)
  Quartus         0x152278: QIS_RTL_STAGE::elaborate_ddm() + 0xc (synth_qis)
  Quartus          0x2a8a2: SCMD_ELABORATE::execute(Tcl_Interp*, DTCL_ARGS&) + 0x5aa (synth_scmd)
  Quartus           0xc7da: DTCL_COMMAND_PKG::eval_cmd(void*, Tcl_Interp*, int, Tcl_Obj* const*) + 0x148 (dni_dtcl)
  Quartus          0x4bb47: TclNRRunCallbacks + 0x67 (tcl8.6)
  Quartus          0x4cf29: TclEvalEx + 0x599 (tcl8.6)
  Quartus          0xf40fe: Tcl_FSEvalFileEx + 0x21e (tcl8.6)
  Quartus          0xf4246: Tcl_EvalFile + 0x26 (tcl8.6)
  Quartus          0x270b4: qexe_evaluate_tcl_script(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) + 0x388 (comp_qexe)
  Quartus          0x29e08: qexe_do_tcl(QEXE_FRAMEWORK*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::list<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > > const&, bool, bool) + 0x71b (comp_qexe)
  Quartus          0x2afc1: qexe_run_tcl_option(QEXE_FRAMEWORK*, char const*, std::__cxx11::list<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bool) + 0x8a5 (comp_qexe)
  Quartus          0x6fb73: QCU::DETAIL::intialise_qhd_and_run_qexe(QCU_FRAMEWORK&, FIO_PATH const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, char const*, std::__cxx11::list<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bool) + 0x99 (comp_qcu)
  Quartus          0x6fe66: qcu_run_tcl_option(QCU_FRAMEWORK*, char const*, std::__cxx11::list<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::allocator<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > > >*, bool) + 0x286 (comp_qcu)
  Quartus         0x40703e: qsyn2_tcl_process_default_flow_option(ACF_VARIABLE_TYPE_ENUM, char const*) + 0x4b5 (quartus_syn)
  Quartus          0x2fbb6: qexe_standard_main(QEXE_FRAMEWORK*, QEXE_OPTION_DEFINITION const**, int, char const**) + 0x7dd (comp_qexe)
  Quartus         0x406a7c: qsyn2_main(int, char const**) + 0x123 (quartus_syn)
  Quartus          0x43980: msg_main_thread(void*) + 0x10 (ccl_msg)
  Quartus          0x44400: msg_thread_wrapper(void* (*)(void*), void*) + 0x8c (ccl_msg)
  Quartus          0x1ff9d: mem_thread_wrapper(void* (*)(void*), void*) + 0x9d (ccl_mem)
  Quartus           0xe178: err_thread_wrapper(void* (*)(void*), void*) + 0x1e (ccl_err)
  Quartus          0x44329: msg_exe_main(int, char const**, int (*)(int, char const**)) + 0xd3 (ccl_msg)
  Quartus         0x406952: main + 0x26 (quartus_syn)
  System           0x3a7e5: __libc_start_main + 0xe5 (c)
  Quartus         0x406879: _start + 0x29 (quartus_syn)

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
