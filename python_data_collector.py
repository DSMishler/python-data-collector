import sys
import os
import socket
import re
import pickle
import pdcutils


# TODOs
# - allow user to choose which handler to use
# - decide how to handle data you don't necessarily want to permute

hostname = socket.gethostname()

gpd = {} # global_parameters_dictionary
# This program runs as many times as necessary on every point until
# the error of the desired quanitites is lower than a number. Think
# of this as a percentage, so 0.01 is 1%. This is simple gaussian error, so
# more runs with the same standard deviation lowers the error
gpd["error_max"]     = {"value": 0.1,
                        "tfunc": float,
                        "desc" : "error cutoff for each point",
                        "flags": ["error", "max_error"]}
# minimum number of runs to collect for each data point
gpd["run_min"]       = {"value": 2,
                        "tfunc": int,
                        "desc" : "minimum runs for each point",
                        "flags": ["run_min", "runs", "nruns"]}
gpd["run_max"]       = {"value": 40,
                        "tfunc": int,
                        "desc" : "error out after this many runs on a point",
                        "flags": ["run_max", "runmax"]}
gpd["run_preamble"]  = {"value": None,
                        "tfunc": str,
                        "desc" : "Preamble for runs if needed (e.g. mpirun)",
                        "flags": ["run_preambe", "pre"]}
gpd["run_fname"]     = {"value": None,
                        "tfunc": str,
                        "desc" : "filename to run",
                        "flags": ["rfile", "run_fname", "rf"]}
gpd["run_dim_fname"] = {"value": None,
                        "tfunc": str,
                        "desc" : "pickle file containing desired datapoints",
                        "flags": ["pfile", "run_dim_fname", "pf"]}
gpd["output_fname"]  = {"value": "mzz_dataout_"+hostname+".csv",
                        "tfunc": str,
                        "desc" : "output csv of this program's collected data",
                        "flags": ["output_fname", "of", "output"]}
gpd["stdout_fname"]  = {"value": "mzz_tmp_"+hostname+".txt",
                        "tfunc": str,
                        "desc" : "temp filename for the runfile's stdout",
                        "flags": ["stdout_fname", "tf"]}
gpd["stderr_fname"]  = {"value": "mzz_err_tmp_"+hostname+".txt",
                        "tfunc": str,
                        "desc" : "temp filename for the runfile's stderr",
                        "flags": ["stderr_fname", "ef"]}


help_message = "python data collector. A program designed to make collecting"
help_message += "data easy and robust in your workflow. Pass any of the"
help_message += "following through the command line as separate arguments"
help_message += str([f"{key}: {gpd[key]['flags']}" for key in gpd])
help_message += "(e.g. nruns 5)."


def print_global_parameters():
    print("global parameters of python data collector")
    for key in gpd:
        print(f"    {key:13}: {str(gpd[key]['value']):25}# {gpd[key]['desc']}")

def parse_args(args):
    i = 1
    while(i < len(args)):
        this_arg = args[i].lower()
        if this_arg in ["help", "-help", "--help", "-h", "--h"]:
            print(help_message)
            print_global_parameters()
            exit()
        # else
        arg_found = False
        for key in gpd:
            if this_arg in gpd[key]["flags"]:
                type_func = gpd[key]["tfunc"]
                # a typing function like (int, str, float, etc.)
                i += 1
                gpd[key]["value"] = type_func(args[i])
                arg_found = True
                break
        if arg_found == False:
            print(f"could not understand argument '{this_arg}'")

        i += 1
            
def check_global_parameters():
    if gpd["run_fname"]["value"]is None:
        print("ERROR: must have a command to run (rf)")
        return False
    if gpd["run_dim_fname"]['value'] is None:
        print("you need a run dimension file!")
        return False
    return True



class run_manager:
    def __init__(self, handler):
        self.handler = handler
        self.data = dict()
        self.current_runs = {}
        self.refresh_current_runs()
        return
    def refresh_current_runs(self):
        self.current_runs = handler.refresh_current_runs()
    def generate_commandstr(self, param_dict):
        commandstr = ""
        if (gpd['run_preamble']['value'] is not None):
            commandstr += f"{gpd['run_preamble']['value']} "
        commandstr += pdcutils.flags_from_dict(param_dict, flags_type="preamble")

        commandstr += f"{gpd['run_fname']['value']} "
        commandstr += pdcutils.flags_from_dict(param_dict, flags_type="function")

        commandstr += f"1>{gpd['stdout_fname']['value']} "
        commandstr += f"2>{gpd['stderr_fname']['value']}"
        return commandstr
    def run_once(self, paramdict):
        commandstr = self.generate_commandstr(paramdict)
        os.system(commandstr)
        f = open(gpd['stderr_fname']['value'], "r")
        ftext = f.read()
        if len(ftext) > 0:
            print("        warning: this run completed, but stderr output was not empty")
            print(ftext)
        f.close()
    def parse_tmp(self, param_dict):
        handler.parse_tmp(param_dict, self.current_runs)
        for key in self.current_runs:
            for element in self.current_runs[key]:
                if element < 0:
                    print(f"negative value detected ", end="")
                    print(f"({element} for {key}). abort.")
                    exit()

    # must be called on array with length at least 1, preferrably 2.
    def calculate_max_percent_error(self):
        max_error = 0
        for key in self.current_runs:
            myerror =  pdcutils.gaussian_error(self.current_runs[key])
            myerror /= pdcutils.mean(self.current_runs[key])
            if myerror > max_error:
                max_error = myerror
        return max_error

    def perform_runs_for(self, param_dict):
        nruns = 0
        runs_per_cmd = 0
        cmds = 0
        try:
            param_dict["nruns"]
            runs_per_cmd = param_dict["nruns"]['value']
        except KeyError:
            runs_per_cmd = 1
        self.refresh_current_runs()
        while nruns < gpd["run_min"]['value']:
            print(f"        run {nruns}",end="")
            if runs_per_cmd > 1:
                print(f"-{nruns+runs_per_cmd-1}")
            else:
                print()
            self.run_once(param_dict)
            self.parse_tmp(param_dict)
            nruns += runs_per_cmd
            cmds += 1
        myerror = self.calculate_max_percent_error()
        while(myerror > gpd["error_max"]['value']):
            print(f"        run {nruns} (needed because error is currently too"
                  f" high at {myerror*100}%)")
            self.run_once(param_dict)
            self.parse_tmp(param_dict)
            myerror = self.calculate_max_percent_error()
            nruns += runs_per_cmd
            cmds += 1
            if (cmds >= gpd["run_max"]['value']):
                print("ERROR: too many runs for this to make sense.")
                print("(adjust run_max if you think this was a mistake.)")
                exit()

        return_dict = {"nruns": nruns}
        return_dict["cmds"] = cmds

        for key in param_dict:
            return_dict[key] = str(param_dict[key]["value"]).replace(',',':')

        for attr in self.current_runs:
            attr_mean = pdcutils.mean(self.current_runs[attr])
            attr_error  = pdcutils.gaussian_error(self.current_runs[attr])
            return_dict[attr] = {"mean" : attr_mean, "error" : attr_error}

        return return_dict

    def write_init(self, return_dict):
        string = ""
        for key1 in return_dict:
            obj1 = return_dict[key1]
            if type(obj1) is not dict:
                string += key1
                string += ","
            else:
                for key2 in obj1:
                    obj2 = obj1[key2]
                    if type(obj2) is not dict:
                        string += key1+"-"+key2
                        string += ","
                    else:
                        print(f"unknown error: possibly triply layered dict?")
        string = string[:-1] + "\n"
        f = open(gpd["output_fname"]['value'], "w")
        f.write(string)
        f.close()


    def write(self, return_dict):
        array = []
        for key1 in return_dict:
            obj1 = return_dict[key1]
            if type(obj1) is not dict:
                array.append(obj1)
            else:
                for key2 in obj1:
                    obj2 = obj1[key2]
                    if type(obj2) is not dict:
                        array.append(obj2)
                    else:
                        print(f"unknown error: possibly triply layered dict?")
        
        if not os.path.isfile(gpd["output_fname"]['value']):
            self.write_init(return_dict)

        string = ""
        for thing in array:
            string += str(thing) + ","
        string = string[:-1] + "\n"
        f = open(gpd["output_fname"]['value'], "a")
        f.write(string)
        f.close()


if __name__ == "__main__":
    parse_args(sys.argv)
    if check_global_parameters() is False:
        print_global_parameters()
        exit()


    import handlers

    # always overwrite old data
    os.system(f"rm -f {gpd['output_fname']['value']}")

    if "heat3d" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_heat3d.heat3d_handler(gpd)
        task = "heat3d"
    elif "stream" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_stream.stream_benchmark_handler(gpd)
        task = "stream_benchmark"
    elif "osu_bench" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_osu.osu_benchmark_handler(gpd)
        task = "osu_benchmark"
    elif "teams" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_teams.teams_benchmark_handler(gpd)
        task = "teams_benchmark"
    elif "gemm" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_dplasma_gemm.dplasma_gemm_handler(gpd)
        task = "dplasma_dgemm"
    elif "pcc" in gpd["run_fname"]['value'].lower():
        handler = handlers.handler_PCC.PCC_handler(gpd)
        task = "PCC"
    else:
        print(f"ERROR: I don't know what program you're running,"
              f" so I don't know what handler to use.")
        exit()

    f = open(gpd["run_dim_fname"]['value'], "rb")
    params_dict = pickle.load(f)
    f.close()

    manager = run_manager(handler)
    ex_commandstr = manager.generate_commandstr(pdcutils.get_nth_dict(params_dict, 0))
    print(f"example command:")
    print(f"```{ex_commandstr}```")
    
    for i in range(pdcutils.count_permutations(params_dict)):
        param_dict = pdcutils.get_nth_dict(params_dict, i)
        print(f"task {task} to {gpd['output_fname']['value']} with params:")
        for key in param_dict:
            print(f"    {key}: {param_dict[key]['value']}")

        return_dict = manager.perform_runs_for(param_dict)
        manager.write(return_dict)

    os.system(f"rm {gpd['stdout_fname']['value']}")
    os.system(f"rm {gpd['stderr_fname']['value']}")
