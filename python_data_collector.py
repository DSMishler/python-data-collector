import sys
import os
import socket


# TODOs
# - make a way to let CTRL+c kill the whole program
# - allow user to choose which handler to use

hostname = socket.gethostname()

# defaults
error_max    = .01                            # error cutoff of 1%
run_min      = 3                              # minimum runs per data point
run_max      = 30                             # maximum runs per point (error)
range_min    = 10                             # minimum range
range_max    = 100                            # maximum range
range_stride = 10                             # run strides
run_preamble = None                           # preamble for runs, if necessary
run_fname    = None                           # file to run. required
output_fname = "mzz_dataout_"+hostname+".csv" # output csv of this program
tmp_fname    = "mzz_tmp_"+hostname+".txt"     # temp filename for this program
stderr_fname = "mzz_err_tmp_"+hostname+".txt" # temp filename for program errors

help_message = "python data collector. A program designed to make collecting"
help_message += "data easy and robust in your workflow. Pass any of the"
help_message += "following through the command line as separate arguments"
help_message += "(e.g. stride 5)."

# Ugh, no mean and std on weaver
def mean(data):
    n = len(data)
    msum = 0
    for element in data:
        msum += element
    return msum/n

def variance(data): # with Bessel's correction
    n = len(data)
    # n must be at least 2
    vsum = 0
    mmean= mean(data)
    for element in data:
        vsum += (element-mmean)**2
    return vsum / (n-1)

def stdev(data):
    return (variance(data)**0.5)

def gaussian_error(data):
    n = len(data)
    return (stdev(data)/((n-1)**0.5)) # not sure if n-1 necessary, but safe

def print_global_parameters():
    print("global parameters of python data collector")
    print(f"    error maximum (error)  :  {error_max}")
    print(f"    minimum nruns (runs)   :  {run_min}")
    print(f"    maximum nruns (runmax) :  {run_max}")
    print(f"    range minimum (min)    :  {range_min}")
    print(f"    range maximum (max)    :  {range_max}")
    print(f"    range stride  (stride) :  {range_stride}")
    print(f"    preamble      (pre)    :  {run_preamble}")
    print(f"    file to run   (rf)     :  {run_fname}")
    print(f"    output file   (of)     :  {output_fname}")
    print(f"    storage file  (tf)     :  {tmp_fname}")
    print(f"    stderr file   (ef)     :  {stderr_fname}")

def parse_args(args):
    global error_max
    global run_min
    global run_max
    global range_min
    global range_max
    global range_stride
    global run_preamble
    global run_fname
    global output_fname
    global tmp_fname
    global stderr_fname
    # parse through arguments in c-like fashion
    i = 1
    while(i < len(args)):
        this_arg = args[i].lower()
        if this_arg in ["help", "-help", "--help", "-h", "--h"]:
            print(help_message)
            print_global_parameters()
            exit()
        elif this_arg in ["error", "max_error"]:
            i += 1
            error_max = float(args[i])
        elif this_arg in ["run_min", "runs", "nruns"]:
            i += 1
            run_min = int(args[i])
        elif this_arg in ["run_max", "runmax"]:
            i += 1
            run_max = int(args[i])
        elif this_arg in ["min", "range_min"]:
            i += 1
            range_min = int(args[i])
        elif this_arg in ["max", "range_max"]:
            i += 1
            range_max = int(args[i])
        elif this_arg in ["stride", "range_stride"]:
            i += 1
            range_stride = int(args[i])
        elif this_arg in ["run_preamble", "pre", "preamble"]:
            i += 1
            run_preamble = args[i]
        elif this_arg in ["run_fname", "rf"]:
            i += 1
            run_fname = args[i]
        elif this_arg in ["output_fname", "of", "output"]:
            i += 1
            output_fname = args[i]
        elif this_arg in ["tmp_fname", "tf"]:
            i += 1
            tmp_fname = args[i]
        elif this_arg in ["stderr_fname", "ef"]:
            i += 1
            stderr_fname = args[i]
        else:
            print(f"could not understand argument '{this_arg}'")
        i += 1


def check_global_parameters():
    if run_fname is None:
        print("ERROR: must have a command to run (rf)")
        return False
    if range_min > range_max:
        print("ERROR: range error")
        return False
    return True


class heat3d_handler:
    def __init__(self):
        self.name = "head3d handler"
        return
    def refresh_current_runs(self):
        return {"time" : [], "compute_time": [], "dt_time": []}
    def generate_commandstr(self, n, N):
        commandstr = ""
        if (run_preamble is not None):
            commandstr += f"{run_preamble} "
        commandstr += f"{run_fname} "
        commandstr += f"-X {n} "
        commandstr += f"-Y {n} "
        commandstr += f"-Z {n} "
        commandstr += f"1>{tmp_fname} "
        commandstr += f"2>{stderr_fname}"
        return commandstr
    def parse_tmp(self, N, data_dest):
        f = open(tmp_fname, "r")

        time = -1
        dt_time = -1
        compute_time = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            try:
                int(words[0])
            except ValueError:
                continue
            if int(words[0]) == N:
                for j in range(len(words)):
                    if words[j] == "Time":
                        time = float(words[j+1].replace('(',''))
                        break
                # next line is the last line
                words = lines[i+1].split()
                for j in range(len(words)):
                    if words[j] == "surface:":
                        dt_time = float(words[j+1])
                    if words[j] == "compute:":
                        compute_time = float(words[j+1])

                break
        data_dest["time"].append(time)
        data_dest["compute_time"].append(compute_time)
        data_dest["dt_time"].append(dt_time)

        f.close()

class cpybench_handler:
    def __init__(self):
        self.name = "cpybench handler"
        return
    def refresh_current_runs(self):
        return {"time_total" : [], "time_TplusdT": []}
    def generate_commandstr(self, n, N):
        commandstr = ""
        if (run_preamble is not None):
            commandstr += f"{run_preamble} "
        commandstr += f"{run_fname} "
        commandstr += f"-X {n} "
        commandstr += f"-Y {n} "
        commandstr += f"-Z {n} "
        commandstr += f"1>{tmp_fname} "
        commandstr += f"2>{stderr_fname}"
        return commandstr
    def parse_tmp(self, N, data_dest):
        f = open(tmp_fname, "r")

        time = -1
        time_TplusdT = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            try:
                int(words[0])
            except ValueError:
                continue
            if int(words[0]) == N:
                for j in range(len(words)):
                    if words[j] == "Time":
                        time = float(words[j+1].replace('(',''))
                        break
                # next line is the last line
                words = lines[i+1].split()
                for j in range(len(words)):
                    if words[j] == "TplusdT:":
                        time_TplusdT = float(words[j+1])

                break
        data_dest["time_total"].append(time)
        data_dest["time_TplusdT"].append(time_TplusdT)

        f.close()

class stream_benchmark_handler:
    def __init__(self):
        self.name = "stream benchmark handler"
        return
    def refresh_current_runs(self):
        return {"time_total" : [], "time_stream": []}
    def generate_commandstr(self, n, iterations):
        commandstr = ""
        if (run_preamble is not None):
            commandstr += f"{run_preamble} "
        commandstr += f"{run_fname} "
        commandstr += f"-N {n} "
        commandstr += f"1>{tmp_fname} "
        commandstr += f"2>{stderr_fname}"
        return commandstr
    def parse_tmp(self, iterations, data_dest):
        f = open(tmp_fname, "r")

        time = -1
        time_stream = -1

        lines = f.read().split('\n')
        for i in range(len(lines)):
            words = lines[i].split()
            if len(words) == 0:
                continue
            try:
                int(words[0])
            except ValueError:
                continue
            if int(words[0]) == iterations:
                for j in range(len(words)):
                    if words[j] == "Time":
                        time = float(words[j+1].replace('(',''))
                        break
                # next line is the last line
                words = lines[i+1].split()
                for j in range(len(words)):
                    if words[j] == "stream:":
                        time_stream = float(words[j+1])

                break
        data_dest["time_total"].append(time)
        data_dest["time_stream"].append(time_stream)

        f.close()

class run_manager:
    def __init__(self, handler):
        self.handler = handler
        self.data = dict()
        self.current_runs = {}
        self.refresh_current_runs()
        return
    def refresh_current_runs(self):
        self.current_runs = handler.refresh_current_runs()
    def generate_commandstr(self, n, iterations):
        return handler.generate_commandstr(n, iterations)
    def run_once(self, n, iterations):
        commandstr = self.generate_commandstr(n, iterations)
        os.system(commandstr)
        f = open(stderr_fname, "r")
        ftext = f.read()
        if len(ftext) > 0:
            print("        warning: this run completed, but stderr output was nonempty")
            print(ftext)
        f.close()
    def parse_tmp(self, iterations):
        handler.parse_tmp(iterations, self.current_runs)
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
            myerror =  gaussian_error(self.current_runs[key])
            myerror /= mean(self.current_runs[key])
            if myerror > max_error:
                max_error = myerror
        return max_error

    def perform_runs_for(self, n, iterations):
        nruns = 0
        self.refresh_current_runs()
        for i in range(run_min):
            print(f"    run {nruns}")
            self.run_once(n, iterations)
            self.parse_tmp(iterations)
            nruns += 1
        myerror = self.calculate_max_percent_error()
        while(myerror > error_max):
            print(f"    run {nruns} (needed because error is currently too"
                  f" high at {myerror*100}%)")
            self.run_once(n, iterations)
            self.parse_tmp(iterations)
            myerror = self.calculate_max_percent_error()
            nruns += 1
            if (nruns >= run_max):
                print("ERROR: too many runs for this to make sense.")
                print("(adjust rum_max if you think this was a mistake.)")
                exit()
        return_dict = {"n" : n}
        return_dict["iterations"] = iterations
        return_dict["nruns"] = nruns

        for attr in self.current_runs:
            attr_mean = mean(self.current_runs[attr])
            attr_error  = gaussian_error(self.current_runs[attr])
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
        f = open(output_fname, "w")
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
        
        if not os.path.isfile(output_fname):
            self.write_init(return_dict)

        string = ""
        for thing in array:
            string += str(thing) + ","
        string = string[:-1] + "\n"
        f = open(output_fname, "a")
        f.write(string)
        f.close()


if __name__ == "__main__":
    parse_args(sys.argv)
    if check_global_parameters() is False:
        print_global_parameters()
        exit()

    # always overwrite old data
    os.system(f"rm -f {output_fname}")

    if "heat3d" in run_fname.lower():
        handler = heat3d_handler()
        task = "heat3d"
    elif "cpybench" in run_fname.lower():
        handler = cpybench_handler()
        task = "cpybench"
    elif "stream" in run_fname.lower():
        handler = stream_benchmark_handler()
        task = "stream_benchmark"
    else:
        print(f"ERROR: I don't know what program you're running,"
              f" so I don't know what handler to use.")
        exit()

    manager = run_manager(handler)



    current_n = range_min

    ex_commandstr = manager.generate_commandstr(current_n,10000)
    print(f"example command:")
    print(f"```{ex_commandstr}```")

    while current_n <= range_max:
        print(f"task {task} to {output_fname} with n={current_n}")
        return_dict = manager.perform_runs_for(current_n, 10000)
        manager.write(return_dict)
        current_n += range_stride

    os.system(f"rm {tmp_fname}")
    os.system(f"rm {stderr_fname}")
