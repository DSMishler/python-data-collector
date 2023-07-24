import sys
import os
import socket
import re
import datetime
import pdcutils


target_dir   = None
benchmark    = None
hostname     = socket.gethostname()
tmp_fname    = f"mzz_gather_{hostname}.txt"
pdc_root     = "~/Kokkos/python-data-collector"
pdc_cmd      = f"python {pdc_root}/python_data_collector.py"
run_ns_fname = f"mzz_run_ns_{hostname}.txt"
today        = str(datetime.date.today())


class stream_1node_generator:
    def __init__(self):
        self.name        = "stream_1node_generator"
        self.target_file = "stream_1node"
        self.data_dir    = "stream_1node_data"
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = ""
    def mode_to_char(self, mode):
        if(mode == 0):
            return "n"
        if(mode == 1):
            return "r"
        if(mode == 2):
            return "u"
        return None
    def bmode_to_style(self, mode):
        if(mode == -1):
            return "pp"
        else:
            return "pe"
    def generate_param_dict_list(self):
        param_dict_list = []
        amodes = [0,1,2]
        bmodes = [-1,0,1,2]
        for amode in amodes:
            for bmode in bmodes:
                param_dict_list.append({"amode": amode, "bmode": bmode})
        return param_dict_list
    def set_vals(self, param_dict):
        amode = param_dict["amode"]
        bmode = param_dict["bmode"]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{today}_"
        of += f"{hostname}_"
        of += "stream_"
        of += "np1_"
        of += f"{self.bmode_to_style(bmode)}_"
        of += f"{self.mode_to_char(amode)}"
        of += "p"
        if bmode == -1:
            of += f"{self.mode_to_char(amode)}"
        else:
            of += f"{self.mode_to_char(bmode)}"
        of += ".csv"

        rf= f"{target_dir}/{self.target_file} -a {amode} -b {bmode}"

        self.out_fname = of
        self.run_fname = rf

class stream_2node_generator:
    def __init__(self):
        self.name        = "stream_2node_generator"
        self.target_file = "stream_2node"
        self.data_dir    = "stream_2node_data"
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = "mpirun -np 2"
    def mode_to_label(self, mode):
        if(mode == 0):
            return "mpi"
        if(mode == 1):
            return "rma"
        return None
    def generate_param_dict_list(self):
        param_dict_list = []
        modes = [0,1]
        for mode in modes:
            param_dict_list.append({"mode": mode})
        return param_dict_list
    def set_vals(self, param_dict):
        mode = param_dict["mode"]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{today}_"
        of += f"{hostname}_"
        of += "stream_"
        of += "np2_"
        of += f"{self.mode_to_label(mode)}"
        of += ".csv"

        rf= f"{target_dir}/{self.target_file} -m {mode}"

        self.out_fname = of
        self.run_fname = rf

class osu_bench_generator:
    def __init__(self):
        self.name        = "osu_bench_generator"
        self.target_file = "osu_bench"
        self.data_dir    = "osu_bench_data"
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = "mpirun -np 2"
    def mode_to_label(self, mode):
        if(mode == 4):
            return "put"
        if(mode == 5):
            return "get"
        return None
    def generate_param_dict_list(self):
        param_dict_list = []
        modes = [4,5]
        for mode in modes:
            param_dict_list.append({"mode": mode})
        return param_dict_list
    def set_vals(self, param_dict):
        mode = param_dict["mode"]
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{today}_"
        of += f"{hostname}_"
        of += "osu_bench_"
        of += "np2_"
        of += f"{self.mode_to_label(mode)}"
        of += ".csv"

        rf= f"{target_dir}/{self.target_file} -m {mode}"

        self.out_fname = of
        self.run_fname = rf



class generator_manager:
    def __init__(self, subclass):
        self.generator = subclass()
    def generate_pdcstr(self):
        pdcstr = ""
        pdcstr += pdc_cmd
        pdcstr += " "
        pdcstr += f"pre \"{self.generator.pre}\""
        pdcstr += " "
        pdcstr += f"rf \"{self.generator.run_fname}\""
        pdcstr += " "
        pdcstr += f"nf {run_ns_fname}"
        pdcstr += " "
        pdcstr += f"of {self.generator.out_fname}"
        pdcstr += " "
        pdcstr += f"tf {tmp_fname}"
        print(pdcstr)
        return pdcstr
    def run(self, pdcstr):
        os.system(pdcstr)
        if os.path.isfile(tmp_fname):
            print("detected pdc abort, manager also aborting")
            exit()
    def all_runs(self):
        os.system(f"mkdir -p {self.generator.data_dir}")
        param_dict_list = self.generator.generate_param_dict_list()
        for param_dict in param_dict_list:
            self.generator.set_vals(param_dict)
            pdcstr = self.generate_pdcstr()
            self.run(pdcstr)

help_message = "no help yet. Good luck chief, you're on your own."

def parse_args(args):
    global target_dir
    global benchmark
    # parse through arguments in c-like fashion
    i = 1
    while(i < len(args)):
        this_arg = args[i].lower()
        if this_arg in ["help", "-help", "--help", "-h", "--h"]:
            print(help_message)
            exit()
        if this_arg in ["benchmark", "b"]:
            i += 1
            benchmark = args[i]
        elif this_arg in ["target_dir", "td", "target"]:
            i += 1
            target_dir = args[i]
        else:
            print(f"could not understand argument '{this_arg}'")
        i += 1

if __name__ == "__main__":
    print(f"begin at {datetime.datetime.now()}")

    parse_args(sys.argv)

    pdcutils.generate_run_ns_file(run_ns_fname, 1e5, 4e8, 1.2)

    if benchmark == "stream_1node":
        manager = generator_manager(stream_1node_generator)
        manager.all_runs()
    elif benchmark == "stream_2node":
        manager = generator_manager(stream_2node_generator)
        manager.all_runs()
    elif benchmark == "osu_bench":
        manager = generator_manager(osu_bench_generator)
        manager.all_runs()
    else:
        print(f"did not understand benchmark {benchmark}")

    os.system(f"rm -f {run_ns_fname}")

    print(f"ended at {datetime.datetime.now()}")

    pdcutils.generate_plot_code(manager.generator.data_dir)
