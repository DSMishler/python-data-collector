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
tmp_fname    = f"mzz_gather_{hostname}.txt"
pdc_root     = "~/Kokkos/python-data-collector"
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
    def all_runs(self):
        os.system(f"mkdir -p {self.generator.data_dir}")
        params_dict = self.generator.generate_params_dict()
        f = open(run_ps_fname, "wb")
        pickle.dump(params_dict, f)
        f.close()

        self.generator.set_vals(params_dict)
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
    else:
        print(f"did not understand benchmark {benchmark}")
        exit()
    manager.all_runs()

    os.system(f"rm -f {run_ps_fname}")

    print(f"ended at {datetime.datetime.now()}")

    pdcutils.generate_plot_code_dict(manager.generator.data_dir)
