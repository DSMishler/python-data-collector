import sys
import os
import socket
import re
import datetime
import pickle
import pdcutils


target_dir   = None
benchmark    = None
hostname     = socket.gethostname()
if hostname.find('.') != -1: # prune dot from hostname if needed
    hostname = hostname[:hostname.find('.')]
tmp_fname    = f"mzz_gather_{hostname}.txt"
pdc_root     = "~/python-data-collector"
pdc_cmd      = f"python {pdc_root}/python_data_collector.py"
run_ps_fname = f"mzz_run_ps_{hostname}.txt"
today        = str(datetime.date.today())


class generator_manager:
    def __init__(self, subclass):
        self.generator = subclass(today, hostname, target_dir)
    def generate_pdcstr(self):
        pdcstr = ""
        pdcstr += pdc_cmd
        pdcstr += " "
        pdcstr += f"pre \"{self.generator.pre}\""
        pdcstr += " "
        pdcstr += f"rf \"{self.generator.run_fname}\""
        pdcstr += " "
        pdcstr += f"pf {run_ps_fname}"
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
    def all_runs(self, requested_params={}):
        os.system(f"mkdir -p {self.generator.data_dir}")
        params_dict = self.generator.generate_params_dict(**requested_params)
        f = open(run_ps_fname, "wb")
        pickle.dump(params_dict, f)
        f.close()

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

    # pdcutils.generate_run_ps_file(run_np_fname, 1e5, 4e8, 1.2)
    
    import generators

    if benchmark == "stream_1node":
        manager = generator_manager(generators.generator_stream_1node.stream_1node_generator)
    elif benchmark == "stream_2node":
        manager = generator_manager(generators.generator_stream_2node.stream_2node_generator)
    elif benchmark == "osu_bench":
        manager = generator_manager(generators.generator_osu_bench.osu_bench_generator)
    elif benchmark == "teams_bench":
        manager = generator_manager(generators.generator_teams.teams_bench_generator)
    elif benchmark == "heat3d":
        manager = generator_manager(generators.generator_heat3d.heat3d_generator)
    elif benchmark == "gemm":
        manager = generator_manager(generators.generator_dplasma_gemm.dplasma_gemm_generator)
    elif benchmark.lower() == "pcc":
        manager = generator_manager(generators.generator_PCC.PCC_generator)
    else:
        print(f"did not understand benchmark {benchmark}")
        exit()
    
    requested_params = {} # currently for heat3d 1 node
    # requested_params["Ns"] = pdcutils.generate_log_scale_stepped_array(1e3,1e4,1.2)
    requested_params["Ns"] = [i for i in range(1000, 20001, 1000)]
    requested_params["codes"] = ["original", "ompb", "omps", "ompd", "norm"]
    # requested_params["iterations"] = [500]
    # requested_params["modes"] = [0,1,3]
    # requested_params["hosts"] = ["weaver6,weaver7"]
    # requested_params["npernode"] = [1]
    # requested_params["mpienv"] = ["NVSHMEMTEST_USE_MPI_LAUNCHER=1"]

    # manager.generator.out_fname=pdcutils.add_to_csv_fname(manager.generator.out_fname, "_XBUS")

    manager.all_runs(requested_params)

    os.system(f"rm -f {run_ps_fname}")

    print(f"ended at {datetime.datetime.now()}")
