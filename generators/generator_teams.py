class teams_bench_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "teams_bench_generator"
        self.target_file = "teams"
        self.data_dir    = "teams_bench_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.out_fname   = None
        self.run_fname   = None
        self.pre         = ""
    def mode_to_label(self, mode):
        if(mode == 0):
            return "nview"
        if(mode == 1):
            return "rview"
        if(mode == 2):
            return "uview"
        return None
    def generate_params_dict(self, lens = [1000, 2000], modes = [0, 1], iters = [5], TSs = [64], LSs = [64]):
        import pdcutils
        lens = pdcutils.generate_log_scale_array(2**27, 2**27, 2)
        TSs = pdcutils.generate_log_scale_array(2**2, 2**10, 2)
        LSs = pdcutils.generate_log_scale_array(2**2, 2**10, 2)
        modes = [0,1,2]
        param_dict = {}
        param_dict["len"]={}
        param_dict["mode"]={}
        param_dict["team_size"] = {}
        param_dict["league_size"] = {}
        param_dict["iterations"]={}
        param_dict["len"]["flag"] = "-N"
        param_dict["mode"]["flag"] = "-M"
        param_dict["team_size"]["flag"] = "-TS"
        param_dict["league_size"]["flag"] = "-LS"
        param_dict["iterations"]["flag"] = "-I"
        param_dict["len"]["values"] = lens
        param_dict["mode"]["values"] = modes
        param_dict["team_size"]["values"] = TSs
        param_dict["league_size"]["values"] = LSs
        param_dict["iterations"]["values"] = iters
        return param_dict
    def set_vals(self, param_dict):
        of = "" #output file
        of += f"{self.data_dir}/"
        of += f"{self.today}_"
        of += f"{self.hostname}_"
        of += "teams_bench_"
        of += "np1"
        of += ".csv"

        rf= f"{self.target_dir}/{self.target_file}"

        self.out_fname = of
        self.run_fname = rf
