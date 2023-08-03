class teams_bench_generator:
    def __init__(self, today, hostname, target_dir):
        self.name        = "teams_bench_generator"
        self.target_file = "teams"
        self.data_dir    = "teams_bench_data"
        self.today       = today
        self.hostname    = hostname
        self.target_dir  = target_dir
        self.pre         = ""

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
    def mode_to_label(self, mode):
        if(mode == 0):
            return "nview"
        if(mode == 1):
            return "rview"
        if(mode == 2):
            return "uview"
        return None
    def generate_params_dict(self, lens = [1000, 2000], modes = [0, 1], iters = [5], TSs = [64], LSs = [64]):
        param_dict = {}
        param_dict["len"]={}
        param_dict["len"]["flags"] = ["-N"]
        param_dict["len"]["values"] = lens
        param_dict["mode"]={}
        param_dict["mode"]["flags"] = ["-M"]
        param_dict["mode"]["values"] = modes
        param_dict["team_size"] = {}
        param_dict["team_size"]["flags"] = ["-TS"]
        param_dict["team_size"]["values"] = TSs
        param_dict["league_size"] = {}
        param_dict["league_size"]["flags"] = ["-LS"]
        param_dict["league_size"]["values"] = LSs
        param_dict["iterations"]={}
        param_dict["iterations"]["flags"] = ["-I"]
        param_dict["iterations"]["values"] = iters
        return param_dict
