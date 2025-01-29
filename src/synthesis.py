from Tool.Yosys import *
from Tool.Vivado import *
import sys
import logging


logging.basicConfig(filename='log.txt', level=logging.DEBUG, 
                    format='%(asctime)s - %(message)s')

def print_progress_bar(percentage, status):

    bar_length = 30
    filled_length = int(bar_length * percentage // 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"[{percentage:3d}%] {bar} {status}")

def Yosys_synthesis(output_folder):
    print("🛠  YOSYS SYNTHESIS INITIALIZING [RUNNING]")

    
    print_progress_bar(30, "Building RTL topology...")
    print_progress_bar(45, "Optimizing logic gates...")
    rtl_file = f"{output_folder}/yosys/rtl.v"
    output_directory = f"{output_folder}/yosys/"

    try:
        yosys = Yosys()
        yosys.run_synth(rtl_file, output_directory)
        print("✅ YOSYS SYNTHESIS COMPLETE [SUCCESS]")
        return "success"
    
    except SynthesisError as e:
        print(f"❌YOSYS SYNTHESIS FAILED [ERROR]")
        print(f"Error Detail: {str(e)}")
    except FileNotFoundError as e:
        print(f"❌ File Error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
    
    return None
    

def Vivado_synthesis(output_folder):
    print("\n\n⚙  VIVADO SYNTHESIS INITIALIZING [RUNNING]")
    print_progress_bar(30, "Loading design files...")
    print_progress_bar(50, "Analyzing timing constraints...")
    
    vivado = Vivado()
    output_directory_vivado = f"{output_folder}/vivado"
    
    try:
        print_progress_bar(70, "Running place & route...")
        vivado.run_synth("top", f"{output_directory_vivado}/rtl.v", output_directory_vivado)
        print("✅ VIVADO SYNTHESIS COMPLETE [SUCCESS]")
        return "success"
    
    except VivadoSynthesisError as e:
        print(f"❌ VIVADO SYNTHESIS FAILED [ERROR]")
        print(f"Error Detail: {str(e)}")
    except FileNotFoundError as e:
        print(f"❌ File Error: {str(e)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command Failed: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(" Usage: python synthesis.py output_folder")
        sys.exit(1)
        
    output_folder = sys.argv[1]
    
    if ((result_yosys := Yosys_synthesis(output_folder)) == "success") and ((result_vivado := Vivado_synthesis(output_folder)) == "success"):
        print("FULLY SYNTHESIZED [SUCCESS]")
    else:
        print("\nSynthesis pipeline aborted!")
        sys.exit(1)
