import sys
import os

# defaults
error_max    = .1              # error cutoff of  10%
run_min      = 3               # minimum runs per data point
range_min    = 10              # minimum range
range_max    = 100             # maximum range
range_stride = 10              # run strides
run_preamble = None            # preamble for runs, if necessary
run_fname    = None            # file to run. required
output_fname = "dataout.csv"   # output csv of this program
tmp_fname    = "mzz_tmp.txt"   # temporary filename for this program
stderr_fname = "mzzerr_tmp.txt"# temporary filename for program errors

help_message = "no help message yet, King. Good luck."
"""
no help message yet, King. Good luck.
"""

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
    print(f"    error maximum :  {error_max}")
    print(f"    minimum nruns :  {run_min}")
    print(f"    range minimum :  {range_min}")
    print(f"    range maximum :  {range_max}")
    print(f"    range stride  :  {range_stride}")
    print(f"    preamble      :  {run_preamble}")
    print(f"    file to run   :  {run_fname}")
    print(f"    output file   :  {output_fname}")
    print(f"    storage file  :  {tmp_fname}")
    print(f"    stderr file   :  {stderr_fname}")

def parse_args(args):
    global error_max
    global run_min
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
            exit()
        elif this_arg in ["error", "max_error"]:
            i += 1
            error_max = float(args[i])
        elif this_arg in ["run_min", "runs"]:
            i += 1
            run_min = int(args[i])
        elif this_arg in ["min", "range_min"]:
            i += 1
            range_min = int(args[i])
        elif this_arg in ["max", "range_max"]:
            i += 1
            range_max = int(args[i])
        elif this_arg in ["stride", "range_stride"]:
            i += 1
            range_stride = int(args[i])
        elif this_arg in ["run_preamble", "rp", "preamble"]:
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
        print("ERROR: required to have a file to run")
        return False
    if range_min > range_max:
        print("ERROR: range error")
        return False
    return True


class heat3d_handler:
    def __init__(self):
        self.data = dict()
        self.current_runs = {}
        self.refresh_current_runs()
        return
    def refresh_current_runs(self):
        self.current_runs = {"time" : [], "compute_time": [], "dt_time": []}
    def run_once(self, n, N):
        commandstr = ""
        if (run_preamble is not None):
            commandstr += f"{run_preamble} "
        commandstr += f"{run_fname} "
        commandstr += f"-X {n} "
        commandstr += f"-Y {n} "
        commandstr += f"-Z {n} "
        commandstr += f"1>{tmp_fname} "
        commandstr += f"2>{stderr_fname}"
        os.system(commandstr)
        f = open(stderr_fname, "r")
        ftext = f.read()
        if len(ftext) > 0:
            print("        warning: this run completed, but stderr output was nonempty")
            # print(ftext)
        f.close()
    def parse_tmp(self, n, N):
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
        self.current_runs["time"].append(time)
        self.current_runs["compute_time"].append(compute_time)
        self.current_runs["dt_time"].append(dt_time)

        f.close()

    # must be called on array with length at least 1, preferrably 2.
    def calculate_max_percent_error(self):
        max_error = 0
        for key in self.current_runs:
            myerror =  gaussian_error(self.current_runs[key])
            myerror /= mean(self.current_runs[key])
            if myerror > max_error:
                max_error = myerror
        return max_error

    def perform_runs_for(self, n, N):
        global error_max
        global run_min
        nruns = 0
        self.refresh_current_runs()
        for i in range(run_min):
            print(f"    run {nruns}")
            self.run_once(n, N)
            self.parse_tmp(n, N)
            nruns += 1
        myerror = self.calculate_max_percent_error()
        while(myerror > error_max):
            print(f"    run {nruns}")
            self.run_once(n, N)
            self.parse_tmp(n, N)
            myerror = self.calculate_max_percent_error()
            nruns += 1
        time = mean(self.current_runs["time"])
        dt_time = mean(self.current_runs["dt_time"])
        compute_time = mean(self.current_runs["compute_time"])
        time_err = gaussian_error(self.current_runs["time"])
        dt_time_err = gaussian_error(self.current_runs["dt_time"])
        compute_time_err = gaussian_error(self.current_runs["compute_time"])
        return {"n" : n,
                "N" : N,
                "time": {"mean" : time, "error" :time_err},
                "dt_time": {"mean" : dt_time, "error" :dt_time_err},
                "compute_time": {"mean" : compute_time, "error" :compute_time_err},
                "nruns" : nruns}

    def write_init(self, return_dict):
        string = ""
        for key1 in return_dict:
            obj1 = return_dict[key1]
            if type(obj1) is not dict:
                string += key1
                string += ", "
            else:
                for key2 in obj1:
                    obj2 = obj1[key2]
                    if type(obj2) is not dict:
                        string += key1+"-"+key2
                        string += ", "
                    else:
                        print(f"unknown error on line {__LINE__}: possibly triply layered dict?")
        string = string[:-2] + "\n"
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
                        print(f"unknown error on line {__LINE__}: possibly triply layered dict?")
        
        if not os.path.isfile(output_fname):
            self.write_init(return_dict)

        string = ""
        for thing in array:
            string += str(thing) + ", "
        string = string[:-2] + "\n"
        f = open(output_fname, "a")
        f.write(string)
        f.close()



if __name__ == "__main__":
    parse_args(sys.argv)
    if check_global_parameters() is False:
        print_global_parameters()
        exit()

    # always overwrite old data
    os.system(f"rm {output_fname}")

    # TODO: choose a handler
    handler = heat3d_handler()

    current_n = range_min
    while current_n <= range_max:
        print(f"task heat3d with n={current_n}")
        return_dict = handler.perform_runs_for(current_n, 10000)
        handler.write(return_dict)
        current_n += range_stride

    os.system(f"rm {tmp_fname}")
    os.system(f"rm {stderr_fname}")
