import datetime

class stream_2node_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "stream_2node_generator"
        self.target_file = "stream_2node"
        self.data_dir    = "stream_2node_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
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
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "stream_"
        of += "np2_"
        of += f"{self.mode_to_label(mode)}"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file} -m {mode}"

        self.out_fname = of
        self.run_fname = rf
