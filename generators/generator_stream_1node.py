class stream_1node_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "stream_1node_generator"
        self.target_file = "stream_1node"
        self.data_dir    = "stream_1node_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.pre         = ""

        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "stream_"
        of += "np1"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
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
    def generate_params_dict(self, lens = [1000, 2000], amodes = [0], bmodes = [-1], iters = [5]):
        param_dict = {}
        param_dict["len"]={}
        param_dict["len"]["flags"] = ["-l"]
        param_dict["len"]["values"] = lens
        param_dict["amode"]={}
        param_dict["amode"]["flags"] = ["-a"]
        param_dict["amode"]["values"] = amodes
        param_dict["bmode"]={}
        param_dict["bmode"]["flags"] = ["-b"]
        param_dict["bmode"]["values"] = bmodes
        param_dict["iterations"]={}
        param_dict["iterations"]["flags"] = ["-i"]
        param_dict["iterations"]["values"] = iters
        return param_dict
