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
    def generate_params_dict(self, lens = [1000, 2000], modes = [0, 1], iterations = [5], hosts=None, npernode=None, mpienv=None):
        param_dict = {}
        param_dict["len"]={}
        param_dict["len"]["flags"] = ["-l"]
        param_dict["len"]["values"] = lens
        param_dict["mode"]={}
        param_dict["mode"]["flags"] = ["-m"]
        param_dict["mode"]["values"] = modes
        param_dict["iterations"]={}
        param_dict["iterations"]["flags"] = ["-i"]
        param_dict["iterations"]["values"] = iterations
        if hosts is not None:
            param_dict["hosts"]={}
            param_dict["hosts"]["flags"] = ["--host"]
            param_dict["hosts"]["values"] = hosts
            param_dict["hosts"]["preamble"] = True
        if npernode is not None:
            param_dict["npernode"]={}
            param_dict["npernode"]["flags"] = ["-npernode"]
            param_dict["npernode"]["values"] = npernode
            param_dict["npernode"]["preamble"] = True
        if mpienv is not None:
            param_dict["mpienv"]={}
            param_dict["mpienv"]["flags"] = ["-x"]
            param_dict["mpienv"]["values"] = mpienv
            param_dict["mpienv"]["preamble"] = True
            
        return param_dict
    def set_vals(self, param_dict):
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "stream_"
        of += "np2_NVL"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
